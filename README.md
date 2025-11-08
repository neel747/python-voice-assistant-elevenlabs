# Real-Time Voice Assistant (OpenAI + ElevenLabs)

**macOS · Conda · Python 3.11**

Mic 🎤 → **OpenAI STT** → **GPT-4o-mini** 🧠 → **ElevenLabs TTS** 🔊

## Features
- Real-time voice loop (push-to-talk)
- OpenAI STT (Whisper / GPT-4o transcribe) + GPT-4o-mini chat
- ElevenLabs TTS with low-latency streaming
- .env-driven config (voice id, persona, schedule)

## Setup
```bash
brew install portaudio
conda create -n voiceai python=3.11 -y && conda activate voiceai
conda install -c conda-forge portaudio pyaudio -y
pip install -r requirements.txt
