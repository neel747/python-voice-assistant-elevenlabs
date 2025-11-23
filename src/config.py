import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(
    os.path.dirname(os.path.dirname(__file__)), ".env"))

# === Required keys ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PICOVOICE_ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")
WAKE_WORD_MODEL_PATH = os.getenv("WAKE_WORD_MODEL_PATH") # Path to .ppn file
# === Optional personalization ===
USER_NAME = os.getenv("USER_NAME", "Neel")
SCHEDULE = os.getenv(
    "SCHEDULE", "Meeting with Taipy team at 10:00; Gym session at 17:00")
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are a helpful real-time voice assistant. "
    "You have access to tools for getting the current date, time, and performing calculations. "
    "If the user asks for the date or time, YOU MUST use the `get_current_date` or `get_current_time` tools. "
    "Do not say you don't have access. Use the tools provided."
)

# === Recording configuration ===
SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "16000"))
CHANNELS = 1
CHUNK = 1024
RECORD_SECONDS = int(os.getenv("RECORD_SECONDS", "10")
                     )  # push-to-talk duration
TMP_WAV_PATH = os.getenv("TMP_WAV_PATH", "tmp_input.wav")

# === Silence Detection ===
SILENCE_THRESHOLD = int(os.getenv("SILENCE_THRESHOLD", "800"))  # Amplitude threshold
SILENCE_DURATION = float(os.getenv("SILENCE_DURATION", "1.2"))  # Seconds of silence to stop
MAX_RECORD_SECONDS = int(os.getenv("MAX_RECORD_SECONDS", "30")) # Max recording duration

# === Validation: ensure API keys exist ===
missing = [k for k, v in {
    "GROQ_API_KEY": GROQ_API_KEY,
    "PICOVOICE_ACCESS_KEY": PICOVOICE_ACCESS_KEY,
}.items() if not v]
if missing:
    raise RuntimeError(
        f"Missing required env vars: {', '.join(missing)}. "
        "Create a .env file with GROQ_API_KEY and PICOVOICE_ACCESS_KEY."
    )
