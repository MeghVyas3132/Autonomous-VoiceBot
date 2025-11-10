"""
Speech Synthesis - Enhanced Text-to-Speech with Natural Prosody
Uses macOS native 'say' command with advanced settings for natural human-like speech
"""

import subprocess
import os
import sys
import threading
import time
import re
from typing import Optional

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import TTS_VOICE_RATE, TTS_VOLUME


class SpeechSynthesizer:
    """Handles text-to-speech synthesis with natural prosody and tone"""
    
    def __init__(self, rate: int = None, volume: float = TTS_VOLUME):
        """
        Initialize the speech synthesizer with natural voice settings
        
        Args:
            rate: Speech rate in words per minute (None = auto-optimized)
            volume: Volume level (0.0 to 1.0) - macOS uses 0-100 scale
        """
        # Optimized rate: 180-200 WPM is more natural than 150 (less robotic)
        self.rate = rate if rate else 190  # Default to natural conversational speed
        self.volume = int(volume * 100)  # Convert to 0-100 scale for macOS
        self.is_speaking = False
        self.process = None
        self.is_macos = os.uname().sysname == 'Darwin'
        
        if not self.is_macos:
            print("[WARNING] Not running on macOS - speech synthesis may be limited")
    
    def _add_prosody(self, text: str) -> str:
        """
        Add natural prosody markers to text
        Makes speech sound more human with pauses and emphasis
        """
        # Add natural pauses at sentence boundaries
        text = re.sub(r'([.!?])\s+', r'\1  ', text)
        
        # Add slight pause after commas for breath
        text = re.sub(r',\s+', ',  ', text)
        
        # No robotic enhancements needed - macOS Samantha handles it naturally
        return text
    
    def speak(self, text: str, async_mode: bool = False, voice_tone: str = 'natural') -> None:
        """
        Speak the given text using macOS say command with natural prosody
        
        Args:
            text: Text to speak
            async_mode: If True, speak in background thread
            voice_tone: 'natural' (default), 'fast', or 'slow'
        """
        if async_mode:
            thread = threading.Thread(target=self._speak_sync, args=(text, voice_tone))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text, voice_tone)
    
    def _speak_sync(self, text: str, voice_tone: str = 'natural') -> None:
        """
        Synchronous speech with natural prosody
        
        Voice tones:
        - 'natural': 190 WPM - Natural conversational speed
        - 'fast': 220+ WPM - Quick and energetic
        - 'slow': 140-150 WPM - Careful and deliberate
        """
        if not self.is_macos:
            print(f"[SYSTEM] Would speak: {text}")
            return
        
        self.is_speaking = True
        try:
            # Apply prosody enhancement
            enhanced_text = self._add_prosody(text)
            
            # Determine rate based on tone
            rate = self._get_rate_for_tone(voice_tone)
            
            # Build command with Samantha - optimized for natural speech
            cmd = [
                'say',
                '-r', str(rate),
                '-v', 'Samantha',  # Natural female voice
                '-a', str(self.volume),
                enhanced_text
            ]
            
            # Run the command with optimized environment
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, 'LANG': 'en_US.UTF-8'}  # UTF-8 for better audio rendering
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
                    rate = self._get_rate_for_tone(voice_tone)
                    cmd = ['say', '-r', str(rate), '-v', voice, text]
                    self.process = subprocess.Popen(cmd)
                    self.process.wait()
                    self.process = None
                    return
                except Exception:
                    continue
            
            # Last resort: use default voice
            try:
                rate = self._get_rate_for_tone(voice_tone)
                cmd = ['say', '-r', str(rate), text]
                self.process = subprocess.Popen(cmd)
                self.process.wait()
                self.process = None
            except Exception as e2:
                print(f"[ERROR] All speech synthesis attempts failed: {e2}")
        finally:
            self.is_speaking = False
    
    def _get_rate_for_tone(self, voice_tone: str) -> int:
        """
        Get appropriate speech rate for the given tone
        
        Natural human speech rates:
        - 140-180 WPM: Slow, careful (ideal for technical info)
        - 180-220 WPM: Normal conversational (most natural)
        - 220-300 WPM: Fast, energetic (for quick responses)
        """
        rates = {
            'slow': 150,           # Careful, deliberate speech
            'natural': 190,        # Normal conversational (OPTIMAL)
            'fast': 240,           # Quick, energetic
            'conversational': 190,
            'formal': 170,
            'casual': 210
        }
        return rates.get(voice_tone, self.rate or 190)
    
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
        """Set speech rate in WPM"""
        self.rate = max(100, min(400, rate))  # Clamp between 100-400 WPM
    
    def set_volume(self, volume: float) -> None:
        """Set volume (0.0 to 1.0)"""
        self.volume = int(max(0.0, min(1.0, volume)) * 100)
    
    def speak_with_emphasis(self, text: str, emphasized_words: list = None) -> None:
        """
        Speak text with emphasis on specific words
        Simulated through pauses and pacing changes
        
        Args:
            text: Text to speak
            emphasized_words: List of words to emphasize
        """
        if not emphasized_words:
            self.speak(text)
            return
        
        # Create enhanced text with pauses before emphasized words
        enhanced = text
        for word in emphasized_words:
            # Add pause before emphasized words (makes them stand out)
            enhanced = enhanced.replace(word, f" {word}")
        
        self.speak(enhanced, voice_tone='natural')


# Example usage and testing
if __name__ == "__main__":
    synthesizer = SpeechSynthesizer()
    
    print("\n" + "="*60)
    print("NATURAL VOICE SYNTHESIS TEST")
    print("="*60 + "\n")
    
    # Test 1: Natural speed (conversational)
    print("[TEST 1] Natural Speed - Conversational (190 WPM)")
    print("Message: 'Hello! I am your voice assistant. I can help you with anything you need.'")
    synthesizer.speak(
        "Hello! I am your voice assistant. I can help you with anything you need.",
        voice_tone='natural'
    )
    print("✓ Spoken\n")
    time.sleep(1)
    
    # Test 2: Fast speed (energetic)
    print("[TEST 2] Fast Speed - Energetic (240 WPM)")
    print("Message: 'This is faster speech. Much more energetic and quick.'")
    synthesizer.speak(
        "This is faster speech. Much more energetic and quick.",
        voice_tone='fast'
    )
    print("✓ Spoken\n")
    time.sleep(1)
    
    # Test 3: Slow speed (deliberate)
    print("[TEST 3] Slow Speed - Deliberate (150 WPM)")
    print("Message: 'This is slower speech. Perfect for important information.'")
    synthesizer.speak(
        "This is slower speech. Perfect for important information.",
        voice_tone='slow'
    )
    print("✓ Spoken\n")
    time.sleep(1)
    
    # Test 4: With prosody (pauses)
    print("[TEST 4] With Prosody - Natural Pauses")
    print("Message: 'I can speak with pauses, for emphasis. This sounds more natural.'")
    synthesizer.speak(
        "I can speak with pauses, for emphasis. This sounds more natural.",
        voice_tone='natural'
    )
    print("✓ Spoken\n")
    
    print("="*60)
    print("All tests completed!")
    print("="*60 + "\n")

