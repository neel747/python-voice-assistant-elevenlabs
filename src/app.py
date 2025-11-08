import signal
import sys
from .audio_io import record_wav
from .stt_whisper_local import transcribe_file
from .nlp_local import chat_reply
from .tts_elevenlabs import speak


def _shutdown(*_):
    print("\n👋 Bye!")
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    print("🎙️ Real-Time Voice Assistant (OpenAI + ElevenLabs)")
    print("Press ENTER to record (~6s), or type 'q' + ENTER to quit.\n")

    while True:
        cmd = input("> ").strip().lower()
        if cmd == "q":
            _shutdown()

        record_wav()  # records to tmp_input.wav
        user_text = transcribe_file()
        if not user_text:
            print("🤷 No speech recognized. Try again.")
            continue

        print(f"🧑 You: {user_text}")
        bot_reply = chat_reply(user_text)
        print(f"🤖 Assistant: {bot_reply}")
        speak(bot_reply)


if __name__ == "__main__":
    main()
