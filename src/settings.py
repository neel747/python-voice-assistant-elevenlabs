import json
import os
from .logger import logger

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "accent": "🇺🇸 US English",
    "wake_word_enabled": True
}

class SettingsManager:
    def __init__(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.load()

    def load(self):
        """Load settings from JSON file."""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    data = json.load(f)
                    self.settings.update(data)
                logger.info("✅ Settings loaded.")
            except Exception as e:
                logger.error(f"❌ Error loading settings: {e}")

    def save(self):
        """Save current settings to JSON file."""
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(self.settings, f, indent=4)
            logger.info("💾 Settings saved.")
        except Exception as e:
            logger.error(f"❌ Error saving settings: {e}")

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()
