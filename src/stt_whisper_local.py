import whisper
from .config import TMP_WAV_PATH

# Load the base model (you can change to "small" or "tiny" for faster speed)
_model = whisper.load_model("base")

def transcribe_file(path: str = TMP_WAV_PATH) -> str:
    """Transcribe audio locally using Whisper."""
    try:
        print("[STT] Using local Whisper model (no API needed) …")
        result = _model.transcribe(path)
        text = result.get("text", "").strip()
        return text
    except Exception as e:
        print(f"[STT] Local Whisper error: {e}")
        return ""
