import tkinter as tk
from src.config import COLORS

# Danh sách lưu trữ hình ảnh để tránh bị xóa bởi garbage collector
image_reference = []

def check_icon(file_path):
    """Kiểm tra và tải icon"""
    import os
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image file '{file_path}' not found.")

    img = tk.PhotoImage(file=file_path)
    image_reference.append(img)  # Lưu trữ hình ảnh để không bị xóa
    return img

def fade_color(start_color, end_color, steps, widget):
    """Create a smooth color transition effect."""
    start_rgb = widget.winfo_rgb(start_color)
    end_rgb = widget.winfo_rgb(end_color)

    delta_r = (end_rgb[0] - start_rgb[0]) // steps
    delta_g = (end_rgb[1] - start_rgb[1]) // steps
    delta_b = (end_rgb[2] - start_rgb[2]) // steps

    colors = [
        f"#{max(0, min(255, (start_rgb[0] + i * delta_r) // 256)):02x}"
        f"{max(0, min(255, (start_rgb[1] + i * delta_g) // 256)):02x}"
        f"{max(0, min(255, (start_rgb[2] + i * delta_b) // 256)):02x}"
        for i in range(steps + 1)
    ]

    def update_color(index=0):
        if index < len(colors):
            widget.config(bg=colors[index])
            widget.after(30, update_color, index + 1)

    update_color()

def on_enter(e, inColor, outColor):
    """Xử lý sự kiện khi hover vào"""
    fade_color(inColor, outColor, 10, e)

def on_leave(e, inColor, outColor):
    """Xử lý sự kiện khi hover ra"""
    fade_color(outColor, inColor, 10, e)

def add_box_shadow(image, offset=(2, 2), blur_radius=4, shadow_color=(0, 0, 0, 77)):
    """Thêm hiệu ứng bóng đổ cho ảnh"""
    from PIL import Image, ImageFilter, ImageDraw
    
    # Chuyển đổi ảnh sang RGBA nếu chưa đúng định dạng
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    
    # Kích thước ảnh gốc
    width, height = image.size

    # Tạo ảnh nền với bóng đổ
    shadow = Image.new(
        "RGBA",
        (width + abs(offset[0]) + blur_radius * 2, height + abs(offset[1]) + blur_radius * 2),
        (0, 0, 0, 0)  # Trong suốt
    )

    shadow_draw = ImageDraw.Draw(shadow)

    # Tạo hình chữ nhật tương ứng với ảnh, thêm shadow
    shadow_draw.rectangle(
        [blur_radius, blur_radius, width + blur_radius, height + blur_radius],
        fill=shadow_color
    )

    # Làm mờ bóng đổ
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

    # Chèn ảnh gốc lên trên bóng
    shadow.paste(image, (blur_radius + offset[0], blur_radius + offset[1]), mask=image)
    
    return shadow 