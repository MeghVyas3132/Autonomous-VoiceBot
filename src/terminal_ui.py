"""
Terminal UI - JARVIS-style Sci-Fi Interface with Futuristic Animations
"""

import time
import os
import sys
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.layout import Layout
from rich.table import Table
import platform


class TerminalUI:
    """Handles all terminal display and animations"""
    
    def __init__(self):
        """Initialize the terminal UI"""
        self.console = Console()
        self.system_online = True
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def display_header(self):
        """Display JARVIS-style header with sci-fi theme"""
        self.clear_screen()
        
        # JARVIS-style header
        header = """
        [NEURAL NETWORK INITIALIZED]
        ==========================================
        
          AUTONOMOUS DIALOGUE INTERFACE
          Version 1.0 - OFFLINE MODE ACTIVE
          
        ==========================================
        [SYSTEMS ONLINE - ALL DIAGNOSTICS NOMINAL]
        """
        
        self.console.print(header, style="bold cyan")
        self.console.print()
    
    def show_listening_animation(self, duration: float = 2):
        """Show listening state with sci-fi animation"""
        frames = [
            "[>>>        ] LISTENING FOR AUDIO INPUT",
            "[>>>>       ] LISTENING FOR AUDIO INPUT",
            "[>>>>>      ] LISTENING FOR AUDIO INPUT",
            "[>>>>>>     ] LISTENING FOR AUDIO INPUT",
            "[>>>>>>>    ] LISTENING FOR AUDIO INPUT",
            "[>>>>>>>>   ] LISTENING FOR AUDIO INPUT",
            "[>>>>>>>>>  ] LISTENING FOR AUDIO INPUT",
            "[>>>>>>>>>> ] LISTENING FOR AUDIO INPUT",
        ]
        start_time = time.time()
        
        while time.time() - start_time < duration:
            for frame in frames:
                self.console.print(f"\r{frame}", end="", style="cyan bold")
                time.sleep(0.15)
        
        self.console.print()
    
    def show_processing_animation(self, duration: float = 1):
        """Show processing animation with sci-fi theme"""
        frames = [
            "[=         ] ANALYZING LANGUAGE PATTERNS",
            "[==        ] ANALYZING LANGUAGE PATTERNS",
            "[===       ] ANALYZING LANGUAGE PATTERNS",
            "[====      ] ANALYZING LANGUAGE PATTERNS",
            "[=====     ] ANALYZING LANGUAGE PATTERNS",
            "[======    ] ANALYZING LANGUAGE PATTERNS",
            "[=======   ] ANALYZING LANGUAGE PATTERNS",
            "[========  ] ANALYZING LANGUAGE PATTERNS",
            "[========= ] ANALYZING LANGUAGE PATTERNS",
            "[========= ] GENERATING RESPONSE PROTOCOL",
        ]
        start_time = time.time()
        
        while time.time() - start_time < duration:
            for frame in frames:
                self.console.print(f"\r{frame}", end="", style="magenta bold")
                time.sleep(0.08)
        
        self.console.print()
    
    def show_speaking_animation(self, duration: float = 1):
        """Show speaking animation with sci-fi theme"""
        frames = [
            "[*       ] TRANSMITTING AUDIO RESPONSE",
            "[  *     ] TRANSMITTING AUDIO RESPONSE",
            "[    *   ] TRANSMITTING AUDIO RESPONSE",
            "[      * ] TRANSMITTING AUDIO RESPONSE",
            "[        *] TRANSMITTING AUDIO RESPONSE",
            "[      * ] TRANSMITTING AUDIO RESPONSE",
            "[    *   ] TRANSMITTING AUDIO RESPONSE",
            "[  *     ] TRANSMITTING AUDIO RESPONSE",
        ]
        start_time = time.time()
        
        while time.time() - start_time < duration:
            for frame in frames:
                self.console.print(f"\r{frame}", end="", style="green bold")
                time.sleep(0.12)
        
        self.console.print()
    
    def display_user_input(self, text: str):
        """Display user input in sci-fi style"""
        panel = Panel(
            Text(f"USER INPUT > {text.upper()}", style="bold cyan"),
            border_style="cyan",
            title="[COMMAND]"
        )
        self.console.print(panel)
    
    def display_response(self, text: str):
        """Display bot response in sci-fi style"""
        panel = Panel(
            Text(f"SYSTEM > {text}", style="bold green"),
            border_style="green",
            title="[RESPONSE]"
        )
        self.console.print(panel)
    
    def display_system_info(self):
        """Display system information in sci-fi style"""
        table = Table(title="[SYSTEM DIAGNOSTICS]", show_header=True, header_style="bold cyan")
        table.add_column("ATTRIBUTE", style="cyan")
        table.add_column("VALUE", style="green")
        
        table.add_row("OPERATING_SYSTEM", platform.system())
        table.add_row("PLATFORM", platform.platform())
        table.add_row("PYTHON_VERSION", platform.python_version())
        table.add_row("PROCESSOR", platform.processor())
        table.add_row("SYSTEM_TIME", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        self.console.print(table)
    
    def display_time(self):
        """Display current time in sci-fi style"""
        current_time = datetime.now().strftime("%H:%M:%S")
        panel = Panel(
            Text(current_time, justify="center", style="bold yellow"),
            border_style="yellow",
            title="[TEMPORAL SYNC]"
        )
        self.console.print(panel)
    
    def display_date(self):
        """Display current date in sci-fi style"""
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        panel = Panel(
            Text(current_date, justify="center", style="bold cyan"),
            border_style="cyan",
            title="[CALENDAR_SYNC]"
        )
        self.console.print(panel)
    
    def display_help(self):
        """Display help information in sci-fi style"""
        help_text = """
[AVAILABLE COMMANDS]

VOICE_COMMANDS:
  - "Hello" - Initiate connection handshake
  - "What time is it?" - Query temporal coordinates
  - "What is today?" - Query calendar data
  - "System info" - Display full diagnostics
  - "Help" - Display command protocol
  - "Goodbye" - Terminate session

KEYBOARD_SHORTCUTS:
  - Ctrl+C - Emergency system shutdown
  - Speak clearly and directly
  - Optimal performance in low-noise environments
        """
        panel = Panel(help_text, border_style="cyan", title="[COMMAND_PROTOCOL]")
        self.console.print(panel)
    
    def display_error(self, error_msg: str):
        """Display error message in sci-fi style"""
        panel = Panel(
            Text(f"ERROR > {error_msg}", style="bold red"),
            border_style="red",
            title="[ALERT]"
        )
        self.console.print(panel)
    
    def display_status(self, status: str, style: str = "green"):
        """Display status message"""
        self.console.print(f"[{style}]>[/{style}] {status}")
    
    def display_welcome(self):
        """Display welcome message in sci-fi style"""
        welcome_text = """
[INITIALIZATION SEQUENCE COMPLETE]

AUTONOMOUS_DIALOGUE_SYSTEM ONLINE
All subsystems nominal for operation

Try commands like:
  * Hello
  * What time is it?
  * System info
  * Help

Type your command or speak directly:
        """
        panel = Panel(welcome_text, border_style="cyan", title="[READY_FOR_INPUT]")
        self.console.print(panel)


# Example usage
if __name__ == "__main__":
    ui = TerminalUI()
    
    ui.display_header()
    ui.display_welcome()
    time.sleep(2)
    
    ui.show_listening_animation(1)
    time.sleep(0.5)
    
    ui.display_user_input("Hello, what time is it?")
    time.sleep(0.5)
    
    ui.show_processing_animation(1)
    time.sleep(0.5)
    
    ui.display_time()
    time.sleep(1)
    
    ui.show_speaking_animation(1)
    time.sleep(0.5)
    
    ui.display_response("The current time is shown above. It's a beautiful day!")
    time.sleep(1)
    
    ui.display_system_info()
    time.sleep(1)
    
    ui.display_help()
