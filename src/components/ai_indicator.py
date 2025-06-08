import tkinter as tk
import threading
import time
import math
import random
from enum import Enum

class AIState(Enum):
    IDLE = "idle"
    PROCESSING = "processing" 
    SPEAKING = "speaking"

class AIIndicator:
    def __init__(self, fullscreen=False, animation_mode="waveform", parent=None):
        self.fullscreen = fullscreen
        self.animation_mode = animation_mode  # "waveform", "ripples", or "frequency"
        self.current_state = AIState.IDLE
        self.parent = parent  # Parent frame for integration
        self.window = None
        self.canvas = None
        self.frame = None  # Container frame when used with parent
        self.center_circle = None
        self.wave_rings = []
        self.waveform_bars = []
        self.animation_thread = None
        self.animation_running = False
        self.audio_level = 0.0  # real-time audio level (0.0 to 1.0)
        
        # screen dimensions for scaling
        self.screen_width = 1920
        self.screen_height = 1080
        self.center_x = self.screen_width // 2
        self.center_y = self.screen_height // 2
        
        # color scheme for different states
        self.colors = {
            AIState.IDLE: "#1a2332",        # dark blue-gray
            AIState.PROCESSING: "#00aaff",   # bright blue  
            AIState.SPEAKING: "#00ffff"      # cyan
        }
        
        # waveform parameters
        self.bar_width = 12  # base bar width
        self.bar_spacing = 6  # base spacing
        self.bar_base_height = 0  # minimal baseline height (changed to 0)
        self.max_bar_height = 250  # increased maximum height
        self.waveform_color = "#00ffff"  # cyan
        self.waveform_peak_color = "#ff3366"  # pink-red for peaks
        self.height_smoothing = 0.25  # increased smoothing for more fluid motion
        
        # These will be calculated dynamically based on screen width
        self.num_bars = 32  # initial value, will be updated
        self.bar_heights = []  # will be initialized in _update_bar_count
        self.target_heights = []  # will be initialized in _update_bar_count
        
        # animation parameters
        self.base_radius = 60 if not fullscreen else 120
        self.wave_count = 5
        self.wave_speed = 0.08  # slightly increased for more movement
        self.wave_amplitude = 20 if not fullscreen else 40
        self.animation_fps = 30  # frame rate for smooth animation
        
        # waveform parameters
        self.waveform_points = 200  # number of points across the line
        self.waveform_amplitude = 40  # maximum height from center line
        self.waveform_thickness = 2
        self.waveform_speed = 0.05
        
    def start_gui(self):
        """start the GUI in a separate thread"""
        if self.parent is None and self.window is None:
            gui_thread = threading.Thread(target=self._create_window, daemon=True)
            gui_thread.start()
            time.sleep(0.1)  # give window time to initialize
        elif self.parent is not None and self.frame is None:
            self._create_embedded_frame()
            
        # Start animation if not already running
        if not self.animation_running:
            self._start_animation()
    
    def get_frame(self):
        """Get the frame for embedding in parent GUI"""
        if self.parent is not None and self.frame is None:
            self._create_embedded_frame()
        return self.frame
    
    def _create_window(self):
        """create the tkinter window and canvas"""
        self.window = tk.Tk()
        self.window.title("K2SO - AI Assistant")
        
        if self.fullscreen:
            self.window.attributes('-fullscreen', True)
            self.window.configure(bg='black', cursor='none')
            canvas_width = self.screen_width
            canvas_height = self.screen_height
        else:
            # windowed mode - larger for better visibility
            canvas_width = 600
            canvas_height = 600
            self.window.geometry(f"{canvas_width}x{canvas_height}")
            self.window.configure(bg='black')
            self.window.attributes('-topmost', True)
        
        # always use actual canvas dimensions for centering
        self.center_x = canvas_width // 2
        self.center_y = canvas_height // 2
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        
        # scale animation parameters based on window size
        size_factor = min(canvas_width, canvas_height) / 400
        self.base_radius = int(60 * size_factor)
        self.wave_amplitude = int(20 * size_factor)
        
        # escape key to exit fullscreen
        self.window.bind('<Escape>', lambda e: self.window.quit())
        
        # spacebar to switch animation modes
        self.window.bind('<space>', self._toggle_animation_mode)
        self.window.focus_set()  # allow key bindings
        
        # bind to configure events to handle resizing
        self.window.bind('<Configure>', self._on_window_resize)
        
        # create canvas for drawing
        self.canvas = tk.Canvas(
            self.window, 
            width=canvas_width, 
            height=canvas_height,
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)  # allow canvas to resize with window
        
        # draw initial elements
        self._draw_elements()
        
        # start animation loop
        self._start_animation()
        
        # start tkinter main loop
        self.window.mainloop()
    
    def _create_embedded_frame(self):
        """Create embedded frame for use in parent GUI"""
        if self.parent is None:
            return
            
        self.frame = tk.Frame(self.parent, bg='black')
        
        # Create canvas that fills the frame
        self.canvas = tk.Canvas(
            self.frame,
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind to resize events
        self.canvas.bind('<Configure>', self._on_canvas_resize)
        
        # Draw initial elements
        self._draw_elements()
        
        # Set initial state to speaking to show animation
        self.set_speaking()
    
    def _on_canvas_resize(self, event):
        """Handle canvas resize events"""
        # Update dimensions
        self.canvas_width = event.width
        self.canvas_height = event.height
        self.center_x = self.canvas_width // 2
        self.center_y = self.canvas_height // 2
        
        # Scale animation parameters based on new size
        size_factor = min(self.canvas_width, self.canvas_height) / 400
        self.base_radius = int(60 * size_factor)
        self.wave_amplitude = int(20 * size_factor)
        
        # Redraw elements with new dimensions
        self._draw_elements()
    
    def _draw_elements(self):
        """draw the main interface elements"""
        if not self.canvas:
            return
            
        # Get current dimensions from canvas
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.center_x = self.canvas_width // 2
        self.center_y = self.canvas_height // 2
        
        # clear previous elements
        if self.center_circle:
            self.canvas.delete(self.center_circle)
        for ring in self.wave_rings:
            self.canvas.delete(ring)
        self.wave_rings.clear()
        
        # draw center circle (scale with window size)
        color = self.colors[self.current_state]
        radius = max(10, self.base_radius // 3)  # ensure minimum size
        
        self.center_circle = self.canvas.create_oval(
            self.center_x - radius, self.center_y - radius,
            self.center_x + radius, self.center_y + radius,
            fill=color, outline=color, width=max(1, int(radius/10))
        )
    
    def _start_animation(self):
        """start the animation thread"""
        self.animation_running = True
        self.animation_thread = threading.Thread(target=self._animate, daemon=True)
        self.animation_thread.start()
    
    def _animate(self):
        """main animation loop"""
        frame = 0
        wave_offsets = [random.uniform(0, 2 * math.pi) for _ in range(self.wave_count)]
        
        while self.animation_running and self.window:
            try:
                if self.current_state == AIState.SPEAKING:
                    # choose animation based on mode
                    if self.animation_mode == "ripples":
                        self._animate_water_ripples(frame, wave_offsets)
                    elif self.animation_mode == "waveform":
                        self._animate_simple_waveform(frame)
                    else:  # frequency
                        self._animate_audio_waveform(frame)
                        
                elif self.current_state == AIState.PROCESSING:
                    # gentle pulse for processing
                    self._animate_processing_pulse(frame)
                
                else:
                    # idle - just update center circle
                    self._animate_idle()
                
                frame += 1
                time.sleep(1.0 / self.animation_fps)  # use configured frame rate
                
            except Exception as e:
                print(f"Animation error: {e}")
                break
    
    def _animate_water_ripples(self, frame, wave_offsets):
        """create organic water-like ripples when speaking"""
        if not self.canvas:
            return
            
        # clear old wave rings
        self._clear_all_animations()
        
        # create new wave rings with fluctuation
        base_color = self.colors[AIState.SPEAKING]
        
        for i in range(self.wave_count):
            # calculate organic wave properties
            wave_time = frame * self.wave_speed + wave_offsets[i]
            
            # add more organic variation based on audio level
            audio_boost = 1.0 + (self.audio_level * 2.0)  # audio makes waves bigger
            amplitude_variation = random.uniform(0.6, 1.4) * audio_boost
            
            # irregular spacing for organic feel
            base_spacing = 25 + random.uniform(-5, 10)
            
            radius = (self.base_radius + 
                     i * base_spacing + 
                     math.sin(wave_time) * self.wave_amplitude * amplitude_variation +
                     math.sin(wave_time * 1.7 + i) * 8)  # secondary wave for complexity
            
            # ensure positive radius and don't exceed window bounds
            max_radius = min(self.canvas_width, self.canvas_height) // 2 - 20
            radius = max(10, min(radius, max_radius))
            
            # vary opacity and color intensity
            alpha_factor = max(0.15, (1.0 - (i * 0.12)) * (0.5 + self.audio_level))
            ring_color = self._adjust_alpha(base_color, alpha_factor)
            
            # slightly irregular shape (not perfect circle)
            offset_x = random.uniform(-2, 2)
            offset_y = random.uniform(-2, 2)
            
            # create organic ring
            ring = self.canvas.create_oval(
                self.center_x - radius + offset_x, self.center_y - radius + offset_y,
                self.center_x + radius + offset_x, self.center_y + radius + offset_y,
                outline=ring_color, width=max(1, int(2 * (1 + self.audio_level))), fill=""
            )
            self.wave_rings.append(ring)
        
        # update center circle with audio response
        if self.center_circle:
            center_intensity = 1.0 + 0.3 * math.sin(frame * 0.4) + (self.audio_level * 0.5)
            center_color = self._brighten_color(base_color, center_intensity)
            self.canvas.itemconfig(self.center_circle, fill=center_color, outline=center_color)
    
    def _animate_audio_waveform(self, frame):
        """create technical audio waveform visualization when speaking"""
        if not self.canvas:
            return
            
        # clear old waveform bars  
        self._clear_all_animations()
        
        # waveform parameters
        base_color = self.colors[AIState.SPEAKING]
        bar_count = 12  # number of frequency bars
        bar_width = 4
        max_height = self.base_radius * 1.5
        
        # create frequency bars around center circle
        angle_step = (2 * math.pi) / bar_count
        
        for i in range(bar_count):
            # calculate bar properties
            angle = i * angle_step + frame * 0.1  # slow rotation
            
            # simulate frequency data with audio level influence
            base_freq = math.sin(frame * 0.3 + i * 0.5) * 0.5 + 0.5
            audio_reactive = self.audio_level * random.uniform(0.7, 1.3)
            bar_height = (base_freq * 0.4 + audio_reactive * 0.6) * max_height
            
            # calculate bar position
            distance = self.base_radius + 20
            x = self.center_x + math.cos(angle) * distance
            y = self.center_y + math.sin(angle) * distance
            
            # create bar extending outward
            end_x = x + math.cos(angle) * bar_height
            end_y = y + math.sin(angle) * bar_height
            
            # vary color intensity based on bar height
            intensity = 0.5 + (bar_height / max_height) * 0.8
            bar_color = self._brighten_color(base_color, intensity)
            
            # create frequency bar
            bar = self.canvas.create_line(
                x, y, end_x, end_y,
                fill=bar_color, width=bar_width,
                capstyle=tk.ROUND
            )
            self.waveform_bars.append(bar)
        
        # update center circle with technical pulse
        if self.center_circle:
            center_intensity = 1.0 + self.audio_level * 0.8
            center_color = self._brighten_color(base_color, center_intensity)
            self.canvas.itemconfig(self.center_circle, fill=center_color, outline=center_color)
    
    def _animate_simple_waveform(self, frame):
        """Create equalizer-style waveform animation with growing/shrinking bars"""
        if not self.canvas:
            return
            
        # Update bar count based on current window size
        self._update_bar_count()
            
        # Clear previous waveform
        self._clear_all_animations()
        
        # Get current dimensions
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_y = height // 2
        
        # Calculate bar layout
        total_width = (self.bar_width + self.bar_spacing) * self.num_bars - self.bar_spacing
        start_x = (width - total_width) // 2
        
        # Generate new target heights for each bar
        for i in range(self.num_bars):
            if self.current_state == AIState.SPEAKING and self.audio_level > 0.05:
                # Create wave pattern across bars with smoother transitions
                t = frame * self.wave_speed  # Wave movement speed
                
                # Multiple wave frequencies for natural look
                wave1 = math.sin(t + i * 0.2) * 0.6  # Primary wave
                wave2 = math.sin(t * 0.7 + i * 0.15) * 0.4  # Secondary wave
                wave3 = math.sin(t * 0.3 + i * 0.25) * 0.3  # Tertiary wave
                
                # Combine waves with smoother blending
                combined_wave = (wave1 + wave2 + wave3) / 1.3  # Normalized blend
                
                # Make it always positive and scale by audio level with more dramatic response
                amplitude = (abs(combined_wave) * 0.8 + 0.2) * (self.audio_level ** 1.5)  # Exponential response
                
                # Add random variation for more natural look
                variation = random.uniform(0.85, 1.15)
                
                # Convert to actual bar height with more dramatic scaling
                target_height = amplitude * self.max_bar_height * variation
                self.target_heights[i] = max(0, min(self.max_bar_height, target_height))
            else:
                # Return to zero when not speaking or audio level is too low
                self.target_heights[i] = 0
        
        # Smoothly animate current heights toward targets
        for i in range(self.num_bars):
            diff = self.target_heights[i] - self.bar_heights[i]
            
            # When not speaking or audio level is zero/very low, immediately snap to flat line
            if self.current_state != AIState.SPEAKING or self.audio_level <= 0.01:
                # Immediate snap to zero - no animation delay
                self.bar_heights[i] = 0
            elif diff < 0:
                # Normal faster decay when going down
                self.bar_heights[i] += diff * 0.3  # Faster drop
            else:
                # Normal rise when going up
                self.bar_heights[i] += diff * self.height_smoothing  # Normal rise
            
            # Clamp to reasonable bounds
            self.bar_heights[i] = max(0, min(self.max_bar_height, self.bar_heights[i]))
        
        # Draw the actual bars
        for i in range(self.num_bars):
            x = start_x + i * (self.bar_width + self.bar_spacing)
            current_height = self.bar_heights[i]
            
            # Only draw bars if they have height
            if current_height > 0:
                # Color based on height
                height_ratio = current_height / self.max_bar_height
                if height_ratio > 0.8:
                    color = self.waveform_peak_color  # Pink for peaks
                elif height_ratio > 0.6:
                    color = "#ff6633"  # Orange-red for high
                elif height_ratio > 0.4:
                    color = "#ffaa33"  # Orange for medium-high
                elif height_ratio > 0.2:
                    color = "#66ccff"  # Light blue for medium
                else:
                    color = self.waveform_color  # Cyan for low
                
                # Upper bar (grows upward from center)
                upper_bar = self.canvas.create_rectangle(
                    x, center_y - current_height,
                    x + self.bar_width, center_y,
                    fill=color,
                    outline=""
                )
                self.waveform_bars.append(upper_bar)
                
                # Lower bar (grows downward from center) 
                lower_bar = self.canvas.create_rectangle(
                    x, center_y,
                    x + self.bar_width, center_y + current_height,
                    fill=color,
                    outline=""
                )
                self.waveform_bars.append(lower_bar)
        
        # Draw center line only when there's activity
        if any(h > 0 for h in self.bar_heights):
            baseline = self.canvas.create_rectangle(
                start_x - 20, center_y - 1,
                start_x + total_width + 20, center_y + 1,
                fill=self.waveform_color,
                outline=""
            )
            self.waveform_bars.append(baseline)
    
    def _animate_processing_pulse(self, frame):
        """gentle pulse animation for processing"""
        if not self.canvas or not self.center_circle:
            return
            
        base_color = self.colors[AIState.PROCESSING]
        intensity = 1.0 + 0.4 * math.sin(frame * 0.2)
        pulse_color = self._brighten_color(base_color, intensity)
        
        self.canvas.itemconfig(self.center_circle, fill=pulse_color, outline=pulse_color)
    
    def _animate_idle(self):
        """static display for idle state"""
        if not self.canvas or not self.center_circle:
            return
            
        color = self.colors[AIState.IDLE]
        self.canvas.itemconfig(self.center_circle, fill=color, outline=color)
    
    def _brighten_color(self, hex_color, factor):
        """brighten a hex color by factor"""
        try:
            # remove # and convert to RGB
            hex_color = hex_color.lstrip('#')
            if len(hex_color) != 6:
                return "#00ffff"  # fallback cyan
                
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16) 
            b = int(hex_color[4:6], 16)
            
            # brighten and clamp to valid range
            r = max(0, min(255, int(r * factor)))
            g = max(0, min(255, int(g * factor)))
            b = max(0, min(255, int(b * factor)))
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception as e:
            print(f"Color error: {e}, using fallback")
            return "#00ffff"  # fallback cyan
    
    def _adjust_alpha(self, hex_color, alpha_factor):
        """simulate alpha by darkening color (tkinter doesn't support alpha)"""
        try:
            hex_color = hex_color.lstrip('#')
            if len(hex_color) != 6:
                return "#004080"  # fallback dark blue
                
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16) 
            b = int(hex_color[4:6], 16)
            
            # darken to simulate transparency and clamp
            r = max(0, min(255, int(r * alpha_factor)))
            g = max(0, min(255, int(g * alpha_factor)))
            b = max(0, min(255, int(b * alpha_factor)))
            
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception as e:
            print(f"Alpha color error: {e}, using fallback")
            return "#004080"  # fallback dark blue
    
    def set_state(self, state: AIState):
        """update the AI state"""
        if self.current_state != state:
            self.current_state = state
            print(f"AI indicator: {state.value}")
            
            # always redraw elements when state changes
            if self.canvas:
                self._draw_elements()
    
    def set_idle(self):
        """convenience method for idle state"""
        self.set_audio_level(0.0)  # Always reset audio level when going idle
        self.set_state(AIState.IDLE)
    
    def set_processing(self):
        """convenience method for processing state"""
        self.set_state(AIState.PROCESSING)
    
    def set_speaking(self):
        """convenience method for speaking state"""
        self.set_state(AIState.SPEAKING)
    
    def set_audio_level(self, level):
        """update audio level for reactive animation (0.0 to 1.0)"""
        old_level = self.audio_level
        self.audio_level = max(0.0, min(1.0, level))
        if abs(old_level - self.audio_level) > 0.1:  # Only print significant changes
            print(f"Audio level: {old_level:.2f} -> {self.audio_level:.2f}")
        
        # Immediately clear waveform when audio level drops to zero
        if self.audio_level <= 0.01 and old_level > 0.01:
            self._immediate_clear_waveform()
    
    def _toggle_animation_mode(self, event=None):
        """toggle between waveform and ripples modes"""
        if self.animation_mode == "waveform":
            self.animation_mode = "ripples"
            print("Animation mode: Water Ripples")
        else:
            self.animation_mode = "waveform"
            print("Animation mode: Simple Waveform")
        
        # clear ALL animations and redraw clean
        self._clear_all_animations()
        self._draw_elements()
    
    def _clear_all_animations(self):
        """clear all animation elements"""
        # clear wave rings
        for ring in self.wave_rings:
            try:
                self.canvas.delete(ring)
            except:
                pass
        self.wave_rings.clear()
        
        # clear waveform bars
        for bar in self.waveform_bars:
            try:
                self.canvas.delete(bar)
            except:
                pass
        self.waveform_bars.clear()
    
    def _immediate_clear_waveform(self):
        """immediately clear waveform and reset bar heights"""
        if not self.canvas:
            return
        
        try:
            # Clear all visual elements immediately
            self._clear_all_animations()
            
            # Reset all bar heights to zero
            if hasattr(self, 'bar_heights'):
                for i in range(len(self.bar_heights)):
                    self.bar_heights[i] = 0
            if hasattr(self, 'target_heights'):
                for i in range(len(self.target_heights)):
                    self.target_heights[i] = 0
                    
            # Force canvas update to ensure immediate visual change
            self.canvas.update_idletasks()
        except Exception as e:
            print(f"Error clearing waveform: {e}")
    
    def _on_window_resize(self, event):
        """handle window resize events to keep animation centered"""
        # only respond to canvas resize events, not other widgets
        if event.widget == self.canvas:
            # update canvas dimensions and center coordinates
            self.canvas_width = event.width
            self.canvas_height = event.height
            self.center_x = self.canvas_width // 2
            self.center_y = self.canvas_height // 2
            
            # Update bar count for new size
            self._update_bar_count()
            
            # recalculate animation parameters based on new size
            size_factor = min(self.canvas_width, self.canvas_height) / 400
            self.base_radius = int(60 * size_factor)
            self.wave_amplitude = int(20 * size_factor)
            
            # redraw elements with new center position
            self._draw_elements()
    
    def _update_bar_count(self):
        """Update number of bars based on screen width"""
        if not self.canvas:
            return
            
        width = self.canvas.winfo_width()
        
        # Calculate how many bars we can fit
        # Leave a small margin on each side (40 pixels)
        usable_width = width - 80
        self.num_bars = max(32, usable_width // (self.bar_width + self.bar_spacing))
        
        # Update arrays if size changed
        if len(self.bar_heights) != self.num_bars:
            self.bar_heights = [self.bar_base_height] * self.num_bars
            self.target_heights = [self.bar_base_height] * self.num_bars
    
    def close(self):
        """close the GUI"""
        self.animation_running = False
        if self.window:
            self.window.quit()
            self.window = None

# global instance will be created by main.py with config
ai_indicator = None 