from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import (
    Conversation,
    ConversationInitiationData,
)
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
import signal
import sys
from .config import API_KEY, AGENT_ID, USER_NAME, SCHEDULE


def main():
    conversation_override = {
        "agent": {
            "prompt": {
                "prompt": f"You are a helpful assistant. Your interlocutor has the following schedule: {SCHEDULE}."
            },
            "first_message": f"Hello {USER_NAME}, how can I help you today?",
        },
    }

    # ✅ Pass user_id here (in the initiation data), not to start_session()
    config = ConversationInitiationData(
        conversation_config_override=conversation_override,
        user_id=USER_NAME or "user",
    )

    client = ElevenLabs(api_key=API_KEY)

    def on_agent_response(text: str):
        if text:
            print(f"\nAssistant: {text}")

    def on_agent_interrupted(original: str, corrected: str):
        print("\n[Assistant interrupted]")
        if corrected:
            print(f"Assistant (truncated): {corrected}")

    def on_user_transcript(text: str):
        if text:
            print(f"User: {text}")

    conversation = Conversation(
        client,
        AGENT_ID,
        requires_auth=bool(API_KEY),
        audio_interface=DefaultAudioInterface(),
        config=config,
        callback_agent_response=on_agent_response,
        callback_agent_response_correction=on_agent_interrupted,
        callback_user_transcript=on_user_transcript,
    )

    def _shutdown(*_):
        try:
            conversation.end_session()
        except Exception:
            pass
        sys.exit(0)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    print("🎙️ Voice assistant starting... Speak after the beep. Press Ctrl+C to quit.")
    # ⛳️ No args here
    conversation.start_session()


if __name__ == "__main__":
    main()
