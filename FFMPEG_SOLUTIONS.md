# FFmpeg Installation Solutions

The voice bot requires ffmpeg for speech recognition with OpenAI Whisper. Here are multiple ways to install it:

## Solution 1: Using Docker (Recommended - No System Dependencies)

The easiest way is to use Docker, which has ffmpeg pre-installed:

```bash
# Build and run using Docker
docker-compose up

# Or just build
docker build -t voicebot .
docker run -it --device /dev/snd -v /run/user/$(id -u)/pulse:/run/user/$(id -u)/pulse voicebot
```

**Pros:**
- No system-level dependencies needed
- Works across all operating systems
- Includes all required libraries
- Isolated environment

**Cons:**
- Requires Docker installation

---

## Solution 2: Direct Download (macOS)

Download ffmpeg directly from the official source:

```bash
# Download the latest ffmpeg for macOS
curl -o ffmpeg-macos.zip https://ffmpeg.org/download.html

# Or use a pre-built binary
# From: https://www.gyan.dev/ffmpeg/builds/

# Extract and move to /usr/local/bin
unzip ffmpeg-macos.zip
sudo mv ffmpeg /usr/local/bin/
```

**Verification:**
```bash
ffmpeg -version
```

---

## Solution 3: Using MacPorts (macOS Alternative)

If you have MacPorts installed:

```bash
sudo port install ffmpeg
```

---

## Solution 4: Using Conda (If Available)

If you have Anaconda/Miniconda installed:

```bash
conda install -c conda-forge ffmpeg
```

---

## Solution 5: Alternative Audio Processing (No FFmpeg)

If you cannot install ffmpeg, the app can use alternative audio libraries:

Update `src/speech_recognition_engine.py` to use librosa + scipy:

```python
# This allows Whisper to work without ffmpeg by pre-processing audio
import librosa
import numpy as np

audio, sr = librosa.load(temp_audio_file, sr=16000)
# Audio is now ready for Whisper without ffmpeg
result = self.model.transcribe(temp_audio_file, language="en")
```

Install the dependencies:
```bash
pip install librosa scipy
```

---

## Testing Your Installation

After installing ffmpeg:

```bash
# Test that ffmpeg is accessible
which ffmpeg

# Run the voice bot
source venv/bin/activate
python src/main.py

# Or test with microphone directly
python -c "
from src.speech_recognition_engine import SpeechRecognitionEngine
engine = SpeechRecognitionEngine()
result = engine.listen(demo_mode=False)
print(f'You said: {result}')
"
```

---

## Troubleshooting

### Error: "No such file or directory: 'ffmpeg'"

This means ffmpeg is not installed or not in your PATH. Try:

```bash
# Check if ffmpeg exists anywhere
find /usr/local -name ffmpeg
find /opt -name ffmpeg

# Add to PATH if found
export PATH=$PATH:/path/to/ffmpeg/directory
```

### "ffmpeg version shows but Whisper still fails"

Restart Python kernel or shell:
```bash
deactivate
source venv/bin/activate
python src/main.py
```

### macOS Permission Denied

If you get permission errors:
```bash
# For files in /usr/local/bin, ensure they're executable
sudo chmod +x /usr/local/bin/ffmpeg

# Or place in a directory you own
mkdir -p ~/bin
cp ffmpeg ~/bin/
export PATH=~/bin:$PATH
```

---

## Recommended Path

1. **Try Docker first** (easiest, no system setup)
2. **Use Conda** if already installed (2-3 commands)
3. **Direct download** if neither available
4. **Contact me** if stuck on any step

The voice bot will automatically detect if ffmpeg is missing and provide helpful guidance.
