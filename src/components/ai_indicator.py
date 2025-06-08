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
    def __init__(self, fullscreen=False, animation_mode="ripples"):
        self.fullscreen = fullscreen
        self.animation_mode = animation_mode  # "ripples" or "frequency"
        self.current_state = AIState.IDLE
        self.window = None
        self.canvas = None
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
        
        # animation parameters
        self.base_radius = 60 if not fullscreen else 120
        self.wave_count = 5
        self.wave_speed = 0.15
        self.wave_amplitude = 20 if not fullscreen else 40
        
    def start_gui(self):
        """start the GUI in a separate thread"""
        if self.window is None:
            gui_thread = threading.Thread(target=self._create_window, daemon=True)
            gui_thread.start()
            time.sleep(0.1)  # give window time to initialize
    
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
    
    def _draw_elements(self):
        """draw the main interface elements"""
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
                    else:  # frequency
                        self._animate_audio_waveform(frame)
                        
                elif self.current_state == AIState.PROCESSING:
                    # gentle pulse for processing
                    self._animate_processing_pulse(frame)
                
                else:
                    # idle - just update center circle
                    self._animate_idle()
                
                frame += 1
                time.sleep(0.033)  # 30 fps for smoother animation
                
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
        self.set_state(AIState.IDLE)
    
    def set_processing(self):
        """convenience method for processing state"""
        self.set_state(AIState.PROCESSING)
    
    def set_speaking(self):
        """convenience method for speaking state"""
        self.set_state(AIState.SPEAKING)
    
    def set_audio_level(self, level):
        """update audio level for reactive animation (0.0 to 1.0)"""
        self.audio_level = max(0.0, min(1.0, level))
    
    def _toggle_animation_mode(self, event=None):
        """toggle between ripples and frequency modes"""
        if self.animation_mode == "ripples":
            self.animation_mode = "frequency"
            print("Animation mode: Frequency Bars")
        else:
            self.animation_mode = "ripples"
            print("Animation mode: Water Ripples")
        
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
    
    def _on_window_resize(self, event):
        """handle window resize events to keep animation centered"""
        # only respond to canvas resize events, not other widgets
        if event.widget == self.canvas:
            # update canvas dimensions and center coordinates
            self.canvas_width = event.width
            self.canvas_height = event.height
            self.center_x = self.canvas_width // 2
            self.center_y = self.canvas_height // 2
            
            # recalculate animation parameters based on new size
            size_factor = min(self.canvas_width, self.canvas_height) / 400
            self.base_radius = int(60 * size_factor)
            self.wave_amplitude = int(20 * size_factor)
            
            # redraw elements with new center position
            self._draw_elements()
    
    def close(self):
        """close the GUI"""
        self.animation_running = False
        if self.window:
            self.window.quit()
            self.window = None

# global instance will be created by main.py with config
ai_indicator = None 