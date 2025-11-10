"""
Main Application - Orchestrates all components
"""

import sys
import os
import time
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.speech_recognition_engine import SpeechRecognizer
from src.speech_synthesis import SpeechSynthesizer
from src.response_engine import ResponseEngine
from src.terminal_ui import TerminalUI
from src.connectivity_manager import ConnectivityManager
from src.advanced_command_interpreter import AdvancedCommandInterpreter
from config.settings import DEBUG


class VoiceBot:
    """Main VoiceBot application"""
    
    def __init__(self):
        """Initialize VoiceBot components"""
        self.ui = TerminalUI()
        self.response_engine = ResponseEngine()
        self.speech_synthesizer = SpeechSynthesizer()
        self.command_interpreter = AdvancedCommandInterpreter()  # NEW: System control
        self.speech_recognizer = None
        self.connectivity_manager = ConnectivityManager()
        self.is_running = False
        self.demo_mode = False
    
    def initialize(self, demo_mode: bool = False) -> bool:
        """
        Initialize all components
        
        Args:
            demo_mode: If True, run in demo mode without actual audio
        
        Returns:
            True if successful, False otherwise
        """
        self.ui.display_header()
        self.ui.display_status("Initializing neural network...", "rgb(255,127,0)")
        self.demo_mode = demo_mode
        
        # Check internet connectivity
        mode = self.connectivity_manager.get_mode().upper()
        if self.connectivity_manager.is_online:
            self.ui.display_status(f"CONNECTIVITY: {mode} - Full Siri-like capabilities", "rgb(255,127,0)")
        else:
            self.ui.display_status(f"CONNECTIVITY: {mode} - System commands only", "rgb(255,127,0)")
        
        # Initialize speech recognizer with Whisper
        self.ui.display_status("Initializing Whisper speech recognition...", "rgb(255,127,0)")
        self.speech_recognizer = SpeechRecognizer(model_size="base")
        
        if self.demo_mode:
            self.ui.display_status("DEMO_MODE: Text input protocol active", "rgb(255,127,0)")
        elif not self.speech_recognizer.model:
            self.ui.display_status("WARNING: Whisper model unavailable", "rgb(255,127,0)")
            self.ui.display_status("Switching to DEMO_MODE for operation", "rgb(255,127,0)")
            self.demo_mode = True
        
        self.ui.display_status("Speech Recognition: OPERATIONAL", "rgb(255,127,0)")
        self.ui.display_status("Text-to-Speech Engine: OPERATIONAL", "rgb(255,127,0)")
        self.ui.display_status("Response Protocol: OPERATIONAL", "rgb(255,127,0)")
        print()
        
        self.ui.display_welcome()
        return True
    
    def process_input(self, user_input: str) -> bool:
        """
        Process user input and generate response
        
        Args:
            user_input: Text recognized from speech
            
        Returns:
            True if should continue, False if should exit
        """
        if not user_input:
            return True
        
        # Display what was heard
        print()
        self.ui.display_user_input(user_input)
        
        # First, try advanced command interpreter (system control)
        cmd_result = self.command_interpreter.interpret_command(user_input)
        
        if cmd_result['status'] == 'success':
            # System command was executed
            response = cmd_result['response']
        elif cmd_result['action'] != 'unknown':
            # Command matched but had an error
            response = cmd_result['response']
        else:
            # Use traditional response engine for general conversation
            response, confidence = self.response_engine.find_response(user_input)
            if DEBUG:
                print(f"[DEBUG] Confidence: {confidence:.2f}")
        
        # Handle special commands that need additional output
        if self._handle_special_commands(user_input):
            pass
        
        # Display response
        print()
        self.ui.display_response(response)
        
        # Speak response
        self.speech_synthesizer.speak(response)
        
        # Check for exit conditions
        user_lower = user_input.lower()
        if any(word in user_lower for word in ["goodbye", "bye", "exit", "quit"]):
            return False
        
        return True
    
    def _handle_special_commands(self, user_input: str) -> bool:
        """
        Handle special commands that require additional output
        
        Args:
            user_input: User input text
            
        Returns:
            True if special command was handled
        """
        user_lower = user_input.lower()
        
        # System info command
        if any(word in user_lower for word in ["system info", "system details", "computer info"]):
            print()
            self.ui.display_system_info()
            return True
        
        # Time command
        if any(word in user_lower for word in ["what time", "tell me time", "current time"]):
            print()
            self.ui.display_time()
            return True
        
        # Date command
        if any(word in user_lower for word in ["what date", "what is today", "tell me date"]):
            print()
            self.ui.display_date()
            return True
        
        # Help command
        if any(word in user_lower for word in ["help", "what can you do", "capabilities"]):
            print()
            self.ui.display_help()
            return True
        
        return False
    
    def run(self):
        """Run the VoiceBot application"""
        # Try to run normally, fallback to demo mode if Whisper unavailable
        if not self.initialize(demo_mode=False):
            self.cleanup()
            return
        
        self.is_running = True
        
        try:
            while self.is_running:
                # Get speech input
                user_input = self.speech_recognizer.listen(demo_mode=self.demo_mode)
                
                if user_input:
                    # Process input
                    should_continue = self.process_input(user_input)
                    if not should_continue:
                        break
                else:
                    print()
                    self.ui.display_error("Could not recognize speech. Please try again.")
                
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n")
            self.ui.display_status("System interrupt detected - initiating shutdown", "yellow")
        
        except Exception as e:
            print("\n")
            self.ui.display_error(f"Critical system error: {str(e)}")
            if DEBUG:
                import traceback
                traceback.print_exc()
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.is_running = False
        
        if self.speech_recognizer:
            self.speech_recognizer.cleanup()
        
        self.speech_synthesizer.stop()
        
        print("\n" + "="*60)
        self.ui.display_status("System shutdown sequence initiated", "cyan")
        print("="*60)


def main():
    """Main entry point"""
    bot = VoiceBot()
    bot.run()


if __name__ == "__main__":
    main()
