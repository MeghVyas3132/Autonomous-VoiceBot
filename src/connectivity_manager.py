"""
Online/Offline Mode Handler - Detect internet and provide appropriate responses
"""

import socket
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import DEBUG


class ConnectivityManager:
    """Manages online/offline mode and provides smart responses"""
    
    def __init__(self):
        """Initialize connectivity manager"""
        self.is_online = False
        self.check_connectivity()
    
    def check_connectivity(self) -> bool:
        """
        Check if internet connection is available
        
        Returns:
            True if online, False if offline
        """
        try:
            # Try to connect to Google's DNS
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            self.is_online = True
            if DEBUG:
                print("[DEBUG] Internet connection: ONLINE")
            return True
        except (socket.timeout, socket.error):
            self.is_online = False
            if DEBUG:
                print("[DEBUG] Internet connection: OFFLINE")
            return False
    
    def get_mode(self) -> str:
        """
        Get current mode
        
        Returns:
            "online" or "offline"
        """
        return "online" if self.is_online else "offline"
    
    def is_general_question(self, user_input: str) -> bool:
        """
        Detect if question is general (needs internet)
        Examples: weather, news, facts, calculations, etc.
        
        Args:
            user_input: User's input text
            
        Returns:
            True if it's a general question, False if system-specific
        """
        general_keywords = [
            "weather", "news", "stock", "convert", "translate",
            "how does", "why", "explain", "tell me about",
            "what is", "who is", "define", "search", "google",
            "calculate", "math", "currency", "bitcoin", "crypto",
            "covid", "disease", "medical", "recipe", "how to make"
        ]
        
        user_lower = user_input.lower()
        return any(keyword in user_lower for keyword in general_keywords)
    
    def is_system_command(self, user_input: str) -> bool:
        """
        Detect if it's a system command (works offline)
        
        Args:
            user_input: User's input text
            
        Returns:
            True if it's a system command
        """
        system_keywords = [
            "time", "date", "system", "info", "help", "hello",
            "goodbye", "who are you", "what can you do", "commands",
            "offline", "online", "shutdown", "status", "cpu", "memory"
        ]
        
        user_lower = user_input.lower()
        return any(keyword in user_lower for keyword in system_keywords)


# Example usage
if __name__ == "__main__":
    manager = ConnectivityManager()
    
    print(f"[SYSTEM] Current Mode: {manager.get_mode().upper()}")
    print(f"[SYSTEM] Is Online: {manager.is_online}\n")
    
    test_inputs = [
        "What time is it?",
        "What is the weather today?",
        "System info",
        "Tell me about Python",
        "How many cores do I have?"
    ]
    
    for test in test_inputs:
        is_general = manager.is_general_question(test)
        is_system = manager.is_system_command(test)
        print(f"Input: '{test}'")
        print(f"  General Question: {is_general}")
        print(f"  System Command: {is_system}\n")
