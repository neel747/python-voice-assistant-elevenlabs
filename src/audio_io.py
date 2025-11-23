import wave
import pyaudio
import soundfile as sf
import math
import struct
import time
from .logger import logger
from .config import (
    SAMPLE_RATE, CHANNELS, CHUNK, RECORD_SECONDS, TMP_WAV_PATH,
    SILENCE_THRESHOLD, SILENCE_DURATION, MAX_RECORD_SECONDS
)


def is_silent(data_chunk: bytes, threshold: int) -> bool:
    """Returns True if the RMS amplitude of the chunk is below threshold."""
    # Convert bytes to list of shorts (int16)
    shorts = struct.unpack(f"{len(data_chunk) // 2}h", data_chunk)
    # Calculate RMS
    sum_squares = sum(s**2 for s in shorts)
    rms = math.sqrt(sum_squares / len(shorts))
    return rms < threshold


def record_wav(path: str = TMP_WAV_PATH, timeout: int = None, on_speech_start=None):
    """
    Records audio from the microphone.
    - timeout: Max seconds to wait for speech to START. If None, waits indefinitely (or until max duration).
    - on_speech_start: Callback function to run when speech is first detected.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=CHANNELS,
                    rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK)
    
    logger.info(f"🎤 Recording... (timeout={timeout}s)")
    frames = []
    
    start_time = time.time()
    silence_start_time = None
    speech_started = False
    
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        is_silent_chunk = is_silent(data, SILENCE_THRESHOLD)

        if not speech_started:
            if not is_silent_chunk:
                speech_started = True
                logger.info("🗣️ Speech started!")
                
                # Trigger callback (e.g., to kill TTS)
                if on_speech_start:
                    on_speech_start()
                    
                silence_start_time = None # Reset silence timer
            elif timeout and elapsed_time > timeout:
                logger.info(f"🛑 Timeout reached ({timeout}s) without speech. Stopping.")
                break
        else:
            # Speech has started, look for end of speech (silence)
            if is_silent_chunk:
                if silence_start_time is None:
                    silence_start_time = current_time
                elif current_time - silence_start_time > SILENCE_DURATION:
                    logger.info(f"🛑 End of speech detected ({SILENCE_DURATION}s silence). Stopping.")
                    break
            else:
                silence_start_time = None # Reset if they talk again

        # Check max duration
        if elapsed_time > MAX_RECORD_SECONDS:
            logger.info(f"🛑 Max duration ({MAX_RECORD_SECONDS}s) reached. Stopping.")
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    # If we timed out without speech starting, don't save (or save but return False)
    if not speech_started and timeout and elapsed_time > timeout:
         # We can still save it for debugging, or just return False
         # Let's save it but return False so the GUI knows to ignore it.
         pass

    # Save via wave
    wf = wave.open(path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    logger.info(f"✅ Saved {len(frames) * CHUNK / SAMPLE_RATE:.1f}s of audio.")
    
    # Return True if speech was detected (or if we didn't have a timeout logic active)
    # If timeout was set, and speech_started is False, then we timed out.
    if timeout and not speech_started:
        return False
    return True


def play_pcm16_bytes(pcm_bytes: bytes, sample_rate: int = 22050, channels: int = 1):
    """Generic player for raw PCM16 mono/stereo bytes."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=channels,
                    rate=sample_rate, output=True)
    stream.write(pcm_bytes)
    stream.stop_stream()
    stream.close()
    p.terminate()
