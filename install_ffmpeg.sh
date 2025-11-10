#!/bin/bash
# FFmpeg Installation Script for macOS
# Easy installation without Homebrew or Conda

set -e  # Exit on error

echo "=================================================="
echo "FFmpeg Installation for Offline-VoiceBot"
echo "=================================================="
echo ""

# Function to print colored output
print_success() {
    echo "✓ $1"
}

print_error() {
    echo "✗ $1"
}

print_info() {
    echo "ℹ $1"
}

# Check if ffmpeg already installed
if command -v ffmpeg &> /dev/null; then
    echo ""
    print_success "FFmpeg already installed!"
    ffmpeg -version | head -1
    echo ""
    exit 0
fi

# Try MacPorts first
if command -v port &> /dev/null; then
    echo ""
    print_info "MacPorts found. Installing ffmpeg..."
    sudo port install ffmpeg
    if command -v ffmpeg &> /dev/null; then
        print_success "FFmpeg installed successfully!"
        ffmpeg -version | head -1
        exit 0
    fi
fi

# If no package manager, provide download instructions
echo ""
print_info "No package manager detected (Conda/MacPorts)"
echo ""
echo "Please choose one of these options:"
echo ""
echo "Option 1: Install via pip (requires system ffmpeg first)"
echo "   python -m pip install ffmpeg-python"
echo ""
echo "Option 2: Download from official site"
echo "   Visit: https://ffmpeg.org/download.html#build-mac"
echo "   Download macOS build"
echo "   Extract and move to /usr/local/bin/"
echo ""
echo "Option 3: Use Docker (includes ffmpeg pre-installed)"
echo "   docker-compose up"
echo ""
echo "Option 4: Try this automated download:"
echo ""

# Try to download ffmpeg binary
echo "Attempting to download ffmpeg..."
cd /tmp

# Try official ffmpeg.org mirrors
FFMPEG_URL="https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2"
if curl -L -f --connect-timeout 5 -o ffmpeg-snap.tar.bz2 "$FFMPEG_URL" 2>/dev/null; then
    print_success "Downloaded ffmpeg snapshot"
    tar -xjf ffmpeg-snap.tar.bz2
    cd ffmpeg-*
    
    print_info "Building ffmpeg (this may take 5-10 minutes)..."
    ./configure --prefix=/usr/local --enable-gpl
    make
    sudo make install
    
    if command -v ffmpeg &> /dev/null; then
        print_success "FFmpeg installed successfully!"
        ffmpeg -version | head -1
        
        # Cleanup
        cd /tmp
        rm -rf ffmpeg-*
        exit 0
    fi
fi

# If all else fails, provide detailed instructions
echo ""
print_error "Automatic installation failed"
echo ""
echo "Please install ffmpeg manually:"
echo ""
echo "1. Go to: https://ffmpeg.org/download.html"
echo "2. Download the macOS build"
echo "3. Extract the zip file"
echo "4. Move ffmpeg to /usr/local/bin/"
echo ""
echo "   $ unzip ffmpeg-*.zip"
echo "   $ sudo mv ffmpeg-* /usr/local/bin/ffmpeg"
echo "   $ chmod +x /usr/local/bin/ffmpeg"
echo ""
echo "5. Verify installation:"
echo "   $ which ffmpeg"
echo "   $ ffmpeg -version"
echo ""
