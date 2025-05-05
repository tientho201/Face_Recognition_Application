"""
Main window for the Emotion Recognition application.
"""

import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk
from ..utils import check_icon, on_enter, on_leave, center_window, set_icon_window
from ..config import COLORS, FONTS, IMG_DIR, WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from .camera_window import CameraWindow
from .video_window import VideoWindow
from .image_window import ImageWindow


class MainWindow(tk.Tk):
    """Main window class for the Emotion Recognition application."""
    
    def __init__(self):
        super().__init__()

        # Configure window
        self.title(WINDOW_TITLE)
        self.configure(bg=COLORS['WHITE'])

        # Set window geometry
        self.rowconfigure(0, minsize=WINDOW_HEIGHT , weight=1)
        self.columnconfigure(1, minsize=WINDOW_WIDTH, weight=1)

        # Create frames
        self._create_left_menu()
        self._create_content_frame()

    def _create_left_menu(self):
        """Create the left menu frame."""
        self.left_frm = tk.Frame(master=self, relief=tk.RAISED, bd=2, bg=COLORS['LIGHT_GREY'])
        self.left_frm.rowconfigure(1, minsize=50)
        self.left_frm.columnconfigure(0, minsize=50)

        # Icons
        menu_icon = check_icon(os.path.join(IMG_DIR, "menu.png"))
        img_icon = check_icon(os.path.join(IMG_DIR, "btn_img.png"))
        video_icon = check_icon(os.path.join(IMG_DIR, "btn_video.png"))
        cam_icon = check_icon(os.path.join(IMG_DIR, "btn_camera.png"))

        # Menu label
        lbl_menu = tk.Label(
            master=self.left_frm,
            text="Menu",
            image=menu_icon,
            compound=tk.LEFT,
            padx=10,
            pady=10,
            font=FONTS['menu']
        )

        # Button frame
        btn_frm = tk.Frame(master=self.left_frm)

        # Image button
        btn_img = tk.Button(
            master=btn_frm,
            image=img_icon,
            compound=tk.LEFT,
            text="Image",
            padx=10,
            bg=COLORS['PINK'],
            fg=COLORS['BLACK'],
            font=FONTS['button'],
            command=lambda: ImageWindow(self),
            cursor="hand2"
        )
        btn_img.bind("<Enter>", lambda e: on_enter(btn_img, COLORS['PINK'], COLORS['RED']))
        btn_img.bind("<Leave>", lambda e: on_leave(btn_img, COLORS['PINK'], COLORS['RED']))

        # Video button
        btn_vid = tk.Button(
            master=btn_frm,
            image=video_icon,
            compound=tk.LEFT,
            text="Video",
            padx=10,
            bg=COLORS['LIGHT_YELLOW'],
            fg=COLORS['BLACK'],
            font=FONTS['button'],
            command=lambda: VideoWindow(self),
            cursor="hand2"
        )
        btn_vid.bind("<Enter>", lambda e: on_enter(btn_vid, COLORS['LIGHT_YELLOW'], COLORS['YELLOW']))
        btn_vid.bind("<Leave>", lambda e: on_leave(btn_vid, COLORS['LIGHT_YELLOW'], COLORS['YELLOW']))

        # Camera button
        btn_cam = tk.Button(
            master=btn_frm,
            image=cam_icon,
            compound=tk.LEFT,
            text="Camera",
            padx=10,
            bg=COLORS['LIGHT_BLUE'],
            fg=COLORS['BLACK'],
            font=FONTS['button'],
            command=lambda: CameraWindow(self),
            cursor="hand2"
        )
        btn_cam.bind("<Enter>", lambda e: on_enter(btn_cam, COLORS['LIGHT_BLUE'], COLORS['BLUE']))
        btn_cam.bind("<Leave>", lambda e: on_leave(btn_cam, COLORS['LIGHT_BLUE'], COLORS['BLUE']))

        # Add buttons to frame
        btn_img.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        btn_vid.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        btn_cam.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        # Add to layout
        lbl_menu.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        btn_frm.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        # Add to main window
        self.left_frm.grid(row=0, column=0, sticky="ns")

    def _create_content_frame(self):
        """Create the content frame with background image and dynamic text."""
        self.content_frm = tk.Frame(master=self)
        self.content_frm.grid(row=0, column=1, sticky="nsew")

        self.content_frm.rowconfigure(0, weight=1)
        self.content_frm.columnconfigure(0, weight=1)

        # Canvas
        canvas = tk.Canvas(master=self.content_frm, bg='white')
        canvas.grid(row=0, column=0, sticky="nsew")

        # Load image
        bg_img_path = os.path.join(IMG_DIR, "bg3.png")
        self.original_img = Image.open(bg_img_path)
        self.original_width, self.original_height = self.original_img.size

        # Initial image
        resized_img = self.original_img.copy()
        photo = ImageTk.PhotoImage(resized_img)
        canvas.bg_image = photo
        image_id = canvas.create_image(0, 0, anchor='center', image=photo)

        # Add text
        text1_id = canvas.create_text(0, 0, text="Emotion", font=FONTS['title'], fill=COLORS['WHITE'], tags="text1")
        text2_id = canvas.create_text(0, 0, text="Recognition", font=FONTS['title'], fill=COLORS['WHITE'], tags="text2")

        # Resize handler
        def resize(event):
            canvas_width = event.width
            canvas_height = event.height

            ratio_w = canvas_width / self.original_width
            ratio_h = canvas_height / self.original_height
            scale = min(ratio_w, ratio_h)

            new_width = int(self.original_width * scale)
            new_height = int(self.original_height * scale)

            resized = self.original_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized)
            canvas.bg_image = photo
            canvas.itemconfig(image_id, image=photo)

            canvas.coords(image_id, canvas_width // 2, canvas_height // 2)

            font_size = max(int(FONTS['title'][1] * scale), 10)
            canvas.itemconfig("text1", font=(FONTS['title'][0], font_size))
            canvas.itemconfig("text2", font=(FONTS['title'][0], font_size))

            canvas.coords("text1", canvas_width * 0.3, canvas_height * 0.2)
            canvas.coords("text2", canvas_width * 0.4, canvas_height * 0.35)

        canvas.bind("<Configure>", resize)
