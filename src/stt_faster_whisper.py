# src/stt_faster_whisper.py
import os
from faster_whisper import WhisperModel
from .logger import logger
from .config import TMP_WAV_PATH

# Global model instance to avoid reloading
# "base.en" is a good balance of speed/accuracy. "small.en" is better but slower.
# device="cpu" and compute_type="int8" works well on most machines.
# On Mac M1/M2, device="cpu" is often faster than "cuda" for small models unless you have specific torch setup.
MODEL_SIZE = "base.en"
_model = None

def get_model():
    global _model
    if _model is None:
        logger.info(f"[STT] Loading faster-whisper model '{MODEL_SIZE}'...")
        # Run on CPU with INT8 quantization for speed
        _model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    return _model

def transcribe_file(path: str = TMP_WAV_PATH) -> str:
    if not os.path.exists(path):
        return ""

    model = get_model()
    
    logger.info("[STT] Transcribing (faster-whisper)...")
    segments, info = model.transcribe(path, beam_size=5)
    
    # faster-whisper returns a generator, so we must iterate to get text
    text = " ".join([segment.text for segment in segments]).strip()
    
    return text
