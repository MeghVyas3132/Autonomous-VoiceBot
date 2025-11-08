FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for audio
RUN apt-get update && apt-get install -y \
    alsa-utils \
    pulseaudio \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create non-root user
RUN useradd -m voicebot && chown -R voicebot:voicebot /app
USER voicebot

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV WHISPER_MODEL_SIZE=base

# Run the application
CMD ["python", "src/main.py"]
