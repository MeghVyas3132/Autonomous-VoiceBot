"""
Response Engine - Handles pattern matching and response generation
"""

import json
import random
import re
from pathlib import Path
from typing import Tuple, Optional


class ResponseEngine:
    """Manages hardcoded responses and pattern matching"""
    
    def __init__(self, responses_path: str = "data/responses.json"):
        """
        Initialize the response engine with responses from JSON file
        
        Args:
            responses_path: Path to the responses JSON file
        """
        self.responses_path = Path(responses_path)
        self.responses_db = self._load_responses()
    
    def _load_responses(self) -> dict:
        """Load responses from JSON file"""
        try:
            with open(self.responses_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Responses file not found at {self.responses_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.responses_path}")
            return {}
    
    def find_response(self, user_input: str) -> Tuple[str, float]:
        """
        Find a matching response for the user input
        
        Args:
            user_input: The recognized speech text
            
        Returns:
            Tuple of (response, confidence_score)
        """
        user_input = user_input.lower().strip()
        best_match = None
        best_confidence = 0.0
        
        # Search through all categories
        for category, data in self.responses_db.items():
            if category == "default":
                continue
            
            patterns = data.get("patterns", [])
            responses = data.get("responses", [])
            
            if not responses:
                continue
            
            # Check each pattern
            for pattern in patterns:
                confidence = self._calculate_similarity(user_input, pattern)
                
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_match = random.choice(responses)
        
        # If no good match, use default response
        if best_confidence < 0.3:
            default_responses = self.responses_db.get("default", {}).get("responses", [])
            if default_responses:
                return random.choice(default_responses), 0.1
        
        return best_match or "I'm not sure how to respond to that.", best_confidence
    
    def _calculate_similarity(self, user_text: str, pattern: str) -> float:
        """
        Calculate similarity between user input and pattern
        Simple substring and word matching
        
        Args:
            user_text: User's input
            pattern: Pattern to match against
            
        Returns:
            Confidence score between 0 and 1
        """
        user_words = set(user_text.split())
        pattern_words = set(pattern.split())
        
        # If pattern is a substring of user input
        if pattern in user_text:
            return 0.9
        
        # If any word from pattern is in user input
        if pattern_words & user_words:
            return 0.7
        
        # Check for partial matches
        for word in pattern_words:
            if word in user_text:
                return 0.6
        
        return 0.0
    
    def add_category(self, category_name: str, patterns: list, responses: list):
        """
        Add a new response category dynamically
        
        Args:
            category_name: Name of the category
            patterns: List of patterns to match
            responses: List of responses for this category
        """
        self.responses_db[category_name] = {
            "patterns": patterns,
            "responses": responses
        }
    
    def reload_responses(self):
        """Reload responses from the JSON file"""
        self.responses_db = self._load_responses()


# Example usage
if __name__ == "__main__":
    engine = ResponseEngine()
    
    test_inputs = [
        "hello there",
        "what time is it",
        "who are you",
        "tell me a joke",
        "goodbye"
    ]
    
    for test in test_inputs:
        response, confidence = engine.find_response(test)
        print(f"Input: '{test}'")
        print(f"Response: '{response}'")
        print(f"Confidence: {confidence:.2f}\n")
