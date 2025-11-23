# src/tts_gtts.py
import os
import subprocess
from gtts import gTTS
from .logger import logger

def preprocess_text(text: str) -> str:
    """Expands common abbreviations for better speech."""
    replacements = {
        "e.g.": "for example",
        "i.e.": "that is",
        "etc.": "et cetera",
        "vs.": "versus",
    }
    for abbr, full in replacements.items():
        text = text.replace(abbr, full)
    return text

def speak(text: str, tld: str = 'com'):
    """
    Converts text to speech using Google Translate TTS and plays it via afplay (macOS).
    tld: Top-Level Domain for accent (e.g., 'com' for US, 'co.uk' for UK, 'co.in' for India).
    """
    try:
        # 0. Preprocess text
        text = preprocess_text(text)

        # 1. Generate MP3
        tts = gTTS(text=text, lang='en', tld=tld)
        filename = "tmp_output.mp3"
        tts.save(filename)

        # 2. Play MP3 (macOS specific) - Non-blocking
        # We use Popen so we can kill it later if needed
        process = subprocess.Popen(["afplay", filename])
        return process

    except Exception as e:
        logger.error(f"[TTS] gTTS error: {e}")
        # Fallback to say (blocking for now, or could be Popen too)
        subprocess.run(["say", text], check=False)
        return None
