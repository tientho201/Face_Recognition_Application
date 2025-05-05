"""
Video window for the Emotion Recognition application.
"""

import tkinter as tk
from tkinter import filedialog
import os
import sys
from ..utils import check_icon, on_enter, on_leave, print_error_input
from ..config import COLORS, FONTS, IMG_DIR, ALLOWED_VIDEO_EXTENSIONS
from ..features import VideoHandler

class VideoWindow(tk.Toplevel):
    """Video window class for processing video files."""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Store parent window
        self.parent = parent
        
        # Initialize video handler
        self.video_handler = VideoHandler()
        
        # Configure window
        self.title("Video")
        self.configure(bg=COLORS['WHITE'])
        
        # Save parent window info
        self.window_width = parent.winfo_width()
        self.window_height = parent.winfo_height()
        self.window_x = parent.winfo_x()
        self.window_y = parent.winfo_y()
        self.is_maximized = parent.state() == "zoomed"
        
        # Hide parent window
        parent.withdraw()
        
        # Set window geometry
        if self.is_maximized:
            self.state("zoomed")
        else:
            self.geometry(f"{self.window_width}x{self.window_height}+{self.window_x}+{self.window_y}")
            
        # Configure grid
        self.rowconfigure(1, weight=9)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Create frames
        self._create_frames()
        
        # Set window close protocol
        self.protocol("WM_DELETE_WINDOW", self._close_window)
        
    def _create_frames(self):
        """Create all frames for the video window."""
        # Top frame with back button
        self.frm_top = tk.Frame(master=self, bg=COLORS['WHITE'])
        self.frm_top.grid(row=0, column=0, sticky="nsew")
        
        # Back button
        back_img = check_icon(os.path.join(IMG_DIR, "back-button.png"))
        self.btn_back = tk.Button(
            master=self.frm_top,
            image=back_img,
            command=self._back_to_main,
            borderwidth=0,
            highlightthickness=0,
            cursor="hand2"
        )
        self.btn_back.grid(row=0, column=0, padx=15, pady=15)
        self.btn_back.bind("<Enter>", lambda e: on_enter(self.btn_back, "SystemButtonFace", "#F4A460"))
        self.btn_back.bind("<Leave>", lambda e: on_leave(self.btn_back, "SystemButtonFace", "#F4A460"))
        
        # Middle frame for video display
        self.frm_mid = tk.Frame(master=self)
        self.frm_mid.grid(row=1, column=0, sticky="nsew", pady=(0, 20), padx=20)
        self.frm_mid.rowconfigure(0, weight=1)
        self.frm_mid.columnconfigure(0, weight=1)
        
        # Display default video image
        video_img = check_icon(os.path.join(IMG_DIR, "film.png"))
        self.video_lbl = tk.Label(master=self.frm_mid, image=video_img)
        self.video_lbl.grid(row=0, column=0, sticky="nsew")
        
        # Bottom frame with control buttons
        self.frm_bottom = tk.Frame(master=self, bg=COLORS['WHITE'])
        self.frm_bottom.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.frm_bottom.columnconfigure(0, weight=1)
        self.frm_bottom.columnconfigure(1, weight=5)
        self.frm_bottom.columnconfigure(2, weight=5)
        self.frm_bottom.columnconfigure(3, weight=1)
        
        # Control buttons
        self.btn_add = tk.Button(
            master=self.frm_bottom,
            text="Add video",
            font=FONTS['button'],
            cursor="hand2",
            command=self._add_video
        )
        self.btn_add.grid(row=0, column=0, sticky="nsew")
        self.btn_add.bind("<Enter>", lambda e: on_enter(self.btn_add, "SystemButtonFace", "#F4A460"))
        self.btn_add.bind("<Leave>", lambda e: on_leave(self.btn_add, "SystemButtonFace", "#F4A460"))
        
        self.btn_delete = tk.Button(
            master=self.frm_bottom,
            text="Delete video",
            font=FONTS['button'],
            cursor="hand2",
            command=self._delete_video
        )
        self.btn_delete.grid(row=0, column=4, sticky="nsew")
        self.btn_delete.bind("<Enter>", lambda e: on_enter(self.btn_delete, "SystemButtonFace", "#F4A460"))
        self.btn_delete.bind("<Leave>", lambda e: on_leave(self.btn_delete, "SystemButtonFace", "#F4A460"))
        
    def _add_video(self):
        self._delete_video()
        """Open file dialog to select video file."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Video files", " ".join(ALLOWED_VIDEO_EXTENSIONS)), ("All files", "*.*")]
        )
        if not file_path:
            return
            
        self.video_handler.start_video(file_path, self.frm_mid, self._update_video_display)
        
    def _delete_video(self):
        """Stop video playback and reset display."""
        self.video_handler.stop_video()
        self._reset_display()
        
    def _update_video_display(self, img_tk):
        """Update video display with new frame."""
        for widget in self.frm_mid.winfo_children():
            widget.destroy()
        video_label = tk.Label(master=self.frm_mid, image=img_tk)
        video_label.image = img_tk
        video_label.pack(fill="both", expand=True)
        
    def _reset_display(self):
        """Reset display to default video image."""
        for widget in self.frm_mid.winfo_children():
            widget.destroy()
        video_img = check_icon(os.path.join(IMG_DIR, "film.png"))
        self.video_lbl = tk.Label(master=self.frm_mid, image=video_img)
        self.video_lbl.grid(row=0, column=0, sticky="nsew")
        
    def _back_to_main(self):
        """Return to main window."""
        self.update_idletasks()
        if self.state() == "zoomed":
            self.parent.state("zoomed")
        else:
            new_width = self.winfo_width()
            new_height = self.winfo_height()
            new_x = self.winfo_x()
            new_y = self.winfo_y()
            self.parent.after(0, lambda: self.parent.geometry(f"{new_width}x{new_height}+{new_x}+{new_y}"))
            
        self._delete_video()
        self.destroy()
        self.parent.deiconify()
        
    def _close_window(self):
        """Handle window close event."""
        self._delete_video()
        sys.exit() 