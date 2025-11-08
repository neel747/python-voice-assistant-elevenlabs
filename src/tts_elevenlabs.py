from elevenlabs import ElevenLabs
from .config import ELEVEN_API_KEY, ELEVEN_VOICE_ID
from .audio_io import play_pcm16_bytes

_client = ElevenLabs(api_key=ELEVEN_API_KEY)

def speak(text: str):
    """
    Generate speech and play it.
    The current SDK returns bytes-like audio (MP3/PCM depending on call).
    We'll request PCM via output format for zero-latency playback.
    """
    try:
        # Stream audio in PCM format for instant playback
        audio = _client.text_to_speech.convert(
            voice_id=ELEVEN_VOICE_ID,
            optimize_streaming_latency="0",
            output_format="pcm_22050",   # PCM16 22.05kHz mono
            text=text,
            model_id="eleven_multilingual_v2",
        )
        pcm = b"".join(chunk for chunk in audio)  # join streamed chunks
        play_pcm16_bytes(pcm, sample_rate=22050, channels=1)

    except Exception as e:
        print("⚠️ ElevenLabs streaming error, trying fallback:", e)
        try:
            # Optional fallback (legacy SDK)
            from elevenlabs import generate, play
            pcm_or_mp3 = generate(text=text, voice=ELEVEN_VOICE_ID, model="eleven_multilingual_v2")
            play(pcm_or_mp3)
        except Exception as inner_e:
            print("❌ ElevenLabs fallback failed:", inner_e)
            raise
