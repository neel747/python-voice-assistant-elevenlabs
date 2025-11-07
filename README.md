# Python Voice Assistant (ElevenLabs, macOS)

## Setup (macOS + Conda)
1) `brew install portaudio`
2) `conda create -n voiceai python=3.11 -y && conda activate voiceai`
3) `conda install -c conda-forge portaudio pyaudio -y`
4) `pip install elevenlabs python-dotenv`
5) Create `.env` with AGENT_ID, API_KEY
6) Run: `python -m src.voice_assistant`
