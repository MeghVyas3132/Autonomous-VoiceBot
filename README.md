# 🎤 Autonomous Voice Bot - Complete System Control

A professional **offline voice assistant** for macOS with full system control. Give your MacBook complete voice command capabilities - ask where you are, check weather, control brightness/volume, manage applications, and much more!

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![macOS](https://img.shields.io/badge/macOS-Compatible-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

**Voice Control • System Integration • AI-Powered • Offline Operation**

</div>

---

## ✨ Key Features

### 🗣️ Voice Capabilities
- **Female Voice**: Natural human-like speech (Samantha, 190 WPM)
- **Real Microphone**: OpenAI Whisper (90%+ accuracy)
- **Offline**: Core features work without internet
- **Multiple Tones**: Natural, Fast, Slow, Formal, Casual
- **Prosody**: Intelligent pauses and emphasis

### 🎮 System Control
- **Location & Weather**: Ask where you are, check weather
- **Find Places**: "Find nearby restaurants"
- **System Monitoring**: Battery, disk, network status
- **Control**: Brightness, volume, sleep, lock screen
- **Apps**: Open/close applications
- **Web Search**: Search the internet

### 💡 Smart Features
- **Natural Language**: Understands command variations
- **Smart Responses**: Automatic tone selection
- **Demo Mode**: Works with text input
- **Terminal UI**: Clean, professional interface
- **Extensible**: Easy to add custom commands

## 🚀 Quick Start (5 minutes)

### 1. Setup

```bash
cd /Users/meghvyas/Desktop/Offline-VoiceBot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Install FFmpeg

```bash
# Option 1: Conda (Easiest)
conda install -c conda-forge ffmpeg

# Option 2: MacPorts
sudo port install ffmpeg

# Option 3: Direct Download
# Visit https://ffmpeg.org/download.html and follow instructions
```

### 3. Run

```bash
python src/main.py
```

## 📖 Complete Commands

### 🗺️ Location & Maps
- "Where am I?" → Shows location (city, coordinates)
- "Find nearby restaurants" → Opens Maps search
- "Coffee shops" → Find coffee shops near you

### 🌤️ Weather
- "What's the weather?" → Current weather data
- "Weather here" → Same as above
- "Is it raining?" → Rain information

### 💻 System Monitoring
- "System information" → Full system details
- "Battery status" → Battery % and charging status
- "Disk usage" → Storage information
- "Network status" → WiFi connection info

### 🔆 Brightness
- "Get brightness" → Current level
- "Set brightness to 80" → 0-100% control

### 🔊 Volume
- "Get volume" → Current level
- "Set volume to 50" → 0-100% control
- "Mute" → Mute sound
- "Unmute" → Restore sound

### 📱 Applications
- "Open Chrome" → Launch app
- "Close Spotify" → Close app
- "List applications" → Show open apps

### 🌐 Web
- "Open google.com" → Open in browser
- "Search for Python" → Google search

### ⚙️ System
- "Lock screen" → Lock Mac
- "Sleep" → Sleep Mac

## 🔊 Voice Characteristics

- **Speed**: 190 WPM (natural conversational)
- **Voice**: Samantha (female, high-quality)
- **Tones**: Natural, Fast, Slow, Formal, Casual
- **Prosody**: Intelligent pauses and emphasis

## 📁 Project Structure

```
Offline-VoiceBot/
├── src/
│   ├── main.py                          # Main app
│   ├── speech_recognition_engine.py     # Whisper
│   ├── speech_synthesis.py              # Voice
│   ├── response_engine.py               # Responses
│   ├── terminal_ui.py                   # UI
│   ├── system_control.py                # System integration
│   ├── advanced_command_interpreter.py  # NLP
│   └── connectivity_manager.py          # Online/offline
├── config/
│   └── settings.py                      # Config
├── data/
│   └── responses.json                   # Response templates
├── requirements.txt                     # Dependencies
└── README.md                            # This file
```

## 🛠️ Technology

- **Python 3.9+**
- **Whisper**: Speech recognition (90%+ accuracy)
- **macOS say command**: Natural voice synthesis
- **Rich**: Terminal UI
- **SoundDevice**: Audio capture

## ⚙️ Configuration

Edit `config/settings.py`:

```python
TTS_VOICE_RATE = 190    # Speech speed (100-400 WPM)
TTS_VOLUME = 1.0        # Volume (0.0-1.0)
WHISPER_MODEL_SIZE = "base"  # Model size
SAMPLE_RATE = 16000     # Audio rate
```

## 🧪 Testing

```bash
# Test voice quality and FFmpeg
python test_voice_fixes.py

# Test system control commands
python test_system_control.py

# Full demo with text input
python test_demo.py
```

## 🔐 Privacy

✅ All operations local  
✅ No data sent elsewhere  
✅ No API keys needed  
✅ Complete privacy

## 📊 System Requirements

- macOS 10.14+
- Python 3.9+
- 2GB free space
- Microphone (optional for voice)
- FFmpeg (for real audio)

## 🚀 Advanced Usage

### Add Custom Commands

Edit `src/advanced_command_interpreter.py` to add new commands.

### Change Voice Tone

```python
synth.speak("Hello!", voice_tone='fast')      # Fast
synth.speak("Hello!", voice_tone='slow')      # Slow
synth.speak("Hello!", voice_tone='formal')    # Formal
synth.speak("Hello!", voice_tone='casual')    # Casual
```

### Extend System Control

Edit `src/system_control.py` to add calendar, email, file operations, etc.

## 📞 Support

**Having issues?**

1. Run diagnostics: `python test_voice_fixes.py`
2. Check FFmpeg: `which ffmpeg`
3. Enable debug: Set `DEBUG = True` in `config/settings.py`
4. Read error messages carefully

## 📝 Troubleshooting

| Issue | Solution |
|-------|----------|
| FFmpeg error | Install FFmpeg (see Quick Start) |
| Voice robotic | Already optimized to 190 WPM |
| Commands not recognized | Run `python test_system_control.py` |
| Microphone not working | Use demo mode: `python src/main.py --demo` |

## 🎉 What's Included

✅ Complete system control  
✅ Natural human-like voice  
✅ Location and weather  
✅ Application management  
✅ Battery/disk monitoring  
✅ Brightness/volume control  
✅ Web search integration  
✅ Professional UI  
✅ Offline operation  
✅ Demo mode available  

## 🎯 Getting Started

1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Install FFmpeg
5. Run: `python src/main.py`
6. Try: "Where am I?" or "What's the weather?"

---

**Your macBook is now voice-controlled!** 🎤✨

Built with ❤️ for offline voice control and complete system integration.

