"""
Speech Synthesis - Text-to-Speech using macOS native 'say' command for Siri voice
"""

import subprocess
import os
import threading
import time
from typing import Optional
from config.settings import TTS_VOICE_RATE, TTS_VOLUME


class SpeechSynthesizer:
    """Handles text-to-speech synthesis using macOS native say command"""
    
    def __init__(self, rate: int = TTS_VOICE_RATE, volume: float = TTS_VOLUME):
        """
        Initialize the speech synthesizer
        
        Args:
            rate: Speech rate in words per minute
            volume: Volume level (0.0 to 1.0) - macOS uses 0-100 scale
        """
        self.rate = rate
        self.volume = int(volume * 100)  # Convert to 0-100 scale for macOS
        self.is_speaking = False
        self.process = None
        self.is_macos = os.uname().sysname == 'Darwin'
        
        if not self.is_macos:
            print("[WARNING] Not running on macOS - speech synthesis may be limited")
    
    def speak(self, text: str, async_mode: bool = False) -> None:
        """
        Speak the given text using macOS say command
        
        Args:
            text: Text to speak
            async_mode: If True, speak in background thread
        """
        if async_mode:
            thread = threading.Thread(target=self._speak_sync, args=(text,))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text)
    
    def _speak_sync(self, text: str) -> None:
        """Synchronous speech using macOS say command"""
        if not self.is_macos:
            print(f"[SYSTEM] Would speak: {text}")
            return
        
        self.is_speaking = True
        try:
            # Build command with Samantha - high-quality female voice
            cmd = [
                'say',
                '-r', str(self.rate),
                '-v', 'Samantha',  # High-quality female voice (confirmed on macOS)
                '-a', str(self.volume),
                text
            ]
            
            # Run the command
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for it to complete
            self.process.wait()
            self.process = None
            
        except Exception as e:
            print(f"[ERROR] Speech synthesis error: {e}")
            # Fallback to alternative female voices if Samantha fails
            alt_voices = ['Kathy', 'Shelley', 'Flo']
            for voice in alt_voices:
                try:
                    cmd = ['say', '-r', str(self.rate), '-v', voice, text]
                    self.process = subprocess.Popen(cmd)
                    self.process.wait()
                    self.process = None
                    return
                except Exception:
                    continue
            
            # Last resort: use default voice
            try:
                cmd = ['say', '-r', str(self.rate), text]
                self.process = subprocess.Popen(cmd)
                self.process.wait()
                self.process = None
            except Exception as e2:
                print(f"[ERROR] All speech synthesis attempts failed: {e2}")
        finally:
            self.is_speaking = False
    
    def stop(self) -> None:
        """Stop current speech"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=1)
            except:
                pass
            self.process = None
        self.is_speaking = False
    
    def set_rate(self, rate: int) -> None:
        """Set speech rate"""
        self.rate = rate
    
    def set_volume(self, volume: float) -> None:
        """Set volume (0.0 to 1.0)"""
        self.volume = int(max(0.0, min(1.0, volume)) * 100)


# Example usage
if __name__ == "__main__":
    synthesizer = SpeechSynthesizer()
    
    test_messages = [
        "Hello! I'm your voice assistant.",
        "Using macOS native Siri voice.",
        "This sounds much more natural!"
    ]
    
    print("[TEST] Testing speech synthesis with macOS say command\n")
    for message in test_messages:
        print(f"Speaking: {message}")
        synthesizer.speak(message)
        time.sleep(0.5)
        print()


