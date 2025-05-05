"""
Features module for the Emotion Recognition application.
"""

from .emotion_detector import EmotionDetector
from .camera_handler import CameraHandler
from .video_handler import VideoHandler
from .image_handler import ImageHandler

__all__ = [
    'EmotionDetector',
    'CameraHandler',
    'VideoHandler',
    'ImageHandler'
] 