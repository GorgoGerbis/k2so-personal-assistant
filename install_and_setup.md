# K2SO Personal Assistant - Installation & Setup Guide

**WORK IN PROGRESS** - This installation guide is still being developed and tested. Some steps may need refinement.

This guide walks you through installing and running the K2SO Personal Assistant on both Windows and Raspberry Pi systems.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Windows Installation](#windows-installation)
  - [Raspberry Pi Installation](#raspberry-pi-installation)
- [Configuration](#configuration)
- [Running the Assistant](#running-the-assistant)
- [Testing Your Setup](#testing-your-setup)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

**Hardware needs:**
- RAM: 4GB minimum, 8GB recommended
- Storage: 2GB free space for models and dependencies
- Audio: Working speakers/headphones for text-to-speech
- Microphone: Optional (planned for future speech input)

**Operating systems:**
- Windows 10/11 (development environment)
- Raspberry Pi OS (recommended for deployment)
- Linux (Ubuntu, Debian - should work but less tested)

### Software you'll need

**Everyone needs:**
- Python 3.8 or higher
- Git
- Internet connection (for setup and downloading models)

**Windows users:**
- PowerShell or Command Prompt
- Windows SAPI (built-in for text-to-speech)

**Pi users:**
- Updated Raspberry Pi OS
- Audio configured and working

---

## Installation

### Windows Installation

#### Step 1: Install Python and Git

1. **Download Python 3.8+** from [python.org](https://python.org)
   - Check "Add Python to PATH" during installation
   - Choose "Install for all users" if prompted

2. **Install Git** from [git-scm.com](https://git-scm.com)
   - Use default settings during installation

3. **Verify installation** in PowerShell/Command Prompt:
   ```bash
   python --version
   git --version
   ```

#### Step 2: Clone the Repository

```bash
# Clone the project
git clone https://github.com/your-username/k2so-personal-assistant.git
cd k2so-personal-assistant
```

#### Step 3: Set Up Python Environment

```bash
# Create virtual environment
python -m venv .venv-k2so

# Activate virtual environment
# PowerShell:
.\.venv-k2so\Scripts\Activate.ps1

# Command Prompt:
.\.venv-k2so\Scripts\activate.bat

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Install Ollama (for LLM)

1. Download Ollama from [ollama.com](https://ollama.com)
2. Install and start the Ollama service
3. Pull the Phi-3 model (this is what we're using):
   ```bash
   ollama pull phi3
   ```

### Raspberry Pi Installation

#### Step 1: Update System

```bash
# Update package lists and system
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install -y python3 python3-pip python3-venv git build-essential
```

#### Step 2: Clone Repository

```bash
# Clone the project
git clone https://github.com/your-username/k2so-personal-assistant.git
cd k2so-personal-assistant
```

#### Step 3: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv .venv-k2so

# Activate virtual environment
source .venv-k2so/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Install Ollama (Pi Version)

```bash
# Install Ollama for ARM64
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
sudo systemctl enable ollama
sudo systemctl start ollama

# Pull the Phi-3 model (optimized for Pi)
ollama pull phi3
```

#### Step 5: Configure Audio (Pi Only)

```bash
# Test audio output
speaker-test -t wav -c 2

# If no sound, configure audio output:
sudo raspi-config
# Navigate to: Advanced Options > Audio > Force 3.5mm jack
```

---

## Configuration

### Environment Setup

The project includes a `.env` file for configuration. You can edit it if needed:
   ```bash
   # Example .env content:
   # API KEYS (optional - only needed for remote models)
   OPENAI_API_KEY=your_openai_key_here
   
   # Desktop Setups (Windows specific)
   PIPER_EXE_WINDOWS_DESKTOP=path_to_piper_if_installed
   ```

### Model Configuration

Edit `src/config.py` to customize your setup:

```python
# Choose your preferred model
SELECTED_MODEL = "testLocal"  # Uses Ollama with Phi-3

# Enable/disable features
TTS_ENABLED = True          # Text-to-speech output
GUI_ENABLED = True          # Visual AI indicator
GUI_FULLSCREEN = False      # Windowed mode (recommended for testing)
GUI_ANIMATION_MODE = "ripples"  # "ripples" or "frequency"
```

### Audio Setup

**Windows:** Should work automatically with Windows SAPI.

**Raspberry Pi:** Test your audio:
```bash
# Test TTS
echo "Hello from K2SO" | espeak

# If issues, check audio device:
aplay -l
```

---

## Running the Assistant

### Starting the Assistant

1. **Activate virtual environment:**
   ```bash
   # Windows PowerShell:
   .\.venv-k2so\Scripts\Activate.ps1
   
   # Linux/Pi:
   source .venv-k2so/bin/activate
   ```

2. **Start the assistant:**
   ```bash
   python src/main.py
   ```

3. **You should see:**
   - Console output showing initialization
   - Visual AI indicator window (if GUI_ENABLED=True)
   - "K2SO: Ready for conversation!" message

### Using the Assistant

**Text Conversation:**
- Type your messages in the console
- Press Enter to send
- K2SO will respond with text and speech (if TTS enabled)
- Type 'quit' or 'exit' to stop

**Visual Indicator Controls:**
- **SPACEBAR:** Toggle between animation modes (ripples ↔ frequency)
- **ESC:** Close the visual indicator window

---

## Testing Your Setup

### Quick Test

Run this test to see if everything is working:

```bash
# With virtual environment activated:
python test_animations.py
```

**Expected behavior:**
- Window opens with blue circle and animations
- Console shows state changes (idle → processing → speaking)
- You can toggle animation modes with spacebar
- Window stays open until you press ESC

### Full Conversation Test

1. **Start the assistant:**
   ```bash
   python src/main.py
   ```

2. **Try these test messages:**
   - "Hello K2SO"
   - "What is the weather like?" (tests response generation)
   - "Tell me a joke" (tests creative responses)

3. **Verify:**
   - Text responses appear in console
   - Speech audio plays (if TTS enabled)
   - Visual indicator shows speaking state (if GUI enabled)
   - No error messages in console

---

## Troubleshooting

*Note: This troubleshooting section is still being expanded based on user feedback.*

### Common Issues

#### "Ollama not found" or connection errors

**Solution:**
```bash
# Check if Ollama is running:
# Windows:
ollama list

# Pi/Linux:
sudo systemctl status ollama

# If not running, start it:
# Windows: Start Ollama desktop app
# Pi/Linux:
sudo systemctl start ollama

# Pull model if missing:
ollama pull phi3
```

#### No audio output

**Windows:**
- Check Windows volume mixer
- Verify default audio device in Sound settings

**Raspberry Pi:**
```bash
# Check audio configuration:
sudo raspi-config
# Advanced Options > Audio > Force 3.5mm jack

# Test audio:
speaker-test -c 2 -t wav
```

#### Python module errors

**Solution:**
```bash
# Ensure virtual environment is activated
# Then reinstall dependencies:
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### Visual indicator window doesn't appear

**Solution:**
1. Check `src/config.py`: Ensure `GUI_ENABLED = True`
2. On Pi, install tkinter: `sudo apt install python3-tk`
3. Check for display issues: `echo $DISPLAY` (should show `:0` or similar)

#### Permission errors (Pi)

**Solution:**
```bash
# Add user to audio group:
sudo usermod -a -G audio $USER

# Reboot after group changes:
sudo reboot
```

### Getting Help

The assistant prints helpful information to the console, so check there first.

**Test individual parts:**
- LLM: Try `ollama run phi3` to test Ollama directly
- TTS: Run `test_animations.py` to test visual and audio
- GUI: Look in the console for tkinter error messages

**Common log messages:**
- `"K2SO: Ready for conversation!"` - Successful startup
- `"Animation mode: [mode name]"` - GUI working
- `"AI indicator: speaking"` - State management working

---

## What's Next

Once everything is working:

1. Try pressing spacebar to switch between animation modes (ripples and frequency)
2. Look at the source code if you want to customize responses
3. The code is modular, so you can extend it pretty easily
4. If you set this up on Windows, you can copy your config to a Pi later
