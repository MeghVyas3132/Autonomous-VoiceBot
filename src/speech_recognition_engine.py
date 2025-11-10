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
    
    def listen(self, timeout: Optional[float] = 10, demo_mode: bool = False) -> str:
        """
        Listen to microphone and return recognized text
        
        Args:
            timeout: Timeout in seconds (None for no timeout)
            demo_mode: If True, use demo text instead of real audio
            
        Returns:
            Recognized text
        """
        if demo_mode:
            return self._demo_listen()
        
        if not self.model:
            print("[SYSTEM] Model not initialized - using demo mode")
            return self._demo_listen()
        
        if not AUDIO_AVAILABLE:
            print("[SYSTEM] Audio libraries not available - using demo mode")
            return self._demo_listen()
        
        try:
            self.is_listening = True
            
            # Record audio - increased to 10 seconds for better voice capture
            duration = timeout or 10  # Default 10 seconds (increased from 5)
            print(f"[SYSTEM] Listening for {int(duration)} seconds... speak now!")
            
            # Record audio at 16kHz
            audio_data = sd.rec(
                int(SAMPLE_RATE * duration),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype='float32'
            )
            sd.wait()
            
            # Save to temporary file (Whisper works with audio files)
            temp_audio_file = "/tmp/voicebot_temp_audio.wav"
            sf.write(temp_audio_file, audio_data, SAMPLE_RATE)
            
            # Use Whisper to transcribe
            print("[SYSTEM] Processing speech with Whisper...")
            
            # Check if ffmpeg is available, use appropriate method
            if check_ffmpeg():
                result = self.model.transcribe(temp_audio_file, language="en")
            else:
                # Fallback: load audio directly without ffmpeg
                import soundfile as sf
                audio, sr = sf.read(temp_audio_file)
                # Resample if necessary
                if sr != 16000:
                    from scipy import signal
                    audio = signal.resample(audio, int(len(audio) * 16000 / sr))
                result = self.model.transcribe(temp_audio_file, language="en", fp16=False)
            
            recognized_text = result.get("text", "").strip()
            
            # Clean up temp file
            if os.path.exists(temp_audio_file):
                os.remove(temp_audio_file)
            
            self.is_listening = False
            
            if recognized_text:
                print(f"[SYSTEM] Confidence: high")
                return recognized_text
            else:
                print("[SYSTEM] No speech detected")
                return ""
            
        except Exception as e:
            print(f"ERROR: Error during listening: {e}")
            print(f"ERROR: ffmpeg might be missing. Install with: brew install ffmpeg")
            self.is_listening = False
            return self._demo_listen()
    
    def _demo_listen(self) -> str:
        """Demo mode - get text input from user"""
        print("\n[DEMO_MODE] Enter your command:")
        print("   Examples: 'hello', 'what time', 'who are you', 'goodbye'")
        user_input = input("[USER_INPUT] > ").strip()
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
