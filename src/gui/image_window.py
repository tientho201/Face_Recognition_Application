"""
Image window for the Emotion Recognition application.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
from PIL import Image, ImageTk
from ..utils import check_icon, on_enter, on_leave, print_error_input, add_box_shadow
from ..config import COLORS, FONTS, IMG_DIR, ALLOWED_IMAGE_EXTENSIONS
from ..features import ImageHandler

class ImageWindow(tk.Toplevel):
    """Image window class for processing image files."""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Store parent window
        self.parent = parent
        
        # Initialize image handler
        self.image_handler = ImageHandler()
        
        # Configure window
        self.title("Image")
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
        """Create all frames for the image window."""
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
        
        # Middle frame for image display
        self.frm_mid = tk.Frame(master=self)
        self.frm_mid.grid(row=1, column=0, sticky="nsew", pady=(0, 20), padx=20)
        self.frm_mid.rowconfigure(0, weight=1)
        self.frm_mid.columnconfigure(0, weight=1)
        self.frm_mid.columnconfigure(1, weight=1)
        
        # Display default image
        img_img = check_icon(os.path.join(IMG_DIR, "frm_img.png"))
        self.img_lbl = tk.Label(master=self.frm_mid, image=img_img)
        self.img_lbl.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
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
            text="Add image",
            font=FONTS['button'],
            cursor="hand2",
            command=self._add_image
        )
        self.btn_add.grid(row=0, column=0, sticky="nsew")
        self.btn_add.bind("<Enter>", lambda e: on_enter(self.btn_add, "SystemButtonFace", "#F4A460"))
        self.btn_add.bind("<Leave>", lambda e: on_leave(self.btn_add, "SystemButtonFace", "#F4A460"))
        
        self.btn_delete = tk.Button(
            master=self.frm_bottom,
            text="Delete image",
            font=FONTS['button'],
            cursor="hand2",
            command=self._delete_image
        )
        self.btn_delete.grid(row=0, column=4, sticky="nsew")
        self.btn_delete.bind("<Enter>", lambda e: on_enter(self.btn_delete, "SystemButtonFace", "#F4A460"))
        self.btn_delete.bind("<Leave>", lambda e: on_leave(self.btn_delete, "SystemButtonFace", "#F4A460"))
        
    def _add_image(self):
        """Open file dialog to select image file."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", " ".join(ALLOWED_IMAGE_EXTENSIONS)), ("All files", "*.*")]
        )
        if not file_path:
            return
            
        try:
            # Try to open image with PIL to check if it's valid
            Image.open(file_path)
            self.image_handler.process_image(file_path, self.frm_mid, self._update_image_display)
        except Exception as e:
            # Show error message in a message box
            error_msg = f"Lỗi: Không thể đọc ảnh\n\nChi tiết lỗi:\n{str(e)}\n\nVui lòng chọn ảnh khác."
            messagebox.showerror("Lỗi đọc ảnh", error_msg)
            self._reset_display()
            
    def _delete_image(self):
        """Reset image display."""
        self._reset_display()
        
    def _update_image_display(self, original_img, processed_img):
        """Update image display with original and processed images."""
        try:
            for widget in self.frm_mid.winfo_children():
                widget.destroy()
                
            # Get frame dimensions
            frame_width = self.frm_mid.winfo_width()
            frame_height = self.frm_mid.winfo_height()
            
            # Calculate target dimensions for each image (half of frame width)
            target_width = frame_width // 2
            target_height = frame_height
            
            # Add labels
            original_label = tk.Label(
                master=self.frm_mid,
                text="Original Image",
                font=FONTS['subtitle'],
                bg=COLORS['WHITE']
            )
            original_label.grid(row=0, column=0, sticky="nsew")
            
            processed_label = tk.Label(
                master=self.frm_mid,
                text="Processed Image",
                font=FONTS['subtitle'],
                bg=COLORS['WHITE']
            )
            processed_label.grid(row=0, column=1, sticky="nsew")
            
            # Create canvas for original image
            original_canvas = tk.Canvas(master=self.frm_mid, width=target_width, height=target_height)
            original_canvas.grid(row=1, column=0, sticky="nsew")
            
            # Create canvas for processed image
            processed_canvas = tk.Canvas(master=self.frm_mid, width=target_width, height=target_height)
            processed_canvas.grid(row=1, column=1, sticky="nsew")
            
            # Function to resize and display image
            def resize_and_display(canvas, img, target_w, target_h):
                try:
                    # Convert PhotoImage to PIL Image
                    pil_img = ImageTk.getimage(img)
                    
                    # Calculate aspect ratio
                    img_ratio = pil_img.width / pil_img.height
                    target_ratio = target_w / target_h
                    
                    # Calculate new dimensions while maintaining aspect ratio
                    if img_ratio > target_ratio:
                        # Image is wider than target
                        new_width = target_w
                        new_height = int(target_w / img_ratio)
                    else:
                        # Image is taller than target
                        new_height = target_h
                        new_width = int(target_h * img_ratio)
                    
                    # Resize image
                    resized = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Convert back to PhotoImage
                    photo = ImageTk.PhotoImage(resized)
                    
                    # Store reference
                    canvas.image = photo
                    
                    # Calculate position to center image
                    x = (target_w - new_width) // 2
                    y = (target_h - new_height) // 2
                    
                    # Display image
                    canvas.create_image(x, y, image=photo, anchor="nw")
                    
                    # Bind resize event
                    def on_resize(event):
                        resize_and_display(canvas, img, event.width, event.height)
                    
                    canvas.bind("<Configure>", on_resize)
                except Exception as e:
                    error_msg = f"Lỗi: Không thể hiển thị ảnh\n\nChi tiết lỗi:\n{str(e)}\n\nVui lòng thử lại."
                    messagebox.showerror("Lỗi hiển thị ảnh", error_msg)
                    self._reset_display()
            
            # Display both images
            resize_and_display(original_canvas, original_img, target_width, target_height)
            resize_and_display(processed_canvas, processed_img, target_width, target_height)
        except Exception as e:
            error_msg = f"Lỗi: Không thể cập nhật hiển thị\n\nChi tiết lỗi:\n{str(e)}\n\nVui lòng thử lại."
            messagebox.showerror("Lỗi cập nhật hiển thị", error_msg)
            self._reset_display()
        
    def _reset_display(self):
        """Reset display to default image."""
        for widget in self.frm_mid.winfo_children():
            widget.destroy()
        img_img = check_icon(os.path.join(IMG_DIR, "frm_img.png"))
        self.img_lbl = tk.Label(master=self.frm_mid, image=img_img)
        self.img_lbl.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
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
            
        self._delete_image()
        self.destroy()
        self.parent.deiconify()
        
    def _close_window(self):
        """Handle window close event."""
        self._delete_image()
        sys.exit()