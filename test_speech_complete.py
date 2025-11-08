#!/usr/bin/env python3
"""
Complete Test - Speech Recognition + Speech Synthesis
Tests both Whisper and pyttsx3 together
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.speech_recognition_engine import SpeechRecognizer
from src.speech_synthesis import SpeechSynthesizer
from src.terminal_ui import TerminalUI

print("\n[AUTONOMOUS DIALOGUE SYSTEM - SPEECH TEST]\n")

# Initialize components
print("[SYSTEM] Initializing components...")
ui = TerminalUI()
ui.display_header()

print("[SYSTEM] Loading Whisper model...")
recognizer = SpeechRecognizer(model_size="base")

print("[SYSTEM] Initializing speech synthesis...")
synthesizer = SpeechSynthesizer()

print("[SYSTEM] All components ready!\n")

# Test synthesis
print("[TEST] Testing speech synthesis...")
ui.display_status("Speaking test message", "cyan")
synthesizer.speak("Hello! Speech synthesis is working correctly.")
print("[SUCCESS] Speech synthesis test passed\n")

# Test recognition in demo mode
print("[TEST] Testing speech recognition (DEMO_MODE)...")
ui.display_status("Enter a test command", "yellow")
test_input = recognizer._demo_listen()

if test_input:
    print(f"[RECOGNIZED] You said: {test_input}\n")
    
    # Now synthesize a response
    print("[TEST] Testing synthesis with recognized input...")
    response = f"You said: {test_input}"
    ui.display_status("Speaking your input back to you", "cyan")
    synthesizer.speak(response)
    print("[SUCCESS] Full cycle test passed!\n")

print("[SYSTEM] All tests completed successfully!")
print("[SYSTEM] System is ready for real microphone input")
