import asyncio
import time
import json
import logging
import traceback
import numpy as np

from core.webSocket_manager import manager
from services.stt.config import (
    SAMPLE_RATE, MIN_UTTERANCE_SAMPLES, MAX_BUFFER_SAMPLES,
    CHECKPOINT_SECONDS, TAIL_OVERLAP_SECONDS, INTERIM_INTERVAL_MS
)
from services.stt.text_utils import _is_hallucination, _merge_text
from services.stt.endpointing import determine_pause_threshold

logger = logging.getLogger(__name__)

async def _commit(buffer, session_id, text, reason):
    """Send final transcription to the client, trigger AI, and clear the buffer."""
    samples = len(buffer) // 4
    duration = samples / SAMPLE_RATE
    logger.info(f"\n[COMMIT] '{reason}' | {duration:.2f}s | \"{text}\"")
    buffer.clear()

    if samples >= MIN_UTTERANCE_SAMPLES and text:
        logger.info(f"[{session_id}] UTTERANCE END! Sending full sentence to Gemini: '{text}'")
        try:
            # --- FAKE DATABASE & GEMINI LOGIC FOR TESTING ---
            logger.info(f"[{session_id}] 💾 (Simulated) Saved user transcript to Database")
            logger.info(f"[{session_id}] 🧠 (Simulated) LLM Called with text: '{text}'")
            
            # 4. WebSocket Broadcast
            active_websockets = manager.active_connections.get(session_id, [])
            
            # Broadcast the finalized user text IMMEDIATELY
            for user_ws in active_websockets:
                await user_ws.send_text(json.dumps({
                    "type": "user_final",
                    "text": text
                }))
                
            # Simulate the AI responding after a tiny delay
            await asyncio.sleep(1)
            
            fake_ai_response = "This is a fake AI response to test the WebSocket."
            logger.info(f"[{session_id}] 💾 (Simulated) Saved AI transcript to Database: '{fake_ai_response}'")
            
            # Broadcast the AI response
            for user_ws in active_websockets:
                await user_ws.send_text(json.dumps({
                    "type": "ai_message",
                    "text": fake_ai_response
                }))
                
        except Exception as e:
            logger.error(f"Error processing transcript in commit: {e}")
    else:
        logger.info(f"[COMMIT:SKIP] {'no text' if not text else 'too short'}\n")

async def transcription_worker(queue, session_id, whisper_model, vad):
    """Main transcription loop with progressive confirmation."""
    buffer = bytearray()
    last_interim = 0.0
    silence_start = None

    # Progressive confirmation state
    confirmed = ""
    confirmed_bytes = 0
    tail_text = ""
    transcribing = False
    utterance_id = 0

    ckpt_bytes = int(CHECKPOINT_SECONDS * SAMPLE_RATE * 4)
    overlap_bytes = int(TAIL_OVERLAP_SECONDS * SAMPLE_RATE * 4)

    logger.info(f"[WORKER] Pipeline ready for session {session_id}.\n")

    try:
        while True:
            # ── Receive audio ────────────────────────────────────────
            try:
                raw_chunk = await asyncio.wait_for(queue.get(), timeout=0.03)
                # Frontend sends int16 PCM. Convert to float32.
                samples = (np.frombuffer(raw_chunk, dtype=np.int16).astype(np.float32) / 32768.0).copy()
                chunk = samples.tobytes()  # Store as float32 bytes in the buffer
                
                is_speech = vad.process(samples)
                now = time.time()

                if is_speech:
                    if silence_start and (now - silence_start) * 1000 > 100:
                        logger.debug(f"[VAD] Speech resumed after {(now - silence_start)*1000:.0f}ms")
                    silence_start = None
                elif silence_start is None and len(buffer) > 0:
                    silence_start = now

                buffer.extend(chunk)

                if len(buffer) // 4 >= MAX_BUFFER_SAMPLES:
                    await _commit(buffer, session_id, _merge_text(confirmed, tail_text), "safety")
                    confirmed, confirmed_bytes, tail_text, silence_start = "", 0, "", None
                    utterance_id += 1
                    continue

            except asyncio.TimeoutError:
                pass
            except asyncio.CancelledError:
                if buffer and (confirmed or tail_text):
                    await _commit(buffer, session_id, _merge_text(confirmed, tail_text), "disconnect")
                return

            now = time.time()
            if not buffer:
                continue

            buf_samples = len(buffer) // 4
            unconfirmed = len(buffer) - confirmed_bytes

            # ── Progressive checkpoint ───────────────────────────────
            if unconfirmed > ckpt_bytes and tail_text and not transcribing:
                confirmed = _merge_text(confirmed, tail_text)
                confirmed_bytes = max(0, len(buffer) - overlap_bytes)
                tail_text = ""
                logger.info(f"[CKPT] Locked: \"{confirmed[:80]}...\" ({confirmed_bytes//4/SAMPLE_RATE:.1f}s)")

            # ── Interim transcription (non-blocking) ─────────────────
            elapsed = (now - last_interim) * 1000
            if elapsed >= INTERIM_INTERVAL_MS and buf_samples >= MIN_UTTERANCE_SAMPLES and not transcribing:
                transcribing = True

                if confirmed_bytes > 0:
                    start = max(0, confirmed_bytes - overlap_bytes)
                    audio = np.frombuffer(bytes(buffer[start:]), dtype=np.float32).copy()
                else:
                    audio = np.frombuffer(bytes(buffer), dtype=np.float32).copy()

                snap_confirmed = confirmed
                current_utterance = utterance_id

                async def _interim():
                    nonlocal tail_text, transcribing, last_interim
                    try:
                        def _run(a):
                            segs, _ = whisper_model.transcribe(
                                a, beam_size=1, vad_filter=True,
                                vad_parameters=dict(min_silence_duration_ms=500),
                                condition_on_previous_text=False,
                                without_timestamps=True, language="en",
                            )
                            return " ".join(s.text for s in segs).strip()

                        t0 = time.time()
                        result = await asyncio.to_thread(_run, audio)
                        dt = time.time() - t0

                        # Race condition check: abort if commit happened while we were transcribing
                        if current_utterance != utterance_id:
                            logger.debug(f"[INTERIM] Stale result discarded (utterance {current_utterance} -> {utterance_id})")
                            return

                        if result and not _is_hallucination(result):
                            tail_text = result
                            full = _merge_text(snap_confirmed, result)
                            if dt > 0.3:
                                logger.debug(f"[INTERIM] [{dt*1000:.0f}ms] \"{full[:100]}\"")
                            try:
                                active_websockets = manager.active_connections.get(session_id, [])
                                for user_ws in active_websockets:
                                    await user_ws.send_text(json.dumps({"type": "interim", "text": full}))
                            except Exception as e:
                                logger.error(f"[INTERIM:ERROR] sending interim {e}")
                    except Exception as e:
                        logger.error(f"[INTERIM:ERROR] transcription {e}")
                    finally:
                        transcribing = False
                        last_interim = time.time()

                asyncio.create_task(_interim())

            # ── Silence-based commit ─────────────────────────────────
            if silence_start:
                silence_ms = (now - silence_start) * 1000
                full = _merge_text(confirmed, tail_text)
                
                should_commit = False
                commit_reason = ""

                # Semantic Endpointing
                # Analyzes the grammatical structure of the sentence to deduce a proper natural pause.
                threshold = determine_pause_threshold(full)

                if silence_ms >= threshold and full and not transcribing:
                    should_commit = True
                    commit_reason = f"silence_{silence_ms:.0f}ms"

                if should_commit:
                    # Final safety check if we were still transcribing
                    if transcribing and silence_ms >= threshold + 200:
                        await asyncio.sleep(0.05)
                        full = _merge_text(confirmed, tail_text)
                    await _commit(buffer, session_id, full, commit_reason)
                    confirmed, confirmed_bytes, tail_text = "", 0, ""
                    silence_start = None
                    transcribing = False
                    utterance_id += 1

    except Exception as e:
        logger.error(f"[WORKER:FATAL] {e}")
        traceback.print_exc()
