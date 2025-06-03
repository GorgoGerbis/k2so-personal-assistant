## K2-SO Personal Droid

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

### Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
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

* Basic wake-and-listen loop triggered by WIP (Key press, timer...?)
* Offline speech-to-text using microphone input
* Local text-to-speech output
* Simple command routing with keyword-based logic (e.g., time, date, shutdown)
* Response behavior defined in a local module
* Fully offline operation with no cloud services or network dependency
* Console logging of input and output for debugging

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
