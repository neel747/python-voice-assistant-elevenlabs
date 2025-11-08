from openai import OpenAI
from .config import OPENAI_API_KEY, TMP_WAV_PATH

_client = OpenAI(api_key=OPENAI_API_KEY)

def transcribe_file(path: str = TMP_WAV_PATH) -> str:
    # Prefer the current transcribe model; whisper-1 also works widely.
    # If you hit a model error, try: model="whisper-1"
    with open(path, "rb") as f:
        tr = _client.audio.transcriptions.create(
            model="gpt-4o-transcribe",  # or "whisper-1" if needed
            file=f,
            response_format="verbose_json"
        )
    return tr.text.strip() if hasattr(tr, "text") else (tr.get("text", "").strip())
