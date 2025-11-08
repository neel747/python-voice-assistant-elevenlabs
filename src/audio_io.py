import wave
import pyaudio
import soundfile as sf
from .config import SAMPLE_RATE, CHANNELS, CHUNK, RECORD_SECONDS, TMP_WAV_PATH


def record_wav(path: str = TMP_WAV_PATH, seconds: int = RECORD_SECONDS):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=CHANNELS,
                    rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK)
    print("🎤 Recording... (speak)")
    frames = []
    for _ in range(0, int(SAMPLE_RATE / CHUNK * seconds)):
        frames.append(stream.read(CHUNK, exception_on_overflow=False))
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save via wave (or soundfile); using wave for compatibility
    wf = wave.open(path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("🛑 Recording stopped.")


def play_pcm16_bytes(pcm_bytes: bytes, sample_rate: int = 22050, channels: int = 1):
    """Generic player for raw PCM16 mono/stereo bytes."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=channels,
                    rate=sample_rate, output=True)
    stream.write(pcm_bytes)
    stream.stop_stream()
    stream.close()
    p.terminate()
