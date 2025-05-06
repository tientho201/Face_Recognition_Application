# Emotion Recognition Application

Ứng dụng nhận diện cảm xúc sử dụng Python Cv2 và Tkinter.

## Mô tả

Đây là một ứng dụng nhận diện cảm xúc được xây dựng bằng Python, sử dụng Tkinter cho giao diện người dùng và sử dụng model Fer2013 để nhận diện cảm xúc. Ứng dụng có khả năng nhận diện cảm xúc từ hình ảnh, video stream hoặc camera trực tiếp.

## Yêu cầu hệ thống

- Python 3.10 trở lên
- Webcam (để sử dụng tính năng nhận diện cảm xúc qua camera)
- Đủ dung lượng ổ cứng để cài đặt các thư viện cần thiết

## Cài đặt

1. Clone repository này về máy của bạn:
```bash
git clone https://github.com/tientho201/Face_Recognition_Application.git
```

2. Tạo và kích hoạt môi trường ảo (khuyến nghị):
```bash
python -m venv .venv
# Trên Windows
.venv\Scripts\activate
# Trên Linux/Mac
source .venv/bin/activate
```

3. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Sử dụng

1. Kích hoạt môi trường ảo (nếu chưa kích hoạt):
```bash
# Trên Windows
.venv\Scripts\activate
# Trên Linux/Mac
source .venv/bin/activate
```

2. Chạy ứng dụng:
```bash
python main.py
```

3. Sử dụng giao diện:
   - Chọn các chức năng cần nhận diện như image, video, camera

## Cấu trúc thư mục

```
.
├── main.py              # Điểm khởi đầu của ứng dụng
├── requirements.txt     # Danh sách các thư viện cần thiết
├── src/                 # Thư mục chứa mã nguồn
|   ├── assets/          # Thư mục chứa các tài nguyên như hình ảnh
│   ├── gui/             # Thư mục chứa các thành phần giao diện người dùng
|   ├── features/        # Thư mục chứa các tính năng chính của ứng dụng
│   └── utils/           # Thư mục chứa các tiện ích và hàm hỗ trợ
└── README.md            # Tài liệu hướng dẫn
```

## Xử lý lỗi thường gặp

1. Nếu gặp lỗi khi cài đặt thư viện:
   - Đảm bảo bạn đang sử dụng Python phiên bản 3.10 trở lên
   - Thử cập nhật pip: `python -m pip install --upgrade pip`
   - Cài đặt lại các thư viện: `pip install -r requirements.txt`

2. Nếu không nhận diện được webcam:
   - Kiểm tra xem webcam đã được kết nối đúng cách chưa
   - Đảm bảo không có ứng dụng nào khác đang sử dụng webcam
   - Kiểm tra quyền truy cập webcam trong hệ điều hành

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo issue hoặc pull request để đóng góp.
