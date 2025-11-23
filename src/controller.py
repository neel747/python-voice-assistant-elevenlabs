import threading
import time
import traceback
from .logger import logger
from .settings import SettingsManager
from .audio_io import record_wav
from .stt_faster_whisper import transcribe_file
from .nlp_groq import chat_reply
from .tts_gtts import speak

class AssistantController:
    def __init__(self, settings_manager: SettingsManager, update_callback):
        self.settings = settings_manager
        self.update_callback = update_callback  # Function to call with status updates (text, color)
        self.chat_callback = None               # Function to call with chat messages (sender, text)
        
        self.is_running = False
        self.thread = None
        self.current_tts_process = None
        self.was_interrupted = False
        
        # Initialize Wake Word
        self.wake_word_listener = None
        self.init_wake_word()

        self.accents_map = {
            "🇺🇸 US English": "com",
            "🇬🇧 UK English": "co.uk",
            "🇮🇳 Indian English": "co.in",
            "🇦🇺 Australian English": "com.au",
            "🇨🇦 Canadian English": "ca"
        }

    def init_wake_word(self):
        try:
            from .wake_word import WakeWordListener
            self.wake_word_listener = WakeWordListener()
        except Exception as e:
            logger.warning(f"⚠️ Wake Word not available: {e}")

    def set_chat_callback(self, callback):
        self.chat_callback = callback

    def start_listening(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._run_loop)
            self.thread.daemon = True
            self.thread.start()

    def stop_listening(self):
        self.is_running = False
        self.stop_tts()

    def stop_tts(self):
        """Kills the current TTS process if running."""
        if self.current_tts_process:
            if self.current_tts_process.poll() is None:
                logger.info("🛑 Interruption detected! Killing TTS.")
                self.was_interrupted = True
                try:
                    self.current_tts_process.terminate()
                    self.current_tts_process.wait(timeout=0.5)
                except Exception as e:
                    logger.error(f"Error killing TTS: {e}")
            self.current_tts_process = None

    def _update_status(self, text, color="gray"):
        if self.update_callback:
            self.update_callback(text, color)

    def _append_chat(self, sender, message):
        if self.chat_callback:
            self.chat_callback(sender, message)

    def _run_loop(self):
        self._update_status("Starting loop...", "blue")
        logger.info("Starting assistant loop...")
        
        conversation_active = False
        self.current_tts_process = None
        self.was_interrupted = False

        while self.is_running:
            try:
                # 0. Wake Word Check
                if self.wake_word_listener and not conversation_active and self.settings.get("wake_word_enabled", True):
                    keyword = self.wake_word_listener.keyword_name
                    self._update_status(f"👂 Waiting for '{keyword}'...", "blue")
                    
                    if not self.wake_word_listener.listen():
                        if not self.is_running: break
                        continue 
                    
                    self._update_status("⚡ Wake Word Detected!", "green")
                    logger.info("Wake word detected")
                    conversation_active = True
                    self.stop_tts()
                
                # 1. Record
                timeout_val = 10 if conversation_active else None
                status_text = "🎤 Listening... (Speak to interrupt)" if conversation_active else "🎤 Listening..."
                self._update_status(status_text, "red")

                self.was_interrupted = False
                speech_detected = record_wav(timeout=timeout_val, on_speech_start=self.stop_tts)
                self.stop_tts() 
                
                if not self.is_running: break
                
                if self.was_interrupted:
                    logger.info("🔄 Interruption detected. Discarding audio and listening again...")
                    self._update_status("🔄 Interrupted! Listening for new query...", "red")
                    continue

                if not speech_detected:
                    self._update_status("💤 Timeout (No speech)", "gray")
                    conversation_active = False
                    continue

                # 2. Transcribe
                self._update_status("📝 Transcribing...", "orange")
                user_text = transcribe_file()
                
                if not user_text:
                    self._update_status("🤷 No speech detected", "gray")
                    conversation_active = False
                    continue
                
                self._append_chat("You", user_text)
                logger.info(f"User: {user_text}")

                if not self.is_running: break

                # 3. LLM
                self._update_status("🤖 Thinking...", "purple")
                bot_text = chat_reply(user_text)
                
                if not bot_text:
                    self._update_status("🤖 Empty reply", "gray")
                    continue

                self._append_chat("Assistant", bot_text)
                logger.info(f"Assistant: {bot_text}")

                if not self.is_running: break

                # 4. TTS
                self._update_status("🗣️ Speaking...", "green")
                
                accent_name = self.settings.get("accent", "🇺🇸 US English")
                tld = self.accents_map.get(accent_name, "com")
                
                self.current_tts_process = speak(bot_text, tld=tld)
                
                self._update_status("Ready (Listening for interruption...)", "gray")
                
            except Exception as e:
                logger.error(f"Error in loop: {e}")
                traceback.print_exc()
                self._update_status(f"Error: {e}", "red")
                time.sleep(1)

        # Cleanup
        if self.wake_word_listener:
            self.wake_word_listener.cleanup()
