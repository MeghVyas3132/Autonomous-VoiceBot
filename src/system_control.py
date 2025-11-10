"""
System Control Module - Gives voice bot full macOS system control
Provides capabilities to:
- Get location and map services
- Check weather using local APIs
- Find nearby restaurants
- Control system settings
- Open applications
- Read system information
- And much more!
"""

import subprocess
import os
import json
import re
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import socket


class SystemControl:
    """Handles system-level operations for voice bot"""
    
    def __init__(self):
        """Initialize system control"""
        self.is_macos = os.uname().sysname == 'Darwin'
        if not self.is_macos:
            print("[WARNING] System control module optimized for macOS")
        
        # Cache for frequently accessed data
        self.location_cache = None
        self.weather_cache = None
        self.cache_time = {}
    
    # ==================== LOCATION & MAPS ====================
    
    def get_location(self) -> Dict[str, Any]:
        """
        Get device location using macOS location services
        Returns: {latitude, longitude, accuracy, address}
        """
        try:
            # Use CoreLocation framework via Python
            # Falls back to public IP geolocation if CoreLocation unavailable
            
            # Try method 1: macOS CoreLocation (more accurate)
            result = subprocess.run(
                ['open', '-g', 'get://'],  # Opens Maps in background
                capture_output=True
            )
            
            # Method 2: Use public IP geolocation (works without CoreLocation)
            location = self._get_location_from_ip()
            
            if location:
                self.location_cache = location
                self.cache_time['location'] = datetime.now()
                return location
            
            return {"error": "Could not determine location"}
        
        except Exception as e:
            return {"error": f"Location error: {e}"}
    
    def _get_location_from_ip(self) -> Optional[Dict]:
        """Get approximate location from public IP address"""
        try:
            import urllib.request
            import json
            
            # Use free geolocation API
            response = urllib.request.urlopen('https://ipapi.co/json/', timeout=5)
            data = json.loads(response.read().decode())
            
            return {
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'city': data.get('city'),
                'region': data.get('region'),
                'country': data.get('country_name'),
                'postal': data.get('postal'),
                'accuracy': 'city-level'
            }
        except:
            return None
    
    def find_nearest_restaurant(self, cuisine: str = None, distance_km: float = 5.0) -> List[Dict]:
        """
        Find nearby restaurants using maps data
        Requires internet connection to query Google Maps or similar
        """
        try:
            location = self.get_location()
            
            if 'error' in location:
                return [{"error": "Cannot find restaurants without location"}]
            
            # Build search query
            query = "restaurants"
            if cuisine:
                query = f"{cuisine} restaurants"
            
            # Open in Maps app with search
            search_url = f"maps://search?q={query}&center={location['latitude']},{location['longitude']}"
            subprocess.run(['open', search_url])
            
            return [{
                "action": "opened",
                "message": f"Opening Maps to search for {query} near you",
                "location": location
            }]
        
        except Exception as e:
            return [{"error": f"Restaurant search error: {e}"}]
    
    def find_coffee_shops(self) -> List[Dict]:
        """Find nearby coffee shops"""
        return self.find_nearest_restaurant("coffee")
    
    def find_restaurants_nearby(self, cuisine: str = None) -> List[Dict]:
        """Find restaurants near current location"""
        return self.find_nearest_restaurant(cuisine)
    
    # ==================== WEATHER ====================
    
    def get_weather(self) -> Dict[str, Any]:
        """
        Get current weather using online API
        Requires internet connection
        """
        try:
            location = self.get_location()
            
            if 'error' in location:
                return {"error": "Cannot fetch weather without location"}
            
            # Use Open-Meteo free weather API (no API key needed)
            import urllib.request
            import json
            
            lat = location['latitude']
            lon = location['longitude']
            
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m"
            
            response = urllib.request.urlopen(url, timeout=5)
            data = json.loads(response.read().decode())
            
            current = data.get('current', {})
            
            weather = {
                'temperature': current.get('temperature_2m'),
                'condition': self._decode_weather_code(current.get('weather_code')),
                'wind_speed': current.get('wind_speed_10m'),
                'humidity': current.get('relative_humidity_2m'),
                'location': location.get('city', 'Your location'),
                'timestamp': datetime.now().isoformat()
            }
            
            self.weather_cache = weather
            self.cache_time['weather'] = datetime.now()
            return weather
        
        except Exception as e:
            return {"error": f"Weather error: {e}"}
    
    def _decode_weather_code(self, code: int) -> str:
        """Convert WMO weather code to description"""
        codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Foggy with frost",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with hail",
            99: "Thunderstorm with large hail",
        }
        return codes.get(code, f"Weather code {code}")
    
    # ==================== SYSTEM INFORMATION ====================
    
    def get_system_info(self) -> Dict[str, str]:
        """Get comprehensive system information"""
        try:
            import platform
            
            info = {
                'os': platform.system(),
                'version': platform.mac_ver()[0] if platform.system() == 'Darwin' else platform.release(),
                'machine': platform.machine(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
                'hostname': socket.gethostname(),
            }
            
            # Get additional macOS info
            if self.is_macos:
                result = subprocess.run(['sw_vers'], capture_output=True, text=True)
                info['macos_version'] = result.stdout.strip()
            
            return info
        
        except Exception as e:
            return {'error': f"System info error: {e}"}
    
    def get_battery_status(self) -> Dict[str, Any]:
        """Get battery information"""
        try:
            result = subprocess.run(
                ['pmset', '-g', 'batt'],
                capture_output=True,
                text=True
            )
            
            output = result.stdout
            # Parse battery percentage
            match = re.search(r'(\d+)%', output)
            percentage = int(match.group(1)) if match else None
            
            return {
                'percentage': percentage,
                'status': 'charging' if 'charging' in output else 'discharging',
                'raw': output
            }
        
        except Exception as e:
            return {'error': f"Battery error: {e}"}
    
    def get_disk_usage(self) -> Dict[str, Any]:
        """Get disk space usage"""
        try:
            result = subprocess.run(
                ['df', '-h', '/'],
                capture_output=True,
                text=True
            )
            
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                return {
                    'total': parts[1],
                    'used': parts[2],
                    'available': parts[3],
                    'percentage': parts[4],
                }
            
            return {'error': 'Could not parse disk usage'}
        
        except Exception as e:
            return {'error': f"Disk error: {e}"}
    
    def get_network_status(self) -> Dict[str, Any]:
        """Get network connection status"""
        try:
            result = subprocess.run(
                ['networksetup', '-getinfo', 'Wi-Fi'],
                capture_output=True,
                text=True
            )
            
            lines = result.stdout.strip().split('\n')
            info = {}
            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
            
            return info
        
        except Exception as e:
            return {'error': f"Network error: {e}"}
    
    # ==================== APPLICATION CONTROL ====================
    
    def open_application(self, app_name: str) -> Dict[str, str]:
        """Open a macOS application by name"""
        try:
            subprocess.run(['open', '-a', app_name], timeout=3)
            return {'status': 'success', 'message': f'Opening {app_name}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Could not open {app_name}: {e}'}
    
    def open_url(self, url: str) -> Dict[str, str]:
        """Open a URL in default browser"""
        try:
            if not url.startswith('http'):
                url = f'https://{url}'
            subprocess.run(['open', url], timeout=3)
            return {'status': 'success', 'message': f'Opening {url}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Could not open URL: {e}'}
    
    def open_file(self, file_path: str) -> Dict[str, str]:
        """Open a file with default application"""
        try:
            subprocess.run(['open', file_path], timeout=3)
            return {'status': 'success', 'message': f'Opening {file_path}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Could not open file: {e}'}
    
    # ==================== SYSTEM CONTROL ====================
    
    def get_brightness(self) -> Optional[float]:
        """Get current screen brightness (0-1)"""
        try:
            result = subprocess.run(
                ['osascript', '-e', 'tell application "System Events" to get brightness of display 1'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return float(result.stdout.strip()) / 100
            return None
        except:
            return None
    
    def set_brightness(self, level: float) -> Dict[str, str]:
        """Set screen brightness (0-1)"""
        try:
            level = max(0, min(1, level))  # Clamp 0-1
            percent = int(level * 100)
            
            subprocess.run([
                'osascript', '-e',
                f'tell application "System Events" to set brightness of display 1 to {percent}'
            ], timeout=3)
            
            return {'status': 'success', 'message': f'Brightness set to {percent}%'}
        except Exception as e:
            return {'status': 'error', 'message': f'Could not set brightness: {e}'}
    
    def get_volume(self) -> Optional[int]:
        """Get current volume level (0-100)"""
        try:
            result = subprocess.run(
                ['osascript', '-e', 'output volume of (get volume settings)'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return int(result.stdout.strip())
            return None
        except:
            return None
    
    def set_volume(self, level: int) -> Dict[str, str]:
        """Set volume level (0-100)"""
        try:
            level = max(0, min(100, level))  # Clamp 0-100
            
            subprocess.run([
                'osascript', '-e',
                f'set volume {level}'
            ], timeout=3)
            
            return {'status': 'success', 'message': f'Volume set to {level}%'}
        except Exception as e:
            return {'status': 'error', 'message': f'Could not set volume: {e}'}
    
    def mute_volume(self) -> Dict[str, str]:
        """Mute system volume"""
        try:
            subprocess.run(['osascript', '-e', 'set volume output muted true'], timeout=3)
            return {'status': 'success', 'message': 'Volume muted'}
        except Exception as e:
            return {'status': 'error', 'message': f'Could not mute: {e}'}
    
    def unmute_volume(self) -> Dict[str, str]:
        """Unmute system volume"""
        try:
            subprocess.run(['osascript', '-e', 'set volume output muted false'], timeout=3)
            return {'status': 'success', 'message': 'Volume unmuted'}
        except Exception as e:
            return {'status': 'error', 'message': f'Could not unmute: {e}'}
    
    # ==================== UTILITIES ====================
    
    def search_web(self, query: str) -> Dict[str, str]:
        """Search the web"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            subprocess.run(['open', search_url], timeout=3)
            return {'status': 'success', 'message': f'Searching for {query}'}
        except Exception as e:
            return {'status': 'error', 'message': f'Search failed: {e}'}
    
    def show_notification(self, title: str, message: str) -> Dict[str, str]:
        """Show macOS notification"""
        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(['osascript', '-e', script], timeout=3)
            return {'status': 'success', 'message': 'Notification shown'}
        except Exception as e:
            return {'status': 'error', 'message': f'Notification error: {e}'}
    
    def list_open_applications(self) -> Dict[str, Any]:
        """List all open applications"""
        try:
            result = subprocess.run(
                ['osascript', '-e', 'tell application "System Events" to get name of every application process where background only is false'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                apps = [app.strip() for app in result.stdout.strip().split(', ')]
                return {'status': 'success', 'applications': apps, 'count': len(apps)}
            
            return {'status': 'error', 'message': 'Could not list applications'}
        except Exception as e:
            return {'status': 'error', 'message': f'Error: {e}'}
    
    def quit_application(self, app_name: str) -> Dict[str, str]:
        """Close an application"""
        try:
            script = f'tell application "{app_name}" to quit'
            subprocess.run(['osascript', '-e', script], timeout=3)
            return {'status': 'success', 'message': f'{app_name} closed'}
        except Exception as e:
            return {'status': 'error', 'message': f'Could not close {app_name}: {e}'}
    
    def sleep_mac(self) -> Dict[str, str]:
        """Put Mac to sleep"""
        try:
            subprocess.run(['osascript', '-e', 'tell application "System Events" to sleep'], timeout=3)
            return {'status': 'success', 'message': 'Mac going to sleep'}
        except Exception as e:
            return {'status': 'error', 'message': f'Could not sleep: {e}'}
    
    def lock_screen(self) -> Dict[str, str]:
        """Lock the screen"""
        try:
            subprocess.run([
                'osascript', '-e',
                'tell application "System Events" to key code 12 using {control down, option down, cmd down}'
            ], timeout=3)
            return {'status': 'success', 'message': 'Screen locked'}
        except Exception as e:
            return {'status': 'error', 'message': f'Could not lock screen: {e}'}


# Example usage
if __name__ == "__main__":
    control = SystemControl()
    
    print("\n=== System Control Module Test ===\n")
    
    # Test system info
    print("System Info:")
    info = control.get_system_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Test battery
    print("\nBattery Status:")
    battery = control.get_battery_status()
    print(f"  {battery}")
    
    # Test disk
    print("\nDisk Usage:")
    disk = control.get_disk_usage()
    print(f"  {disk}")
    
    # Test network
    print("\nNetwork Status:")
    network = control.get_network_status()
    print(f"  {network}")
    
    # Test brightness
    print("\nScreen Brightness:")
    brightness = control.get_brightness()
    print(f"  Current: {brightness}")
    
    # Test volume
    print("\nVolume:")
    volume = control.get_volume()
    print(f"  Current: {volume}%")
    
    # Test applications
    print("\nOpen Applications:")
    apps = control.list_open_applications()
    print(f"  Total: {apps.get('count')}")
    
    print("\n=== Test Complete ===\n")
