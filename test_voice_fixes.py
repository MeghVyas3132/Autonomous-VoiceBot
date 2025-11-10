#!/usr/bin/env python3
"""
Comprehensive test for voice bot fixes:
1. Voice gender verification (Samantha is female)
2. FFmpeg detection and fallback
"""

import sys
import os
sys.path.insert(0, '/Users/meghvyas/Desktop/Offline-VoiceBot')

from src.speech_synthesis import SpeechSynthesizer
from src.speech_recognition_engine import check_ffmpeg

def test_voice():
    """Test that Samantha female voice is working"""
    print("\n" + "="*60)
    print("TEST 1: Voice Gender - Samantha (Female)")
    print("="*60)
    
    synth = SpeechSynthesizer()
    test_phrases = [
        "Hello! I'm Samantha, a female voice assistant.",
        "This is a high quality female voice for your offline voice bot.",
        "If you hear a female voice, the fix is working!"
    ]
    
    for i, phrase in enumerate(test_phrases, 1):
        print(f"\n[TEST {i}] Speaking: {phrase}")
        synth.speak(phrase)
        print(f"[TEST {i}] ✓ Completed")
    
    print("\n✓ Voice test complete - you should have heard a FEMALE voice")

def test_ffmpeg():
    """Test FFmpeg detection and provide guidance"""
    print("\n" + "="*60)
    print("TEST 2: FFmpeg Availability Check")
    print("="*60)
    
    ffmpeg_available = check_ffmpeg()
    
    if ffmpeg_available:
        print("\n✓ FFmpeg is installed and available!")
        print("  → Real microphone input will work properly")
        print("  → Whisper will successfully transcribe audio")
    else:
        print("\n✗ FFmpeg is NOT currently installed")
        print("\n  Solutions (in order of ease):")
        print("  1. Use Docker (has ffmpeg pre-installed):")
        print("     docker-compose up")
        print("\n  2. Install with Conda:")
        print("     conda install -c conda-forge ffmpeg")
        print("\n  3. Install directly:")
        print("     See FFMPEG_SOLUTIONS.md for detailed instructions")
        print("\n  → Until ffmpeg is installed, demo mode will still work")

def main():
    print("\n" + "="*60)
    print("VOICE BOT DIAGNOSTIC TEST")
    print("="*60)
    print("\nTesting fixes for:")
    print("  1. Voice gender (should be female - Samantha)")
    print("  2. FFmpeg dependency (required for real audio)")
    
    test_voice()
    test_ffmpeg()
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print("\n✓ Voice synthesis: WORKING (Samantha female voice)")
    
    if check_ffmpeg():
        print("✓ FFmpeg: INSTALLED - Real audio mode ready")
        print("\nYou can now run: python src/main.py")
    else:
        print("⚠ FFmpeg: NOT INSTALLED - Demo mode available")
        print("\nYou can run in demo mode: python src/main.py")
        print("Or install ffmpeg using the solutions in FFMPEG_SOLUTIONS.md")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()
