import os

# ═══════════════════════════════════════════════════════════════════════
# STT Configuration
# ═══════════════════════════════════════════════════════════════════════

SAMPLE_RATE = 16000
MIN_UTTERANCE_SAMPLES = int(SAMPLE_RATE * 0.3)        # 300ms minimum audio to transcribe
MAX_BUFFER_SAMPLES = SAMPLE_RATE * 180                # 3-minute safety valve

CHECKPOINT_SECONDS = 15.0       # lock confirmed text every 15s for long speech
TAIL_OVERLAP_SECONDS = 3.0      # re-transcribe 3s of overlap at checkpoint boundary

INTERIM_INTERVAL_MS = 120       # how often to send interim transcription updates

# Whisper Model Settings
WHISPER_MODEL = "tiny.en"       # 6x faster than base.en on CPU, accurate for English
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE = "int8"
WHISPER_THREADS = max(os.cpu_count() or 4, 4)
