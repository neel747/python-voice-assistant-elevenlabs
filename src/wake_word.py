import pvporcupine
import pvrecorder
import os
from .logger import logger
from .config import PICOVOICE_ACCESS_KEY, WAKE_WORD_MODEL_PATH

class WakeWordListener:
    def __init__(self):
        self.access_key = PICOVOICE_ACCESS_KEY
        self.porcupine = None
        self.recorder = None
        self.keyword_name = "Jarvis" # Default
        
        if not self.access_key:
            logger.warning("⚠️ No PICOVOICE_ACCESS_KEY found. Wake word will not work.")
            return

        try:
            if WAKE_WORD_MODEL_PATH and os.path.exists(WAKE_WORD_MODEL_PATH):
                logger.info(f"📂 Loading custom wake word model: {WAKE_WORD_MODEL_PATH}")
                self.porcupine = pvporcupine.create(
                    access_key=self.access_key,
                    keyword_paths=[WAKE_WORD_MODEL_PATH]
                )
                self.keyword_name = os.path.basename(WAKE_WORD_MODEL_PATH)
            else:
                # Use default
                self.porcupine = pvporcupine.create(
                    access_key=self.access_key,
                    keywords=['jarvis'] 
                )
            
            self.recorder = pvrecorder.PvRecorder(
                device_index=-1, 
                frame_length=self.porcupine.frame_length
            )
            logger.info(f"✅ Wake Word Listener initialized (Keyword: {self.keyword_name})")
            
        except Exception as e:
            logger.error(f"❌ Error initializing Porcupine: {e}")

    def listen(self):
        """
        Blocks until the wake word is detected.
        Returns True if detected, False if stopped/error.
        """
        if not self.porcupine or not self.recorder:
            logger.error("❌ Wake word listener not initialized properly.")
            return False

        logger.info(f"👂 Listening for wake word '{self.keyword_name}'...")
        self.recorder.start()
        
        try:
            while True:
                pcm = self.recorder.read()
                result = self.porcupine.process(pcm)
                
                if result >= 0:
                    logger.info("⚡ Wake word detected!")
                    return True
                    
        except KeyboardInterrupt:
            return False
        except Exception as e:
            logger.error(f"❌ Error in wake word loop: {e}")
            return False
        finally:
            self.recorder.stop()

    def cleanup(self):
        if self.recorder:
            self.recorder.delete()
        if self.porcupine:
            self.porcupine.delete()
