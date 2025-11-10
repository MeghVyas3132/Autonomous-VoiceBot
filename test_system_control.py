#!/usr/bin/env python3
"""
Test script for advanced system control commands
Try out your voice bot's new macOS system control capabilities!
"""

import sys
import os
sys.path.insert(0, '/Users/meghvyas/Desktop/Offline-VoiceBot')

from src.advanced_command_interpreter import AdvancedCommandInterpreter


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60 + "\n")


def test_command(interpreter, command):
    """Test a single command"""
    print(f"👤 Command: \"{command}\"")
    result = interpreter.interpret_command(command)
    print(f"🤖 Response: {result['response']}")
    print(f"⚙️  Status: {result['status']}")
    if result['status'] == 'success' and 'result' in result:
        # Show actual data for informational commands
        if isinstance(result['result'], dict) and any(k in result['result'] for k in ['percentage', 'temperature', 'count']):
            import json
            print(f"📊 Data: {json.dumps(result['result'], indent=2)[:200]}")
    print()


def main():
    """Run interactive system control tests"""
    interpreter = AdvancedCommandInterpreter()
    
    print("\n" + "="*60)
    print("  SYSTEM CONTROL COMMAND TEST SUITE")
    print("  Full macOS Integration Demo")
    print("="*60)
    
    # System Information Tests
    print_section("1️⃣  SYSTEM INFORMATION")
    test_command(interpreter, "battery status")
    test_command(interpreter, "disk usage")
    test_command(interpreter, "network status")
    test_command(interpreter, "system information")
    
    # Location & Weather Tests (requires internet)
    print_section("2️⃣  LOCATION & WEATHER (requires internet)")
    test_command(interpreter, "where am i")
    test_command(interpreter, "what's the weather")
    test_command(interpreter, "find nearby restaurants")
    test_command(interpreter, "coffee shops near me")
    
    # Control Tests
    print_section("3️⃣  CONTROL TESTS (non-destructive)")
    test_command(interpreter, "get brightness")
    test_command(interpreter, "current volume")
    test_command(interpreter, "list open applications")
    
    # Application Tests
    print_section("4️⃣  APPLICATION COMMANDS (examples)")
    test_command(interpreter, "open calculator")  # Safe test app
    test_command(interpreter, "list applications")
    
    # Web Tests
    print_section("5️⃣  WEB COMMANDS")
    test_command(interpreter, "search for python programming")
    test_command(interpreter, "open github.com")
    
    # Interactive Mode
    print_section("6️⃣  INTERACTIVE MODE")
    print("Try your own commands! (type 'help' for all commands, 'quit' to exit)\n")
    
    while True:
        try:
            user_input = input("🎤 Your command: ").strip()
            
            if user_input.lower() == 'quit':
                print("Exiting... Goodbye! 👋\n")
                break
            
            if user_input.lower() == 'help':
                print(interpreter.get_help())
                continue
            
            if not user_input:
                continue
            
            print()
            test_command(interpreter, user_input)
        
        except KeyboardInterrupt:
            print("\n\nExiting... Goodbye! 👋\n")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    main()
