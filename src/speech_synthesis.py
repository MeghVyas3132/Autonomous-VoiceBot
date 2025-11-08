"""
Speech Synthesis - Text-to-Speech using pyttsx3
"""

import pyttsx3
import threading
from typing import Optional
from config.settings import TTS_VOICE_RATE, TTS_VOLUME


class SpeechSynthesizer:
    """Handles text-to-speech synthesis"""
    
    def __init__(self, rate: int = TTS_VOICE_RATE, volume: float = TTS_VOLUME):
        """
        Initialize the speech synthesizer
        
        Args:
            rate: Speech rate in words per minute
            volume: Volume level (0.0 to 1.0)
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        self.is_speaking = False
        
        # Set voice (prefer female voice if available)
        self._set_voice()
    
    def _set_voice(self):
        """Set a preferred voice - MALE voice for JARVIS-style assistant"""
        voices = self.engine.getProperty('voices')
        if voices:
            # Try to find a male voice
            for voice in voices:
                if 'male' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    return
            # Default to first available voice if no male voice found
            self.engine.setProperty('voice', voices[0].id)
    
    def speak(self, text: str, async_mode: bool = False) -> None:
        """
        Speak the given text
        
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
        """Synchronous speech"""
        self.is_speaking = True
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        finally:
            self.is_speaking = False
    
    def stop(self) -> None:
        """Stop current speech"""
        self.engine.stop()
        self.is_speaking = False
    
    def set_rate(self, rate: int) -> None:
        """Set speech rate"""
        self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float) -> None:
        """Set volume (0.0 to 1.0)"""
        self.engine.setProperty('volume', max(0.0, min(1.0, volume)))


# Example usage
if __name__ == "__main__":
    synthesizer = SpeechSynthesizer()
    
    test_messages = [
        "Hello! I'm your offline voice assistant.",
        "How can I help you today?",
        "The weather is nice, but I cannot tell you live weather data since I am offline."
    ]
    
    for message in test_messages:
        print(f"Speaking: {message}")
        synthesizer.speak(message)
        print()
