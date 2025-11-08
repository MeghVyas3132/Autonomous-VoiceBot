"""
Configuration settings for Offline VoiceBot
"""

# Speech Recognition Settings (Whisper)
WHISPER_MODEL_SIZE = "base"  # Options: "tiny", "base", "small", "medium", "large"
SAMPLE_RATE = 16000  # Hertz
AUDIO_CHUNK = 4096   # Bytes per chunk

# Text-to-Speech Settings
TTS_VOICE_RATE = 150  # Words per minute
TTS_VOLUME = 1.0  # 0.0 to 1.0

# Terminal UI Settings
ANIMATION_SPEED = 0.05  # Seconds between frames

# Response Settings
RESPONSE_CONFIG_PATH = "data/responses.json"
CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for recognition

# Debug Mode
DEBUG = False
