from fer import FER
import cv2

class EmotionDetector:
    def __init__(self):
        self.detector = FER()

    def detect_emotions(self, frame):
        """Nhận diện cảm xúc trong frame"""
        return self.detector.detect_emotions(frame)

    def process_frame(self, frame, scale=1.0):
        """Xử lý frame và trả về kết quả nhận diện"""
        results = self.detect_emotions(frame)
        return self.draw_results(frame, results, scale)

    def draw_results(self, frame, results, scale=1.0):
        """Vẽ kết quả nhận diện lên frame"""
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