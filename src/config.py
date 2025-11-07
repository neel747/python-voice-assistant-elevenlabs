import os
from dotenv import load_dotenv

load_dotenv()

AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("ELEVENLABS_API_KEY") or os.getenv(
    "API_KEY")  # ← accept both
USER_NAME = os.getenv("USER_NAME", "Alex")
SCHEDULE = os.getenv(
    "SCHEDULE", "Sales Meeting with Taipy at 10:00; Gym with Sophie at 17:00")

missing = [k for k, v in {"AGENT_ID": AGENT_ID,
                          "API_KEY": API_KEY}.items() if not v]
if missing:
    raise RuntimeError(f"Missing required env vars: {', '.join(missing)}")
