"""
Image handler for processing image files.
"""

import cv2
import numpy as np
from PIL import Image, ImageTk
from tkinter import messagebox
from .emotion_detector import EmotionDetector
from ..utils import resize_image, convert_cv2_to_tk, draw_emotion_results, add_box_shadow

class ImageHandler:
    """Handler class for processing image files."""
    
    def __init__(self):
        """Initialize image handler with emotion detector."""
        self.detector = EmotionDetector()
        self.original_frame = None
        self.processed_frame = None
        
    def process_image(self, file_path, frame, callback):
        """Process an image file and detect emotions."""
        try:
            # Read image
            img = cv2.imread(file_path)
            if img is None:
                error_msg = f"Lỗi: Không thể đọc ảnh\n\nChi tiết lỗi:\nKhông thể đọc ảnh từ đường dẫn:\n{file_path}\n\nVui lòng kiểm tra lại đường dẫn và chọn ảnh khác."
                messagebox.showerror("Lỗi đọc ảnh", error_msg)
                return
                
            # Store original frame
            self.original_frame = img.copy()
            
            # Detect emotions
            results = self.detector.detect_emotions(img)
            
            # Draw results on frame
            self.processed_frame = draw_emotion_results(img, results)
            
            # Convert frames to Tkinter format
            original_img = self._convert_to_tk(self.original_frame, frame)
            processed_img = self._convert_to_tk(self.processed_frame, frame)
            
            # Call callback with both images
            callback(original_img, processed_img)
            
        except Exception as e:
            error_msg = f"Lỗi: Không thể xử lý ảnh\n\nChi tiết lỗi:\n{str(e)}\n\nVui lòng thử lại."
            messagebox.showerror("Lỗi xử lý ảnh", error_msg)
            
    def _convert_to_tk(self, frame, target_frame):
        """Convert OpenCV frame to Tkinter image with shadow effect."""
        try:
            # Resize frame to fit target frame
            resized = resize_image(frame, target_frame.winfo_height())
            
            # Convert to PIL Image
            img = Image.fromarray(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
            
            # Add shadow effect
            img_with_shadow = add_box_shadow(img, offset=(2, 2), blur_radius=4, shadow_color=(0, 0, 0, 77))
            
            # Convert to Tkinter format
            return ImageTk.PhotoImage(image=img_with_shadow)
        except Exception as e:
            error_msg = f"Lỗi: Không thể chuyển đổi ảnh\n\nChi tiết lỗi:\n{str(e)}\n\nVui lòng thử lại."
            messagebox.showerror("Lỗi chuyển đổi ảnh", error_msg)
            return None 