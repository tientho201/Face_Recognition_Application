import cv2
from tkinter import messagebox
from src.features.emotion_detector import EmotionDetector
from src.utils.image_utils import resize_image, convert_cv2_to_tk

class VideoHandler:
    def __init__(self):
        self.cap = None
        self.detector = EmotionDetector()
        self.update_task = None
        self.detect_closed = False

    def start_video(self, file_path, frm_mid, update_callback):
        """Khởi động video"""
        if self.cap is not None:
            self.stop_video()

        self.detect_closed = False  # Reset the flag
        self.cap = cv2.VideoCapture(file_path)
        if not self.cap.isOpened():
            error_msg = f"Lỗi: Không thể đọc video\n\nChi tiết lỗi:\nKhông thể đọc video từ đường dẫn:\n{file_path}\n\nVui lòng kiểm tra lại đường dẫn và chọn video khác."
            messagebox.showerror("Lỗi đọc video", error_msg)
            return False

        # Lấy thông tin xoay của frame
        rotation = self.cap.get(cv2.CAP_PROP_ORIENTATION_META)

        def update_frame():
            if self.detect_closed:
                self.detect_closed = False
                return

            ret, frame = self.cap.read()
            if not ret:
                self.stop_video()
                return

            # Xử lý xoay frame nếu cần
            if rotation == 90:
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            elif rotation == 180:
                frame = cv2.rotate(frame, cv2.ROTATE_180)
            elif rotation == 270:
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Resize frame
            frame = resize_image(frame, frm_mid.winfo_height())
            
            # Process frame
            frame = self.detector.process_frame(frame)
            
            # Convert to Tkinter format
            img_tk = convert_cv2_to_tk(frame)
            
            # Update display
            update_callback(img_tk)
            
            # Schedule next update
            self.update_task = frm_mid.after(15, update_frame)

        update_frame()
        return True

    def stop_video(self):
        """Dừng video"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        if self.update_task is not None:
            self.update_task = None
        self.detect_closed = True 