#!/usr/bin/env python3
"""
K2SO GUI Animation Test - Water ripples vs Audio waveform modes
Press SPACEBAR to toggle between modes, ESC to quit
"""
import time
import sys
import os
import math

# add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from components.ai_indicator import AIIndicator

def test_dual_modes():
    print("🌊 K2SO Animation Test")
    print("=" * 40)
    
    # start with ripples mode
    ai_indicator = AIIndicator(fullscreen=False, animation_mode="ripples")
    ai_indicator.start_gui()
    
    print("✓ GUI started (600x600 window)")
    print("✓ Water ripples mode active")
    print("\n🎮 Controls:")
    print("  SPACEBAR = Toggle ripples ↔ waveform")
    print("  ESC = Exit")
    print("\n🎯 What to expect:")
    print("  • Larger centered animations")
    print("  • Smooth 30fps motion")
    print("  • Clean mode switching")
    print("  • Audio-reactive intensity")
    
    time.sleep(2)
    
    print("Starting speaking animation with simulated audio levels...")
    ai_indicator.set_speaking()
    
    # simulate varying audio levels for 10 seconds
    for i in range(200):  # 10 seconds at 20fps
        # simulate audio level variation
        audio_level = (math.sin(i * 0.2) * 0.5 + 0.5) * 0.8 + 0.2
        ai_indicator.set_audio_level(audio_level)
        time.sleep(0.05)  # 20fps
    
    print("Test complete! Try pressing SPACEBAR to switch modes.")
    print("Audio levels should make the animation more intense.")
    
    # keep running
    try:
        while ai_indicator.window:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nClosing...")
        ai_indicator.close()

if __name__ == "__main__":
    test_dual_modes() 