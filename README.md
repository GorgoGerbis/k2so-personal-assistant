## K-2SO Personal Droid

A simple voice assistant for Raspberry Pi.

I have multiple options to run a chatbot on Raspberry Pi 5.
Option 1: Run a small quantized model locally
- Fully offline and self-contained.
- Best for privacy, no latency, and no internet dependency.
- Runs slower than cloud but manageable for prototypes.

Option 2: Offload to a local server/LAN PC
- Keep the Pi as a frontend.
- Backend server handles heavy model inference.
- Fast, and allows use of bigger models.

Option 3: Use cloud-hosted models (not preferred)
- Not aligned with goal of fully local. 

### Running the Project

The project uses a virtual environment named `.venv-k2so`. After setup, you can activate and run the project:

```powershell
# Windows PowerShell
.\.venv-k2so\Scripts\Activate.ps1

# Windows Command Prompt
.\.venv-k2so\Scripts\activate.bat

# Linux/Mac
source .venv-k2so/bin/activate
```

Once activated, run the project from the root directory:
```bash
python src/main.py
```

### Setup

1. Create virtual environment:
```bash
python -m venv .venv-k2so
```

2. Activate the environment (see above for your shell)

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Pi Setup
1. Update Raspberry Pi:
```bash
sudo apt update && sudo apt upgrade -y
```
2. Install Python 3 and build tools:
```bash
sudo apt install -y python3 python3-pip python3-venv build-essential
```

3. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install Python Packages: WIP
```bash
pip install llama-cpp-python
```

5. Download a Small Quantized Model: WIP
    - Option A: With Hugging Face CLI
    - Option B: Direct Download

### MVP Features to Implement

- [ ] basic wake-and-listen loop (triggered by key press, timer, or hotword)
- [ ] offline speech-to-text using microphone input
- [ ] local text-to-speech output
- [ ] simple command routing with keyword-based logic (e.g., time, date, shutdown)
- [ ] response behavior defined in a local module
- [ ] fully offline operation with no cloud services or network dependency
- [ ] console logging of input and output for debugging

## Planned Features (Next Branch)

- [ ] face gui: animated ai face with expressions that react to conversation and speech
- [ ] chat log: persistent chat history for each session
    - [ ] logging of command and message history to support contextual follow-ups
- [ ] easy setup interface: gui or executable for first-time setup (api keys, model selection, etc.)
    - [ ] config directory for user preferences and local settings
- [ ] voice toggle: flags to enable/disable text-to-speech and speech-to-text
    - [ ] adjustable speaking rate and voice settings for tts
    - [ ] optional hotword detection toggle in config
- [ ] conversational memory: maintain context for back-and-forth, multi-turn conversations
    - [ ] message handler pattern for extensible command-response workflows
    - [ ] local intent parsing for natural language input matching
- [ ] resource/cost tracking: track resource usage (ram, cpu, model size) and, for remote models, estimate api cost per prompt
- [ ] modular command handling for extended system functions (e.g., weather, file access)
- [ ] robust error handling and fallback behavior

> development for these features will be done in a new branch: `feature/next-gen-gui-and-logging`

### Additional Features to Implement

* Voice activation using local speech detection or hotword models
* Adjustable speaking rate and voice settings for text-to-speech
* Modular command handling for extended system functions (e.g., weather, file access)
* Local intent parsing for natural language input matching
* Optional hotword detection toggle in config
* Message handler pattern for extensible command-response workflows
* Logging of command history to support contextual follow-ups
* Config directory for user preferences and local settings
* Robust error handling and fallback behavior
