import sys
import os
import time
import threading
import random
import math

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from components.ai_indicator import AIIndicator, AIState
from components.gui_manager import GUIManager, DisplayMode

def simulate_dramatic_audio():
    """Simulate dramatic audio level changes for testing"""
    print("Starting K2SO Waveform Test...")
    print("Controls:")
    print("  F1-F4 - Switch views")
    print("  SPACE - Toggle animation mode")
    print("  ESC - Exit")
    
    # Create and start GUI
    gui = GUIManager(fullscreen=False, animation_mode="waveform")
    gui.start()
    
    # Test conversation with dramatic audio changes
    conversation = [
        # Format: (state, duration, audio_pattern)
        # Audio patterns: "sine" (smooth), "pulse" (dramatic), "ramp" (building)
        (AIState.IDLE, 2.0, None),
        (AIState.SPEAKING, 4.0, "sine"),     # Gentle sine wave
        (AIState.SPEAKING, 3.0, "pulse"),    # Dramatic pulses
        (AIState.PROCESSING, 2.0, None),
        (AIState.SPEAKING, 5.0, "ramp"),     # Building intensity
        (AIState.SPEAKING, 3.0, "pulse"),    # More dramatic pulses
        (AIState.IDLE, 2.0, None),
    ]
    
    try:
        if gui.root and gui.ai_indicator:
            def update_audio():
                for state, duration, pattern in conversation:
                    print(f"State: {state.value}, Pattern: {pattern if pattern else 'none'}")
                    gui.ai_indicator.set_state(state)
                    
                    start_time = time.time()
                    while time.time() - start_time < duration and gui.running:
                        if pattern == "sine":
                            # Smooth sine wave
                            t = (time.time() - start_time) * 2
                            level = 0.5 + 0.5 * math.sin(t * math.pi)
                        elif pattern == "pulse":
                            # Dramatic pulses
                            t = (time.time() - start_time) * 4
                            level = random.uniform(0.7, 1.0) if t % 1 < 0.5 else 0.2
                        elif pattern == "ramp":
                            # Building intensity
                            progress = (time.time() - start_time) / duration
                            base = min(1.0, progress * 2)
                            level = base + random.uniform(-0.1, 0.1)
                        else:
                            level = 0.0
                            
                        gui.ai_indicator.set_audio_level(max(0.0, min(1.0, level)))
                        time.sleep(0.05)
                
                # Set to idle state with no audio level
                gui.ai_indicator.set_idle()  # This will reset audio level to 0
                
                # Keep running but stay idle (flat line)
                while gui.running:
                    time.sleep(0.1)  # Just wait, no more audio simulation
            
            # Start audio simulation in background
            audio_thread = threading.Thread(target=update_audio, daemon=True)
            audio_thread.start()
            
            # Start main loop
            gui.root.mainloop()
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        gui.stop()

if __name__ == "__main__":
    simulate_dramatic_audio()