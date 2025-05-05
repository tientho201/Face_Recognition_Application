import cv2
import time
from tkinter import messagebox
from src.features.emotion_detector import EmotionDetector
from src.utils.image_utils import resize_image, convert_cv2_to_tk

class CameraHandler:
    def __init__(self):
        self.cap = None
        self.detector = EmotionDetector()
        self.update_task = None
        self.detect_closed = False

    def start_camera(self, frm_mid, update_callback):
        """Khởi động camera"""
        if self.cap is not None:
            self.stop_camera()

        self.detect_closed = False  # Reset the flag
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            error_msg = f"Lỗi: Không thể mở camera\n\nChi tiết lỗi:\nKhông thể kết nối với camera.\n\nVui lòng kiểm tra:\n- Camera có được kết nối không\n- Camera có đang được sử dụng bởi ứng dụng khác không\n- Quyền truy cập camera đã được cấp chưa"
            messagebox.showerror("Lỗi mở camera", error_msg)
            return False

        def update_frame():
            if self.detect_closed:
                self.detect_closed = False
                return

            ret, frame = self.cap.read()
            if not ret:
                self.stop_camera()
                return

            # Resize frame
            frame = resize_image(frame, frm_mid.winfo_height())
            
            # Process frame
            frame = self.detector.process_frame(frame)
            
            # Convert to Tkinter format
            img_tk = convert_cv2_to_tk(frame)
            
            # Update display
            update_callback(img_tk)
            
            # Schedule next update
            self.update_task = frm_mid.after(20, update_frame)

        update_frame()
        return True

    def stop_camera(self):
        """Dừng camera"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        if self.update_task is not None:
            self.update_task = None
        self.detect_closed = True 