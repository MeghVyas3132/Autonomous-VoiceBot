"""
Advanced Command Interpreter - Maps voice commands to system control functions
Understands natural language and executes actual system operations
"""

import re
from typing import Dict, Any, Tuple, Optional
from src.system_control import SystemControl


class AdvancedCommandInterpreter:
    """Interprets voice commands and executes system operations"""
    
    def __init__(self):
        """Initialize command interpreter"""
        self.system_control = SystemControl()
        self.command_patterns = self._build_command_patterns()
    
    def _build_command_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Build regex patterns for command recognition"""
        return {
            # Location & Maps
            'location': {
                'patterns': [
                    r'where am i',
                    r'current location',
                    r'my location',
                    r'what is my location'
                ],
                'action': 'get_location',
                'description': 'Get your current location'
            },
            
            # Restaurants & Nearby
            'restaurants': {
                'patterns': [
                    r'find (me )?nearby restaurants',
                    r'restaurants near( by| here)?',
                    r'find (me )?a restaurant',
                    r'where are restaurants',
                    r'any restaurants nearby'
                ],
                'action': 'find_restaurants_nearby',
                'description': 'Find nearby restaurants'
            },
            'coffee': {
                'patterns': [
                    r'find coffee',
                    r'coffee shops',
                    r'where is.*coffee',
                    r'nearest coffee'
                ],
                'action': 'find_coffee_shops',
                'description': 'Find nearby coffee shops'
            },
            
            # Weather
            'weather': {
                'patterns': [
                    r"what's the weather",
                    r'weather here',
                    r'current weather',
                    r'is it raining',
                    r'temperature outside',
                    r'how is the weather'
                ],
                'action': 'get_weather',
                'description': 'Get current weather'
            },
            
            # System Information
            'system_info': {
                'patterns': [
                    r'system (information|info|details)',
                    r'tell me about (my )?system',
                    r'system status',
                    r'computer info'
                ],
                'action': 'get_system_info',
                'description': 'Get system information'
            },
            'battery': {
                'patterns': [
                    r'battery (status|level|percentage)',
                    r'how much battery',
                    r'battery (left|remaining)',
                    r'battery percentage'
                ],
                'action': 'get_battery_status',
                'description': 'Check battery status'
            },
            'disk': {
                'patterns': [
                    r'disk (usage|space|information)',
                    r'how much storage',
                    r'storage (used|available)',
                    r'disk space'
                ],
                'action': 'get_disk_usage',
                'description': 'Check disk usage'
            },
            'network': {
                'patterns': [
                    r'network (status|information)',
                    r'internet (status|connection)',
                    r'wifi (status|connection)',
                    r'network info'
                ],
                'action': 'get_network_status',
                'description': 'Check network status'
            },
            
            # Brightness Control
            'brightness': {
                'patterns': [
                    r'(get|check|what is) (the )?brightness',
                    r'how (bright|dim)',
                    r'current brightness'
                ],
                'action': 'get_brightness',
                'description': 'Get brightness level'
            },
            'set_brightness': {
                'patterns': [
                    r'(set|change|adjust) brightness (to )?(\d+)',
                    r'brightness (\d+)',
                    r'(brighten|dim) (to )?(\d+)'
                ],
                'action': 'set_brightness',
                'extract_param': 'last_number',
                'description': 'Set brightness level'
            },
            
            # Volume Control
            'volume': {
                'patterns': [
                    r'(get|check|what is) (the )?volume',
                    r'volume level',
                    r'current volume'
                ],
                'action': 'get_volume',
                'description': 'Get volume level'
            },
            'set_volume': {
                'patterns': [
                    r'(set|change|adjust) volume (to )?(\d+)',
                    r'volume (\d+)',
                    r'(louder|quieter|increase|decrease) volume',
                    r'volume (up|down)'
                ],
                'action': 'set_volume',
                'extract_param': 'last_number',
                'description': 'Set volume level'
            },
            'mute': {
                'patterns': [
                    r'(mute|silence)',
                    r'mute (the )?sound',
                    r'mute audio'
                ],
                'action': 'mute_volume',
                'description': 'Mute volume'
            },
            'unmute': {
                'patterns': [
                    r'unmute',
                    r'unmute (the )?sound'
                ],
                'action': 'unmute_volume',
                'description': 'Unmute volume'
            },
            
            # Applications
            'open_app': {
                'patterns': [
                    r'(open|launch|start) (\w+)',
                    r'open (\w+) (application|app)',
                    r'start (\w+)'
                ],
                'action': 'open_application',
                'extract_param': 'app_name',
                'description': 'Open an application'
            },
            'close_app': {
                'patterns': [
                    r'(close|quit|exit) (\w+)',
                    r'close (\w+) (application|app)',
                    r'exit (\w+)'
                ],
                'action': 'quit_application',
                'extract_param': 'app_name',
                'description': 'Close an application'
            },
            'list_apps': {
                'patterns': [
                    r'(list|show|what are) (open )?applications',
                    r'(list|show) running (apps|applications)',
                    r'what apps are open'
                ],
                'action': 'list_open_applications',
                'description': 'List open applications'
            },
            
            # URLs & Search
            'open_url': {
                'patterns': [
                    r'(open|go to|visit) (.+\..+)',
                    r'open (.+\.com)',
                    r'go to (.+)'
                ],
                'action': 'open_url',
                'extract_param': 'url',
                'description': 'Open a URL'
            },
            'search': {
                'patterns': [
                    r'(search for|search|google) (.+)',
                    r'(find|look for|look up) (.+)',
                    r'search (.+) on google'
                ],
                'action': 'search_web',
                'extract_param': 'search_query',
                'description': 'Search the web'
            },
            
            # System Control
            'sleep': {
                'patterns': [
                    r'(sleep|go to sleep)',
                    r'put mac to sleep',
                    r'mac sleep'
                ],
                'action': 'sleep_mac',
                'description': 'Put Mac to sleep'
            },
            'lock': {
                'patterns': [
                    r'(lock|lock screen)',
                    r'lock (the )?screen',
                    r'lock mac'
                ],
                'action': 'lock_screen',
                'description': 'Lock the screen'
            }
        }
    
    def interpret_command(self, text: str) -> Dict[str, Any]:
        """
        Interpret voice command and execute corresponding action
        Returns: {action, result, status, response}
        """
        text_lower = text.lower().strip()
        
        # Try to match command patterns
        for cmd_name, cmd_config in self.command_patterns.items():
            for pattern in cmd_config['patterns']:
                match = re.search(pattern, text_lower, re.IGNORECASE)
                if match:
                    return self._execute_command(cmd_name, cmd_config, text, match)
        
        # No command matched
        return {
            'action': 'unknown',
            'status': 'unmatched',
            'response': 'I did not recognize that command. Try asking about location, weather, battery, or system information.',
            'suggestions': [
                'Where am I?',
                'What is the weather?',
                'Check battery status',
                'System information',
                'Find nearby restaurants'
            ]
        }
    
    def _execute_command(self, cmd_name: str, cmd_config: Dict, text: str, match) -> Dict[str, Any]:
        """Execute a matched command"""
        try:
            action_name = cmd_config['action']
            
            # Get the action method from system_control
            if not hasattr(self.system_control, action_name):
                return {
                    'action': cmd_name,
                    'status': 'error',
                    'response': f'Command {action_name} not implemented'
                }
            
            action_method = getattr(self.system_control, action_name)
            
            # Extract parameters if needed
            params = {}
            if 'extract_param' in cmd_config:
                param_name = cmd_config['extract_param']
                
                if param_name == 'last_number':
                    # Extract last number from command
                    numbers = re.findall(r'\d+', text_lower)
                    if numbers:
                        params['level'] = int(numbers[-1])
                
                elif param_name == 'app_name':
                    # Extract application name
                    for group in match.groups():
                        if group and group not in ['open', 'launch', 'start', 'close', 'quit', 'exit', 'application', 'app']:
                            params['app_name'] = group
                            break
                
                elif param_name == 'url':
                    # Extract URL
                    urls = re.findall(r'https?://\S+|[\w\-.]+\.\w{2,}', text)
                    if urls:
                        params['url'] = urls[0]
                
                elif param_name == 'search_query':
                    # Extract search query
                    # Remove the command words
                    query = text_lower
                    for pattern in cmd_config['patterns']:
                        query = re.sub(pattern, '', query, flags=re.IGNORECASE)
                    query = query.strip()
                    if query:
                        params['query'] = query
                    else:
                        params['query'] = user_input  # Use original text if extraction failed
            
            # Execute the action
            result = action_method(**params) if params else action_method()
            
            # Format response
            response = self._format_response(cmd_name, result)
            
            return {
                'action': cmd_name,
                'status': 'success',
                'result': result,
                'response': response
            }
        
        except Exception as e:
            return {
                'action': cmd_name,
                'status': 'error',
                'response': f'Error executing command: {str(e)}',
                'error': str(e)
            }
    
    def _format_response(self, cmd_name: str, result: Any) -> str:
        """Format system control result into a natural language response"""
        
        if isinstance(result, dict):
            if 'error' in result:
                return f"Error: {result['error']}"
            
            if cmd_name == 'location':
                return f"You are in {result.get('city', 'unknown')}, {result.get('region', 'unknown')}. Coordinates: {result.get('latitude', 'N/A')}, {result.get('longitude', 'N/A')}"
            
            elif cmd_name == 'weather':
                temp = result.get('temperature')
                condition = result.get('condition')
                location = result.get('location', 'your area')
                return f"In {location}, it's {temp}°C and {condition}. Wind speed: {result.get('wind_speed')} km/h. Humidity: {result.get('humidity')}%"
            
            elif cmd_name == 'battery':
                return f"Battery: {result.get('percentage')}%, Status: {result.get('status')}"
            
            elif cmd_name == 'disk':
                return f"Disk usage - Used: {result.get('used')}, Available: {result.get('available')}, Total: {result.get('total')}"
            
            elif cmd_name == 'network':
                return f"Network status: Connected to {result.get('SSID', 'unknown network')}"
            
            elif cmd_name == 'list_apps':
                count = result.get('count', 0)
                return f"You have {count} applications open"
            
            elif 'status' in result and result['status'] == 'success':
                return result.get('message', 'Command executed successfully')
            
            else:
                return str(result)
        
        return str(result)
    
    def get_help(self) -> str:
        """Get all available commands"""
        help_text = "Available commands:\n\n"
        
        categories = {
            'Location & Maps': ['location', 'restaurants', 'coffee'],
            'Weather': ['weather'],
            'System Info': ['system_info', 'battery', 'disk', 'network'],
            'Controls': ['brightness', 'set_brightness', 'volume', 'set_volume', 'mute', 'unmute'],
            'Applications': ['open_app', 'close_app', 'list_apps'],
            'Web': ['open_url', 'search'],
            'System': ['sleep', 'lock']
        }
        
        for category, cmds in categories.items():
            help_text += f"\n{category}:\n"
            for cmd in cmds:
                if cmd in self.command_patterns:
                    desc = self.command_patterns[cmd]['description']
                    help_text += f"  • {desc}\n"
        
        return help_text


# Example usage and testing
if __name__ == "__main__":
    interpreter = AdvancedCommandInterpreter()
    
    # Test commands
    test_commands = [
        "where am i",
        "what's the weather",
        "find nearby restaurants",
        "coffee shops",
        "battery status",
        "system information",
        "set volume to 50",
        "brightness to 80",
        "open chrome",
        "search for python programming",
        "lock screen",
        "mute"
    ]
    
    print("\n=== Advanced Command Interpreter Test ===\n")
    
    for cmd in test_commands:
        print(f"Command: '{cmd}'")
        result = interpreter.interpret_command(cmd)
        print(f"Action: {result['action']}")
        print(f"Status: {result['status']}")
        print(f"Response: {result['response']}")
        print()
    
    print("\n=== Available Commands ===\n")
    print(interpreter.get_help())
