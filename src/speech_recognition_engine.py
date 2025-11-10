"""
Speech Recognition Engine - Using OpenAI Whisper for offline recognition
"""

import os
import sys
import time
from typing import Optional

try:
    import sounddevice as sd
    import soundfile as sf
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

from config.settings import SAMPLE_RATE, AUDIO_CHUNK


def check_ffmpeg():
    """Check if ffmpeg is available"""
    import subprocess
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=2)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


class SpeechRecognizer:
    """Handles offline speech recognition using OpenAI Whisper"""
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize the speech recognizer with Whisper
        
        Args:
            model_size: Whisper model size ("tiny", "base", "small", "medium", "large")
                       "base" = ~140MB, good balance of accuracy and speed
                       "small" = ~460MB, better accuracy
                       "tiny" = ~39MB, fastest but less accurate
        """
        self.model_size = model_size
        self.model = None
        self.is_listening = False
        
        self._initialize_model()
    
    def _get_default_model_path(self) -> str:
        """Get the default model path"""
        home_dir = os.path.expanduser("~")
        model_dir = os.path.join(home_dir, ".vosk", "model-en-us")
        return model_dir
    
    def _initialize_model(self) -> bool:
        """
        Initialize the Whisper model
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if not WHISPER_AVAILABLE:
                print("ERROR: Whisper not installed")
                print("Run: pip install openai-whisper")
                return False
            
            print(f"[SYSTEM] Loading Whisper {self.model_size} model (first time may take a minute)...")
            self.model = whisper.load_model(self.model_size)
            print(f"[SYSTEM] Whisper {self.model_size} model loaded successfully")
            return True
        except Exception as e:
            print(f"ERROR: Failed to initialize Whisper: {e}")
            return False
    
    def listen(self, timeout: Optional[float] = 10, demo_mode: bool = True) -> str:
        """
        Get user input - TEXT MODE (no audio required)
        
        Args:
            timeout: Ignored (kept for compatibility)
            demo_mode: Always True (text input mode)
            
        Returns:
            User input text
        """
        # Always use text input - no ffmpeg or audio required!
        return self._demo_listen()
    
    def _demo_listen(self) -> str:
        """Text input mode - get text input from user (no audio required)"""
        print()
        user_input = input("[INPUT] > ").strip()
        return user_input
    
    def stop_listening(self):
        """Stop listening"""
        self.is_listening = False
    
    def cleanup(self):
        """Clean up all resources"""
        self.stop_listening()


# Example usage
if __name__ == "__main__":
    recognizer = SpeechRecognizer(model_size="base")
    
    if recognizer.model:
        print("[SYSTEM] Speech Recognition Ready")
        print("[SYSTEM] Say something (press Ctrl+C to exit):")
        
        try:
            while True:
                text = recognizer.listen()
                if text:
                    print(f"[RECOGNIZED] {text}\n")
                else:
                    print("[SYSTEM] Could not recognize speech\n")
        except KeyboardInterrupt:
            print("\n[SYSTEM] Shutdown sequence initiated")
        finally:
            recognizer.cleanup()
    else:
        print("[ERROR] Failed to initialize speech recognition")
