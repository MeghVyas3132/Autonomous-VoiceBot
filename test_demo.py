#!/usr/bin/env python3
"""
Quick demo test script - AUTONOMOUS DIALOGUE SYSTEM
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.response_engine import ResponseEngine
from src.speech_synthesis import SpeechSynthesizer
from src.terminal_ui import TerminalUI
import time

def test_demo():
    """Test the VoiceBot components"""
    
    print("\n" + "="*60)
    print("AUTONOMOUS DIALOGUE SYSTEM - DEMO TEST")
    print("="*60 + "\n")
    
    # Initialize components
    ui = TerminalUI()
    response_engine = ResponseEngine()
    speech_synthesizer = SpeechSynthesizer()
    
    ui.display_header()
    print("[SYSTEM] All components initialized!\n")
    
    # Test cases
    test_inputs = [
        "hello there",
        "what time is it",
        "who are you",
        "system info",
        "goodbye"
    ]
    
    for user_input in test_inputs:
        print("\n" + "="*60)
        
        # Show listening
        ui.show_listening_animation(0.8)
        time.sleep(0.3)
        
        # Display user input
        ui.display_user_input(user_input)
        time.sleep(0.3)
        
        # Show processing
        ui.show_processing_animation(0.6)
        time.sleep(0.3)
        
        # Get response
        response, confidence = response_engine.find_response(user_input)
        
        # Handle special commands
        if "system info" in user_input.lower():
            ui.display_system_info()
            time.sleep(0.5)
        elif "time" in user_input.lower():
            ui.display_time()
            time.sleep(0.5)
        
        # Display response
        ui.display_response(response)
        time.sleep(0.3)
        
        # Show speaking
        ui.show_speaking_animation(0.8)
        time.sleep(0.3)
        
        # Speak response
        print("[SYSTEM] Speaking... (muted in demo)")
        # speech_synthesizer.speak(response)  # Uncomment to actually speak
        
        time.sleep(0.5)
        
        if "goodbye" in user_input.lower() or "bye" in user_input.lower():
            break
    
    print("\n" + "="*60)
    print("[SYSTEM] Demo execution completed successfully")
    print("="*60 + "\n")

if __name__ == "__main__":
    test_demo()
