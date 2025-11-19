import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

class ImageCompareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Compare App")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")

        # Store images
        self.img1 = None
        self.img2 = None
        self.diff_gray = None
        self.diff_red = None
        self.thresh = None

        # Store references to PhotoImages
        self.canvas_images = {}

        # Top frame for buttons
        # btn_frame = tk.Frame(root, bg="#f0f0f0")
        # btn_frame.pack(pady=10, fill="x")

        # tk.Button(btn_frame, text="Select Image 1", width=20, command=self.load_image1).grid(row=0, column=0, padx=5)
        # tk.Button(btn_frame, text="Select Image 2", width=20, command=self.load_image2).grid(row=0, column=1, padx=5)
        # tk.Button(btn_frame, text="Compare & Generate Diff", width=25, command=self.compare_images).grid(row=0, column=2, padx=5)
        # tk.Button(btn_frame, text="Save Diff Images", width=20, command=self.save_images).grid(row=0, column=3, padx=5)
        # Top frame for buttons (centered)
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        # Create buttons inside a horizontal frame
        tk.Button(btn_frame, text="Select Image 1", width=20, command=self.load_image1).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Select Image 2", width=20, command=self.load_image2).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Compare & Generate Diff", width=25, command=self.compare_images).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Save Diff Images", width=20, command=self.save_images).pack(side="left", padx=5)

        # ===== SSIM label =====
        self.ssim_label = tk.Label(root, text="SSIM Score: N/A", font=("Arial", 12), bg="#f0f0f0")
        self.ssim_label.pack(pady=5)

        # Frame for original images
        orig_frame = tk.LabelFrame(root, text="Original Images", padx=10, pady=10, bg="#f0f0f0")
        orig_frame.pack(pady=10, fill="both", expand=True)

        self.canvas1 = tk.Canvas(orig_frame, bg="white")
        self.canvas1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.canvas2 = tk.Canvas(orig_frame, bg="white")
        self.canvas2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        orig_frame.columnconfigure(0, weight=1)
        orig_frame.columnconfigure(1, weight=1)
        orig_frame.rowconfigure(0, weight=1)

        # Frame for difference images
        diff_frame = tk.LabelFrame(root, text="Difference Images", padx=10, pady=10, bg="#f0f0f0")
        diff_frame.pack(pady=10, fill="both", expand=True)

        self.canvas_diff_gray = tk.Canvas(diff_frame, bg="white")
        self.canvas_diff_gray.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.canvas_diff_red = tk.Canvas(diff_frame, bg="white")
        self.canvas_diff_red.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.canvas_thresh = tk.Canvas(diff_frame, bg="white")
        self.canvas_thresh.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        diff_frame.columnconfigure(0, weight=1)
        diff_frame.columnconfigure(1, weight=1)
        diff_frame.columnconfigure(2, weight=1)
        diff_frame.rowconfigure(0, weight=1)

        # Bind canvas resize events to redraw images
        for canvas in [self.canvas1, self.canvas2, self.canvas_diff_gray, self.canvas_diff_red, self.canvas_thresh]:
            canvas.bind("<Configure>", self.on_canvas_resize)

    def load_image1(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            self.img1 = cv2.imread(path)
            self.show_image_on_canvas(self.img1, self.canvas1)

    def load_image2(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if path:
            self.img2 = cv2.imread(path)
            self.show_image_on_canvas(self.img2, self.canvas2)

    def compare_images(self):
        if self.img1 is None or self.img2 is None:
            messagebox.showerror("Error", "Select both images first")
            return

        img2_resized = cv2.resize(self.img2, (self.img1.shape[1], self.img1.shape[0]))
        gray1 = cv2.cvtColor(self.img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2GRAY)

        score, diff = ssim(gray1, gray2, full=True)
        diff = (diff * 255).astype("uint8")
        _, thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

        # Update SSIM score label
        self.ssim_label.config(text=f"SSIM Score: {score:.4f}")
        # Create red diff image
        red_mask = np.zeros_like(self.img1)
        red_mask[:, :] = (0, 0, 255)
        diff_red = self.img1.copy()
        diff_red[thresh == 255] = red_mask[thresh == 255]

        self.diff_gray = diff
        self.diff_red = diff_red
        self.thresh = thresh

        self.show_image_on_canvas(self.diff_gray, self.canvas_diff_gray, is_gray=True)
        self.show_image_on_canvas(self.diff_red, self.canvas_diff_red)
        self.show_image_on_canvas(self.thresh, self.canvas_thresh, is_gray=True)

    def show_image_on_canvas(self, cv_img, canvas, is_gray=False):
        if cv_img is None:
            return
        if is_gray:
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        if canvas_width < 10 or canvas_height < 10:
            return  # Skip if not yet properly sized

        h, w = cv_img.shape[:2]
        scale = min(canvas_width / w, canvas_height / h)
        new_w, new_h = int(w * scale), int(h * scale)
        cv_img_resized = cv2.resize(cv_img, (new_w, new_h))

        img = Image.fromarray(cv2.cvtColor(cv_img_resized, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)

        # Save reference to prevent garbage collection
        self.canvas_images[canvas] = imgtk
        canvas.delete("all")
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=imgtk, anchor="center")

    def on_canvas_resize(self, event):
        canvas = event.widget
        if canvas == self.canvas1:
            self.show_image_on_canvas(self.img1, canvas)
        elif canvas == self.canvas2:
            self.show_image_on_canvas(self.img2, canvas)
        elif canvas == self.canvas_diff_gray:
            self.show_image_on_canvas(self.diff_gray, canvas, is_gray=True)
        elif canvas == self.canvas_diff_red:
            self.show_image_on_canvas(self.diff_red, canvas)
        elif canvas == self.canvas_thresh:
            self.show_image_on_canvas(self.thresh, canvas, is_gray=True)

    def save_images(self):
        if self.diff_gray is None:
            messagebox.showerror("Error", "No diff images to save")
            return

        save_dir = filedialog.askdirectory()
        if not save_dir:
            return

        cv2.imwrite(f"{save_dir}/diff_gray.png", self.diff_gray)
        cv2.imwrite(f"{save_dir}/diff_red.png", self.diff_red)
        cv2.imwrite(f"{save_dir}/thresh.png", self.thresh)
        messagebox.showinfo("Saved", "Diff images saved successfully")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCompareApp(root)
    root.mainloop()
