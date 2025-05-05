import tkinter as tk
import os
import ctypes
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, IMG_DIR

def center_window(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
    """Đặt cửa sổ ở giữa màn hình"""
    # Lấy kích thước màn hình
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Tính toán tọa độ để đặt cửa sổ ở giữa màn hình
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    # Đặt kích thước và vị trí cửa sổ
    window.geometry(f"{width}x{height}+{x}+{y}")

def set_icon_window(window):
    """Đặt icon cho cửa sổ"""
    from src.utils.style_utils import check_icon
    
    icon_path = os.path.join(IMG_DIR, "emotion.png")
    icon = check_icon(icon_path)
    window.iconphoto(False, icon)

    if os.name == 'nt':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('mycompany.myproduct.subproduct.version')
        window.iconbitmap(default=os.path.join(IMG_DIR, 'emotion.ico'))

def print_error_input(frm_mid, announce):
    """Hiển thị thông báo lỗi"""
    frm_mid.update_idletasks()  # Đảm bảo frm_mid có kích thước trước khi gọi
    # Xóa nội dung cũ trong `frm_mid`  
    for widget in frm_mid.winfo_children():  
        widget.destroy() 

    frm_mid.update_idletasks()
    # Thông báo lỗi
    label = tk.Label(
        master=frm_mid,
        text=announce,
        font=("Helvetica", 18),
        fg="red",
        wraplength=frm_mid.winfo_width() - 20,
        justify='center'
    )
    label.pack(fill="both", expand=True)
    # Update wraplength on resize  
    frm_mid.bind("<Configure>", lambda event: update_error_wrap_length(frm_mid, label))  

def update_error_wrap_length(frm_mid, error_label):  
    """Cập nhật độ dài tối đa của text khi resize"""
    error_label.config(wraplength=frm_mid.winfo_width() - 20) 