## K2-SO Personal Droid

A simple voice assistant for Raspberry Pi.

### Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

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


