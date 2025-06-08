import sys
import os
import time
import threading

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from components.ai_indicator import AIIndicator, AIState

def simulate_conversation():
    """simulate a conversation with audio levels"""
    print("K2SO: Starting animation test...")
    print("  - Press SPACEBAR to toggle: Ripples ↔ Frequency")
    print("  - Press ESC to exit")
    print("  - Watch the different animation modes!")
    
    # create the indicator with ripples mode
    indicator = AIIndicator(fullscreen=False, animation_mode="ripples")
    indicator.start_gui()
    time.sleep(1)
    
    # simulate different states with varying audio levels
    states = [
        (AIState.IDLE, 0.0, 2.0),
        (AIState.PROCESSING, 0.2, 3.0),
        (AIState.SPEAKING, 0.8, 4.0),  # high audio level
        (AIState.SPEAKING, 0.5, 3.0),  # medium audio
        (AIState.SPEAKING, 0.9, 3.0),  # high audio again
        (AIState.IDLE, 0.0, 2.0),
    ]
    
    # run through states
    for state, audio_level, duration in states:
        print(f"State: {state.value}, Audio Level: {audio_level:.1f}")
        indicator.set_state(state)
        indicator.set_audio_level(audio_level)
        
        # gradually vary audio level during speaking
        if state == AIState.SPEAKING:
            steps = int(duration * 10)  # 10 updates per second
            for i in range(steps):
                # vary audio level for animation reactivity
                varied_level = audio_level + 0.2 * (i % 3 - 1)  # varies ±0.2
                indicator.set_audio_level(max(0.0, min(1.0, varied_level)))
                time.sleep(0.1)
        else:
            time.sleep(duration)
    
    print("Test complete - GUI will remain open")
    print("Try switching animation modes with SPACEBAR!")
    
    # keep the main thread alive so GUI doesn't close
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        indicator.close()

if __name__ == "__main__":
    simulate_conversation() 