"""
Main entry point for the Emotion Recognition application.
"""

import tkinter as tk
from src.gui import MainWindow
from src.utils import center_window, set_icon_window

def main():
    """Initialize and run the Emotion Recognition application."""
    # Create main window
    window = MainWindow()
    
    # Set window icon
    set_icon_window(window)
    
    # Center window on screen
    center_window(window)
    
    # Start the application
    window.mainloop()

if __name__ == "__main__":
    main() 