# src/app.py
import signal
import sys
import tkinter as tk
import traceback

from .logger import logger
from .settings import SettingsManager
from .gui import VoiceAssistantGUI

def _shutdown(*_):
    logger.info("👋 Bye!")
    sys.exit(0)

def main():
    # Clean exit on Ctrl+C / kill
    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    logger.info("🚀 Launching Voice Assistant (MVC)...")
    
    try:
        # 1. Initialize Settings
        settings_manager = SettingsManager()
        
        # 2. Initialize GUI
        root = tk.Tk()
        logger.info("✅ Tkinter root created.")
        
        app = VoiceAssistantGUI(root, settings_manager)
        logger.info("✅ App initialized. Entering mainloop...")
        
        root.mainloop()
        logger.info("👋 Mainloop exited.")
        
    except Exception as e:
        logger.error(f"❌ App Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
