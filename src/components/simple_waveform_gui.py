"""
Simple Waveform Line Visualizer

A minimalist, center-aligned waveform visualizer that flexes in real time 
to simulated audio data, designed for low resource usage and clean feedback.
"""

import pygame
import math
import time
from typing import List, Tuple
import threading


class SimpleWaveformGUI:
    def __init__(self, width: int = 1200, height: int = 400):
        """
        Initialize the Simple Waveform GUI
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
        """
        self.width = width
        self.height = height
        self.center_y = height // 2
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        
        # Waveform settings
        self.num_points = 200  # Number of points across the width
        self.max_amplitude = 80  # Maximum wave height from center
        self.line_thickness = 3
        
        # Animation settings
        self.fps = 60
        self.time_offset = 0
        self.speed = 0.05  # Animation speed
        
        # Waveform data buffer
        self.waveform_data: List[float] = [0.0] * self.num_points
        
        # Pygame initialization
        pygame.init()
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("K2SO - Simple Waveform Visualizer")
        self.clock = pygame.time.Clock()
        
        # State
        self.running = False
        self.paused = False
        
    def generate_simulated_data(self) -> List[float]:
        """
        Generate simulated waveform data based on multiple sine waves
        
        Returns:
            List of amplitude values between -1.0 and 1.0
        """
        data = []
        current_time = time.time() * self.speed
        
        for i in range(self.num_points):
            # Create complex waveform with multiple frequencies
            x = i / self.num_points * 4 * math.pi + current_time
            
            # Base wave
            amplitude = 0.5 * math.sin(x)
            
            # Add harmonics for more interesting shape
            amplitude += 0.3 * math.sin(x * 2.5 + current_time * 1.5)
            amplitude += 0.2 * math.sin(x * 0.8 + current_time * 0.7)
            
            # Add some noise for realism
            amplitude += 0.1 * math.sin(x * 8 + current_time * 3)
            
            # Normalize to [-1, 1]
            amplitude = max(-1.0, min(1.0, amplitude))
            data.append(amplitude)
            
        return data
    
    def interpolate_data(self, data: List[float]) -> List[Tuple[int, int]]:
        """
        Convert amplitude data to screen coordinates with smooth interpolation
        
        Args:
            data: List of amplitude values [-1.0, 1.0]
            
        Returns:
            List of (x, y) screen coordinates
        """
        points = []
        width_step = self.width / (len(data) - 1)
        
        for i, amplitude in enumerate(data):
            x = int(i * width_step)
            y = int(self.center_y + amplitude * self.max_amplitude)
            points.append((x, y))
            
        return points
    
    def draw_waveform(self):
        """Draw the waveform line on the screen"""
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Generate new data
        self.waveform_data = self.generate_simulated_data()
        
        # Convert to screen coordinates
        points = self.interpolate_data(self.waveform_data)
        
        if len(points) >= 2:
            # Draw main waveform line in white
            pygame.draw.lines(self.screen, self.WHITE, False, points, self.line_thickness)
            
            # Highlight peaks in red
            for i, (x, y) in enumerate(points):
                amplitude = abs(self.waveform_data[i])
                if amplitude > 0.7:  # Threshold for peak highlighting
                    pygame.draw.circle(self.screen, self.RED, (x, y), self.line_thickness + 1)
        
        # Draw center reference line (very faint)
        pygame.draw.line(self.screen, (20, 20, 20), (0, self.center_y), (self.width, self.center_y), 1)
    
    def handle_resize(self, new_size: Tuple[int, int]):
        """Handle window resize events"""
        self.width, self.height = new_size
        self.center_y = self.height // 2
        self.screen = pygame.display.set_mode(new_size, pygame.RESIZABLE)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_UP:
                    self.max_amplitude = min(self.height // 2 - 10, self.max_amplitude + 10)
                elif event.key == pygame.K_DOWN:
                    self.max_amplitude = max(10, self.max_amplitude - 10)
                elif event.key == pygame.K_RIGHT:
                    self.speed = min(0.2, self.speed + 0.01)
                elif event.key == pygame.K_LEFT:
                    self.speed = max(0.01, self.speed - 0.01)
                    
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize((event.w, event.h))
    
    def run(self):
        """Main loop for the waveform visualizer"""
        self.running = True
        print("K2SO Simple Waveform Visualizer")
        print("Controls:")
        print("  SPACE - Pause/Resume")
        print("  UP/DOWN - Adjust amplitude")
        print("  LEFT/RIGHT - Adjust speed")
        print("  ESC - Exit")
        
        while self.running:
            self.handle_events()
            
            if not self.paused:
                self.draw_waveform()
                
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        pygame.quit()
    
    def start_threaded(self):
        """Start the visualizer in a separate thread"""
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        return self.thread
    
    def stop(self):
        """Stop the visualizer"""
        self.running = False


def main():
    """Test runner for the Simple Waveform GUI"""
    visualizer = SimpleWaveformGUI()
    try:
        visualizer.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        visualizer.stop()


if __name__ == "__main__":
    main() 