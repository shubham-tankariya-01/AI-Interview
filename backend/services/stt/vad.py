import torch
import numpy as np
import logging

logger = logging.getLogger(__name__)

class VADProcessor:
    """Lightweight acoustic speech detector using Silero VAD.
    Processes only the last 512-sample window per chunk for speed."""

    def __init__(self, model):
        self.model = model
        self._call_count = 0

    def process(self, samples: np.ndarray) -> bool:
        """Returns True if speech is detected in the audio samples."""
        if len(samples) < 512:
            return False

        rms = float(np.sqrt(np.mean(samples ** 2)))
        if rms < 0.001:
            return False

        chunk = torch.from_numpy(samples[-512:].copy()).float()
        with torch.no_grad():
            prob = self.model(chunk, 16000).item()

        is_speech = prob > 0.5

        self._call_count += 1
        if self._call_count % 50 == 0:
            logger.debug(f"[VAD] RMS: {rms:.4f} | Prob: {prob:.4f} -> {'SPEECH' if is_speech else 'silence'}")

        return is_speech

def load_vad_model():
    """Download and return the Silero VAD model from torch.hub."""
    logger.info("[VAD] Loading Silero VAD model...")
    model, _ = torch.hub.load(
        repo_or_dir="snakers4/silero-vad",
        model="silero_vad",
        force_reload=False,
        trust_repo=True,
    )
    logger.info("[VAD] Silero VAD loaded.")
    return model
