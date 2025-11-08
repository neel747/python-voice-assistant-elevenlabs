import os
from dotenv import load_dotenv

load_dotenv()

# === Required keys ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

# === Optional personalization ===
ELEVEN_VOICE_ID = os.getenv(
    "ELEVEN_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # default: "Rachel"
USER_NAME = os.getenv("USER_NAME", "Neel")
SCHEDULE = os.getenv(
    "SCHEDULE", "Meeting with Taipy team at 10:00; Gym session at 17:00")
SYSTEM_PROMPT = os.getenv(
    "SYSTEM_PROMPT",
    "You are a helpful real-time voice assistant. Be concise, friendly, and reference the user's schedule when helpful."
)

# === Recording configuration ===
SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "16000"))
CHANNELS = 1
CHUNK = 1024
RECORD_SECONDS = int(os.getenv("RECORD_SECONDS", "10")
                     )  # push-to-talk duration
TMP_WAV_PATH = os.getenv("TMP_WAV_PATH", "tmp_input.wav")

# === Validation: ensure API keys exist ===
missing = [k for k, v in {
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "ELEVEN_API_KEY": ELEVEN_API_KEY
}.items() if not v]
if missing:
    raise RuntimeError(
        f"Missing required env vars: {', '.join(missing)}. "
        "Create a .env file with OPENAI_API_KEY and ELEVEN_API_KEY."
    )
