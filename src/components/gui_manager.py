"""
GUI Manager - Lite Mode Implementation

Main controller for K2SO's context-aware GUI system.
Coordinates between animation displays (waveform/ripples) and information screens.
"""

import tkinter as tk
from enum import Enum
from typing import Optional, Dict, Any
import threading
import time
from .ai_indicator import AIIndicator, AIState
import random


class DisplayMode(Enum):
    """Available display modes for the GUI"""
    ANIMATION = "animation"      # Waveform or ripples
    CALENDAR = "calendar"        # Calendar view
    TASKS = "tasks"             # Task/shopping lists
    SETTINGS = "settings"       # Configuration panel
    CHAT = "chat"               # Chat history (optional)


class GUIManager:
    """
    Main GUI controller for Lite Mode implementation.
    Manages display switching, state coordination, and context awareness.
    """
    
    def __init__(self, fullscreen: bool = False, animation_mode: str = "waveform"):
        """
        Initialize the GUI Manager
        
        Args:
            fullscreen: Whether to run in fullscreen mode
            animation_mode: Default animation mode ("waveform", "ripples", "frequency")
        """
        self.fullscreen = fullscreen
        self.animation_mode = animation_mode
        self.current_display = DisplayMode.ANIMATION
        self.previous_display = DisplayMode.ANIMATION
        
        # GUI components
        self.root: Optional[tk.Tk] = None
        self.main_frame: Optional[tk.Frame] = None
        self.ai_indicator: Optional[AIIndicator] = None
        
        # Display frames
        self.frames: Dict[DisplayMode, tk.Frame] = {}
        
        # State management
        self.running = False
        self.auto_return_timer: Optional[threading.Timer] = None
        self.auto_return_delay = 30.0  # seconds
        
        # Context switching
        self.context_keywords = {
            "calendar": DisplayMode.CALENDAR,
            "schedule": DisplayMode.CALENDAR,
            "appointments": DisplayMode.CALENDAR,
            "tasks": DisplayMode.TASKS,
            "todo": DisplayMode.TASKS,
            "shopping": DisplayMode.TASKS,
            "list": DisplayMode.TASKS,
            "settings": DisplayMode.SETTINGS,
            "preferences": DisplayMode.SETTINGS,
            "config": DisplayMode.SETTINGS,
            "chat": DisplayMode.CHAT,
            "history": DisplayMode.CHAT,
            "conversation": DisplayMode.CHAT,
        }
    
    def start(self):
        """Start the GUI Manager"""
        if not self.running:
            self.running = True
            self._create_gui()  # Create GUI directly in main thread
            
    def _create_gui(self):
        """Create the main GUI window and components"""
        if self.root is not None:
            return
            
        self.root = tk.Tk()
        self.root.title("K2SO - Personal Assistant")
        self.root.configure(bg='black')
        
        if self.fullscreen:
            self.root.attributes('-fullscreen', True)
            self.root.configure(cursor='none')
        else:
            self.root.geometry("1000x700")
            
        # Create main container
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Initialize display frames
        self._create_frames()
        
        # Key bindings
        self.root.bind('<Escape>', self._handle_escape)
        self.root.bind('<F1>', lambda e: self.switch_display(DisplayMode.CALENDAR))
        self.root.bind('<F2>', lambda e: self.switch_display(DisplayMode.TASKS))
        self.root.bind('<F3>', lambda e: self.switch_display(DisplayMode.SETTINGS))
        self.root.bind('<F4>', lambda e: self.switch_display(DisplayMode.CHAT))
        self.root.bind('<space>', self._handle_spacebar)
        self.root.focus_set()
        
        # Start with animation display and ensure it's visible
        self.frames[DisplayMode.ANIMATION].pack(fill=tk.BOTH, expand=True)
        self.root.update_idletasks()  # Force geometry update
        
        # Start the animation
        if self.ai_indicator:
            self.ai_indicator.start_gui()
            self.ai_indicator.set_speaking()
            
    def _create_frames(self):
        """Create all display frames"""
        # Animation frame (AI Indicator)
        self.ai_indicator = AIIndicator(
            parent=self.main_frame,
            fullscreen=self.fullscreen,
            animation_mode=self.animation_mode
        )
        self.frames[DisplayMode.ANIMATION] = self.ai_indicator.get_frame()
        
        # Information display frames
        self.frames[DisplayMode.CALENDAR] = self._create_calendar_frame()
        self.frames[DisplayMode.TASKS] = self._create_tasks_frame()
        self.frames[DisplayMode.SETTINGS] = self._create_settings_frame()
        self.frames[DisplayMode.CHAT] = self._create_chat_frame()
        
        # Initially hide all frames except animation
        for mode, frame in self.frames.items():
            if mode != DisplayMode.ANIMATION:
                frame.pack_forget()
    
    def _create_calendar_frame(self) -> tk.Frame:
        """Create calendar display frame"""
        frame = tk.Frame(self.main_frame, bg='black')
        
        # Title
        title = tk.Label(
            frame, 
            text="📅 Calendar", 
            font=("Arial", 24, "bold"),
            fg='white', 
            bg='black'
        )
        title.pack(pady=20)
        
        # Calendar content placeholder
        content = tk.Text(
            frame,
            font=("Arial", 14),
            bg='#1a1a1a',
            fg='white',
            height=20,
            width=80,
            wrap=tk.WORD
        )
        content.insert(tk.END, "Calendar functionality will be implemented here.\n\n")
        content.insert(tk.END, "Upcoming events:\n")
        content.insert(tk.END, "• Meeting at 2 PM\n")
        content.insert(tk.END, "• Doctor appointment tomorrow\n")
        content.pack(pady=20)
        
        # Back button
        back_btn = tk.Button(
            frame,
            text="← Back to Animation",
            font=("Arial", 12),
            command=lambda: self.switch_display(DisplayMode.ANIMATION),
            bg='#333333',
            fg='white'
        )
        back_btn.pack(pady=10)
        
        return frame
    
    def _create_tasks_frame(self) -> tk.Frame:
        """Create tasks/shopping list frame"""
        frame = tk.Frame(self.main_frame, bg='black')
        
        # Title
        title = tk.Label(
            frame,
            text="📝 Tasks & Lists",
            font=("Arial", 24, "bold"),
            fg='white',
            bg='black'
        )
        title.pack(pady=20)
        
        # Tasks content
        content = tk.Text(
            frame,
            font=("Arial", 14),
            bg='#1a1a1a',
            fg='white',
            height=20,
            width=80,
            wrap=tk.WORD
        )
        content.insert(tk.END, "Tasks and shopping lists will be managed here.\n\n")
        content.insert(tk.END, "TODO:\n")
        content.insert(tk.END, "☐ Buy groceries\n")
        content.insert(tk.END, "☐ Schedule dentist appointment\n")
        content.insert(tk.END, "☐ Review project documentation\n\n")
        content.insert(tk.END, "SHOPPING LIST:\n")
        content.insert(tk.END, "• Milk\n")
        content.insert(tk.END, "• Bread\n")
        content.insert(tk.END, "• Batteries\n")
        content.pack(pady=20)
        
        # Back button
        back_btn = tk.Button(
            frame,
            text="← Back to Animation",
            font=("Arial", 12),
            command=lambda: self.switch_display(DisplayMode.ANIMATION),
            bg='#333333',
            fg='white'
        )
        back_btn.pack(pady=10)
        
        return frame
    
    def _create_settings_frame(self) -> tk.Frame:
        """Create settings panel frame"""
        frame = tk.Frame(self.main_frame, bg='black')
        
        # Title
        title = tk.Label(
            frame,
            text="⚙️ Settings",
            font=("Arial", 24, "bold"),
            fg='white',
            bg='black'
        )
        title.pack(pady=20)
        
        # Settings content
        settings_frame = tk.Frame(frame, bg='black')
        settings_frame.pack(pady=20)
        
        # Animation mode setting
        tk.Label(
            settings_frame,
            text="Animation Mode:",
            font=("Arial", 14),
            fg='white',
            bg='black'
        ).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        
        mode_var = tk.StringVar(value=self.animation_mode)
        mode_menu = tk.OptionMenu(
            settings_frame,
            mode_var,
            "waveform", "ripples", "frequency"
        )
        mode_menu.grid(row=0, column=1, padx=10, pady=5)
        
        # Auto-return delay setting
        tk.Label(
            settings_frame,
            text="Auto-return delay (seconds):",
            font=("Arial", 14),
            fg='white',
            bg='black'
        ).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        
        delay_var = tk.IntVar(value=int(self.auto_return_delay))
        delay_spin = tk.Spinbox(
            settings_frame,
            from_=5,
            to=300,
            textvariable=delay_var,
            width=10
        )
        delay_spin.grid(row=1, column=1, padx=10, pady=5)
        
        # Apply button
        apply_btn = tk.Button(
            settings_frame,
            text="Apply Settings",
            font=("Arial", 12),
            command=lambda: self._apply_settings(mode_var.get(), delay_var.get()),
            bg='#0066cc',
            fg='white'
        )
        apply_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Back button
        back_btn = tk.Button(
            frame,
            text="← Back to Animation",
            font=("Arial", 12),
            command=lambda: self.switch_display(DisplayMode.ANIMATION),
            bg='#333333',
            fg='white'
        )
        back_btn.pack(pady=10)
        
        return frame
    
    def _create_chat_frame(self) -> tk.Frame:
        """Create chat history frame"""
        frame = tk.Frame(self.main_frame, bg='black')
        
        # Title
        title = tk.Label(
            frame,
            text="💬 Chat History",
            font=("Arial", 24, "bold"),
            fg='white',
            bg='black'
        )
        title.pack(pady=20)
        
        # Chat content
        content = tk.Text(
            frame,
            font=("Arial", 12),
            bg='#1a1a1a',
            fg='white',
            height=25,
            width=100,
            wrap=tk.WORD
        )
        content.insert(tk.END, "Chat history will be displayed here.\n\n")
        content.insert(tk.END, "User: Hello K2SO\n")
        content.insert(tk.END, "K2SO: Hello! How can I assist you today?\n\n")
        content.insert(tk.END, "User: What's the weather like?\n")
        content.insert(tk.END, "K2SO: I'd need internet access to check current weather conditions.\n\n")
        content.pack(pady=20)
        
        # Back button
        back_btn = tk.Button(
            frame,
            text="← Back to Animation",
            font=("Arial", 12),
            command=lambda: self.switch_display(DisplayMode.ANIMATION),
            bg='#333333',
            fg='white'
        )
        back_btn.pack(pady=10)
        
        return frame
    
    def switch_display(self, mode: DisplayMode, auto_return: bool = True):
        """
        Switch to a different display mode
        
        Args:
            mode: The display mode to switch to
            auto_return: Whether to automatically return to animation after timeout
        """
        if mode == self.current_display:
            return
            
        # Hide current frame
        if self.current_display in self.frames:
            self.frames[self.current_display].pack_forget()
        
        # Store previous display for potential return
        if self.current_display != DisplayMode.ANIMATION:
            self.previous_display = self.current_display
        
        # Show new frame
        self.current_display = mode
        if mode in self.frames:
            self.frames[mode].pack(fill=tk.BOTH, expand=True)
            
            # Start AI indicator animation if switching to animation mode
            if mode == DisplayMode.ANIMATION and self.ai_indicator:
                self.ai_indicator.start_gui()
                self.ai_indicator.set_speaking()  # Ensure animation is visible
                self.frames[mode].update()  # Force frame update
        
        # Set auto-return timer for non-animation modes
        if auto_return and mode != DisplayMode.ANIMATION:
            self._start_auto_return_timer()
        else:
            self._cancel_auto_return_timer()
            
        print(f"Switched to {mode.value} display")
    
    def handle_context_trigger(self, text: str):
        """
        Handle context-based display switching from AI conversation
        
        Args:
            text: Text to analyze for context keywords
        """
        text_lower = text.lower()
        
        for keyword, mode in self.context_keywords.items():
            if keyword in text_lower:
                self.switch_display(mode)
                return True
        
        return False
    
    def set_ai_state(self, state: AIState):
        """Update AI state for animation display"""
        if self.ai_indicator:
            self.ai_indicator.set_state(state)
    
    def set_audio_level(self, level: float):
        """Update audio level for animation display"""
        if self.ai_indicator:
            self.ai_indicator.set_audio_level(level)
    
    def _apply_settings(self, animation_mode: str, auto_return_delay: int):
        """Apply settings changes"""
        self.animation_mode = animation_mode
        self.auto_return_delay = float(auto_return_delay)
        
        if self.ai_indicator:
            self.ai_indicator.animation_mode = animation_mode
            
        print(f"Settings applied: mode={animation_mode}, delay={auto_return_delay}s")
    
    def _start_auto_return_timer(self):
        """Start timer to automatically return to animation display"""
        self._cancel_auto_return_timer()
        
        self.auto_return_timer = threading.Timer(
            self.auto_return_delay,
            lambda: self.switch_display(DisplayMode.ANIMATION, auto_return=False)
        )
        self.auto_return_timer.start()
    
    def _cancel_auto_return_timer(self):
        """Cancel any active auto-return timer"""
        if self.auto_return_timer:
            self.auto_return_timer.cancel()
            self.auto_return_timer = None
    
    def _handle_escape(self, event):
        """Handle escape key press"""
        if self.fullscreen:
            self.stop()
        else:
            self.switch_display(DisplayMode.ANIMATION)
    
    def _handle_spacebar(self, event):
        """Handle spacebar press for animation mode switching"""
        if self.current_display == DisplayMode.ANIMATION and self.ai_indicator:
            self.ai_indicator._toggle_animation_mode()
    
    def stop(self):
        """Stop the GUI Manager"""
        self.running = False
        self._cancel_auto_return_timer()
        
        if self.ai_indicator:
            self.ai_indicator.close()
            
        if self.root:
            self.root.quit()
            self.root.destroy()


def main():
    """Test runner for the GUI Manager"""
    print("Starting K2SO GUI Manager (Lite Mode)")
    print("Controls:")
    print("  F1 - Calendar")
    print("  F2 - Tasks")
    print("  F3 - Settings")
    print("  F4 - Chat")
    print("  SPACE - Toggle animation mode")
    print("  ESC - Exit")
    
    # Create and start GUI
    gui = GUIManager(fullscreen=False, animation_mode="waveform")
    gui.start()
    
    # Simulate some audio activity for testing
    def update_audio():
        while gui.running:
            if gui.ai_indicator and gui.ai_indicator.current_state == AIState.SPEAKING:
                # Simulate varying audio levels
                gui.ai_indicator.set_audio_level(random.uniform(0.3, 1.0))
            time.sleep(0.1)
    
    try:
        if gui.root:
            # Start audio simulation in background
            audio_thread = threading.Thread(target=update_audio, daemon=True)
            audio_thread.start()
            
            # Set initial state to speaking for demo
            if gui.ai_indicator:
                gui.ai_indicator.set_speaking()
            
            # Start main loop
            gui.root.mainloop()
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        gui.stop()


if __name__ == "__main__":
    main() 