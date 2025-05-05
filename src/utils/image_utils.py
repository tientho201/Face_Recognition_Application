import cv2
import numpy as np
from PIL import Image, ImageTk
from src.config import IMG_DIR
import os

def resize_image(frame, target_height):
    """Resize ảnh theo chiều cao mục tiêu"""
    height, width = frame.shape[:2]
    scale = target_height / height
    new_width = int(width * scale)
    return cv2.resize(frame, (new_width, target_height))

def convert_cv2_to_tk(frame):
    """Chuyển đổi ảnh OpenCV sang định dạng Tkinter"""
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    return ImageTk.PhotoImage(image=img)

def draw_emotion_results(frame, results, scale=1.0):
    """Vẽ kết quả nhận diện cảm xúc lên ảnh"""
    if results:
        for face in results:
            x, y, w, h = face['box']
            x, y, w, h = int(x * scale), int(y * scale), int(w * scale), int(h * scale)
            top_emotion = max(face["emotions"], key=face["emotions"].get)
            percent = max(face["emotions"].values())

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{top_emotion} {percent*100:.0f}%", 
                       (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "No face detected", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return frame

def load_default_image(img_name):
    """Tải ảnh mặc định từ thư mục assets"""
    img_path = os.path.join(IMG_DIR, img_name)
    return Image.open(img_path) 