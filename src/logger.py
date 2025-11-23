import logging
import sys
import os

def setup_logger(name: str = "VoiceAssistant", log_file: str = "app.log", level=logging.INFO) -> logging.Logger:
    """
    Configures and returns a logger with console and file handlers.
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding handlers multiple times if setup_logger is called repeatedly
    if logger.hasHandlers():
        return logger

    # Formatters
    # Console: simpler format
    console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
    # File: detailed format
    file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] %(message)s')

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    # File Handler
    try:
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Failed to set up file logging: {e}")

    return logger

# Create a default logger instance for easy import
logger = setup_logger()
