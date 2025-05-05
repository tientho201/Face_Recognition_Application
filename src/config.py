"""
Configuration settings for the Emotion Recognition application.
"""

import os

# Directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, 'src', 'assets')
IMG_DIR = os.path.join(ASSETS_DIR, 'img')

# Window settings
WINDOW_TITLE = "Emotion Recognition"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Color configuration
COLORS = {
    'WHITE': '#FFFFFF',
    'BLACK': '#000000',
    'LIGHT_GREY': '#F0F0F0',
    'DARK_GREY': '#333333',
    'BLUE': '#007BFF',
    'RED': '#DC3545',
    'GREEN': '#28A745',
    'YELLOW': '#FFC107',
    'PINK': '#FF69B4',
    'LIGHT_BLUE': '#ADD8E6',
    'LIGHT_YELLOW': '#FFFACD'
}

# Font configuration
FONTS = {
    'title': ('Helvetica', 24, 'bold'),
    'subtitle': ('Helvetica', 18),
    'button': ('Helvetica', 14),
    'menu': ('Helvetica', 12),
    'label': ('Helvetica', 10)
}

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'] 