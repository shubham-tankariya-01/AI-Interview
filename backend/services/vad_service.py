import torch
import logging
from silero_vad import load_silero_vad

logger = logging.getLogger(__name__)

_vad_model = None


#a simple function same as getting client in ai_reasoning file
def _get_vad_model():
    global _vad_model
    if _vad_model is None:
        _vad_model = load_silero_vad()
        logger.info(" Silero VAD model loaded (CPU, ~1.5MB)...")

    return _vad_model



#state machine -> the so called VAD PROCESSOR
class VADProcessor:

    SAMPLE_RATE = 16000

    SPEECH_THRESHOLD =0.65

    SILENCE_DURATION_MS = 1200

    CHUNK_DURATION_MS = 100

    def __init__(self,session_id : str):
        self.session_id = session_id
        self.model = _get_vad_model()
        self.state = "IDLE"
        self.silence_counter_ms = 0

        logger.info(f"[VAD] Processor created for the session : {session_id}")
                       
    def process_chunk(self , audio_bytes: bytes)->str:
        
        # fe is sending audio in the raw binary bytes which represents the sound waves captured
        # somehow have to change them into some specific tensors so that model can understand them
        #so first ,converting into 16-bit int -32768 to 32767
        int16_tensor = torch.frombuffer(bytearray(audio_bytes), dtype=torch.int16).float()
        # divide by 32768.0 to "normalize" the audio into a range between -1.0 and 1.0.
        float_audio = int16_tensor/32768.0
        
        # Calculate the actual duration of this websocket payload (e.g. 4096 samples = 256ms)
        num_samples = float_audio.shape[0]
        actual_duration_ms = int((num_samples / self.SAMPLE_RATE) * 1000)

        # Silero requires EXACTLY 512 samples per chunk at 16kHz
        chunk_size = 512
        any_speech = False
        max_speech_prob = 0.0
        
        #Process each 512-sample slice one by one
        for i in range(0, num_samples, chunk_size):
            chunk = float_audio[i:i+chunk_size]
            if chunk.shape[0] != chunk_size:
                continue # Ignore tiny tail chunk if it doesn't fit perfectly
            
            # passing to a model 
            speech_prob = self.model(chunk, self.SAMPLE_RATE).item()
            if speech_prob > max_speech_prob:
                max_speech_prob = speech_prob
                
            if speech_prob > self.SPEECH_THRESHOLD:
                any_speech = True

        is_speech = any_speech

        #setting the current state from the result
        if self.state == "IDLE":
            if is_speech:
                # User started talking! Change state to SPEAKING.
                self.state = "SPEAKING"
                self.silence_counter_ms = 0
                logger.debug(f"[VAD:{self.session_id}] IDLE → SPEAKING (max_prob={max_speech_prob:.2f})")
                return "speech"
            # If not speech, just stay IDLE and do nothing.
            return "silence"

        elif self.state == "SPEAKING":
            if is_speech:
                self.silence_counter_ms = 0
                return "speech"
            else:
                self.state = "SILENCE_TIMER"
                self.silence_counter_ms = actual_duration_ms
                logger.debug(f"[VAD:{self.session_id}] SPEAKING → SILENCE_TIMER")
                return "silence"

        elif self.state == "SILENCE_TIMER":
            if is_speech:
                self.silence_counter_ms = 0
                logger.debug(f"[VAD:{self.session_id}] SILENCE_TIMER → SPEAKING (resumed)")
                return "speech"
            else: 
                self.silence_counter_ms += actual_duration_ms

                if self.silence_counter_ms >=self.SILENCE_DURATION_MS:

                    self.state = "IDLE"
                    self.silence_counter_ms = 0

                    logger.info(f"[VAD:{self.session_id}] UTTERANCE_END (after {self.SILENCE_DURATION_MS}ms silence)")

                    return "utterance_end"

                return "silence"

            return "silence"
        #Fallback(should theoretically never happen , yaa i know but being dev :| )
        return "silence"

    def reset(self):
        self.state = "IDLE"
        self.silence_counter_ms = 0
            

