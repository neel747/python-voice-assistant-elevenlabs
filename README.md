# Real-Time Voice Assistant

**Local STT (Faster Whisper) + Groq LLM + Free TTS (gTTS) + Wake Word (Porcupine)**

A fast, free, and private voice assistant that runs locally on your Mac (mostly).

## Features
- **Wake Word**: Hands-free activation using `Porcupine` (default: "Jarvis", custom models supported).
- **GUI**: User-friendly interface with chat history and status.
- **STT**: `faster-whisper` (local, fast, accurate).
- **LLM**: Groq API (Llama 3.1 8b) - extremely fast and free tier available.
- **TTS**: `gTTS` (Google Translate TTS) - free and unlimited.
- **Logging**: Professional logging to console and `app.log`.
- **VAD**: Silence detection to automatically stop recording when you stop speaking.

## Setup

1. **Install System Dependencies** (macOS)
   ```bash
   brew install portaudio ffmpeg
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   Create a `.env` file:
   ```ini
   # Required
   GROQ_API_KEY=gsk_...
   PICOVOICE_ACCESS_KEY=... (Get from Picovoice Console)

   # Optional
   OPENAI_API_KEY=sk-... (If using OpenAI instead of Groq)
   WAKE_WORD_MODEL_PATH=/path/to/hey_neel.ppn (Custom wake word model)
   ```

## Usage

### Run the GUI (Recommended)
```bash
python -m src.gui
```
- Say **"Jarvis"** (or your custom wake word) to activate.
- Or click **Start Listening**.
- Speak into your microphone.
- The assistant will reply with text and audio.

### Run the CLI (Terminal Mode)
```bash
python -m src.app
```
- Press **ENTER** to start recording.
- Speak, then stop speaking (it auto-detects silence).
- Press **q** to quit.
