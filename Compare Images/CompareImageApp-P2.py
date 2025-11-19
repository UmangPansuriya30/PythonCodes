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
        self.root.geometry("1300x850")
        self.root.configure(bg="#f0f0f0")

        # Store images
        self.img1 = None
        self.img2 = None
        self.diff_gray = None
        self.diff_red = None
        self.thresh = None

        # Store PhotoImages
        self.canvas_images = {}

        # Zoom levels & offsets for difference images
        self.zoom_levels = {"diff_gray": 1.0, "diff_red": 1.0, "thresh": 1.0}
        self.offsets = {"diff_gray": [0, 0], "diff_red": [0, 0], "thresh": [0, 0]}
        self.start_drag = {}

        # ===== Top Buttons =====
        btn_frame = tk.Frame(root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Select Image 1", width=20, command=self.load_image1).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Select Image 2", width=20, command=self.load_image2).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Compare & Generate Diff", width=25, command=self.compare_images).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Save Diff Images", width=20, command=self.save_images).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Reset Zoom/Pan", width=20, command=self.reset_zoom_pan).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Fit to Canvas", width=20, command=self.fit_to_canvas).pack(side="left", padx=5)

        # ===== SSIM Score & Numeric Differences (Horizontal) =====
        score_frame = tk.Frame(root, bg="#f0f0f0")
        score_frame.pack(pady=5)

        self.ssim_label = tk.Label(score_frame, text="SSIM Score: N/A", font=("Arial", 12), bg="#f0f0f0")
        self.ssim_label.pack(side="left", padx=10)

        self.diff_percent_label = tk.Label(score_frame, text="Difference Pixels: N/A", font=("Arial", 12), bg="#f0f0f0")
        self.diff_percent_label.pack(side="left", padx=10)


        # ===== Original Images Frame =====
        orig_frame = tk.LabelFrame(root, text="Original Images", padx=10, pady=10, bg="#f0f0f0")
        orig_frame.pack(pady=10, fill="both", expand=True)

        self.canvas1 = tk.Canvas(orig_frame, bg="white")
        self.canvas1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.canvas2 = tk.Canvas(orig_frame, bg="white")
        self.canvas2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        orig_frame.columnconfigure(0, weight=1)
        orig_frame.columnconfigure(1, weight=1)
        orig_frame.rowconfigure(0, weight=1)

        # ===== Difference Images Frame =====
        diff_frame = tk.LabelFrame(root, text="Difference Images (Zoomable + Draggable)", padx=10, pady=10, bg="#f0f0f0")
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

        # Bind canvas resize
        for canvas in [self.canvas1, self.canvas2, self.canvas_diff_gray, self.canvas_diff_red, self.canvas_thresh]:
            canvas.bind("<Configure>", self.on_canvas_resize)

        # Bind mouse events for difference images
        for canvas, img_type in [(self.canvas_diff_gray, "diff_gray"),
                                 (self.canvas_diff_red, "diff_red"),
                                 (self.canvas_thresh, "thresh")]:
            canvas.bind("<MouseWheel>", lambda e, t=img_type: self.zoom_image(e, t))
            canvas.bind("<ButtonPress-1>", lambda e, t=img_type: self.start_drag_event(e, t))
            canvas.bind("<B1-Motion>", lambda e, t=img_type: self.drag_image(e, t))

    # ==================== Image Loading ====================
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

    # ==================== Compare Images ====================
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

        red_mask = np.zeros_like(self.img1)
        red_mask[:, :] = (0, 0, 255)
        diff_red = self.img1.copy()
        diff_red[thresh == 255] = red_mask[thresh == 255]

        self.diff_gray = diff
        self.diff_red = diff_red
        self.thresh = thresh

        # Reset zoom & offsets
        self.zoom_levels = {k: 1.0 for k in self.zoom_levels}
        self.offsets = {k: [0,0] for k in self.offsets}

        # Update SSIM and difference % labels
        self.ssim_label.config(text=f"SSIM Score: {score:.4f}", fg=self.get_ssim_color(score))
        diff_percent = np.sum(thresh==255)/thresh.size*100
        self.diff_percent_label.config(text=f"Difference Pixels: {diff_percent:.2f}%")

        # Show difference images
        self.show_all_diffs()

    # ==================== Show all difference images ====================
    def show_all_diffs(self):
        self.show_image_on_canvas(self.diff_gray, self.canvas_diff_gray, is_gray=True, zoom=self.zoom_levels["diff_gray"], offset=self.offsets["diff_gray"])
        self.show_image_on_canvas(self.diff_red, self.canvas_diff_red, zoom=self.zoom_levels["diff_red"], offset=self.offsets["diff_red"])
        self.show_image_on_canvas(self.thresh, self.canvas_thresh, is_gray=True, zoom=self.zoom_levels["thresh"], offset=self.offsets["thresh"])

    # ==================== Show Image on Canvas ====================
    def show_image_on_canvas(self, cv_img, canvas, is_gray=False, zoom=1.0, offset=[0,0]):
        if cv_img is None:
            return
        if is_gray:
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)

        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        if canvas_width < 10 or canvas_height < 10:
            return

        h, w = cv_img.shape[:2]
        scale = min(canvas_width / w, canvas_height / h) * zoom
        new_w, new_h = int(w * scale), int(h * scale)
        cv_img_resized = cv2.resize(cv_img, (new_w, new_h))

        img = Image.fromarray(cv2.cvtColor(cv_img_resized, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)

        self.canvas_images[canvas] = imgtk
        canvas.delete("all")
        canvas.create_image(canvas_width//2 + offset[0], canvas_height//2 + offset[1], image=imgtk, anchor="center")

    # ==================== Zoom with mouse-centered behavior ====================
    def zoom_image(self, event, image_type):
        old_zoom = self.zoom_levels[image_type]
        factor = 1.1 if event.delta > 0 else 0.9
        new_zoom = old_zoom * factor
        new_zoom = max(0.2, min(new_zoom, 5.0))
        self.zoom_levels[image_type] = new_zoom

        canvas, img, is_gray = self.get_canvas_img_type(image_type)
        if img is None:
            return

        # Mouse-centered offset adjustment
        mx, my = event.x, event.y
        offset = self.offsets[image_type]
        offset[0] = int((offset[0] - mx) * (new_zoom / old_zoom) + mx)
        offset[1] = int((offset[1] - my) * (new_zoom / old_zoom) + my)

        self.show_image_on_canvas(img, canvas, is_gray, zoom=new_zoom, offset=offset)

    # ==================== Drag ====================
    def start_drag_event(self, event, image_type):
        self.start_drag[image_type] = (event.x, event.y)

    def drag_image(self, event, image_type):
        start_x, start_y = self.start_drag.get(image_type, (event.x, event.y))
        dx = event.x - start_x
        dy = event.y - start_y
        self.offsets[image_type][0] += dx
        self.offsets[image_type][1] += dy
        self.start_drag[image_type] = (event.x, event.y)
        canvas, img, is_gray = self.get_canvas_img_type(image_type)
        if img is not None:
            self.show_image_on_canvas(img, canvas, is_gray, zoom=self.zoom_levels[image_type], offset=self.offsets[image_type])

    # ==================== Helpers ====================
    def get_canvas_img_type(self, image_type):
        if image_type == "diff_gray":
            return self.canvas_diff_gray, self.diff_gray, True
        elif image_type == "diff_red":
            return self.canvas_diff_red, self.diff_red, False
        elif image_type == "thresh":
            return self.canvas_thresh, self.thresh, True
        return None, None, None

    def get_ssim_color(self, score):
        if score > 0.95: return "green"
        elif score > 0.85: return "orange"
        else: return "red"

    # ==================== Reset / Fit ====================
    def reset_zoom_pan(self):
        self.zoom_levels = {k: 1.0 for k in self.zoom_levels}
        self.offsets = {k: [0,0] for k in self.offsets}
        self.show_all_diffs()

    def fit_to_canvas(self):
        self.zoom_levels = {k: 1.0 for k in self.zoom_levels}
        self.offsets = {k: [0,0] for k in self.offsets}
        self.show_all_diffs()

    # ==================== Canvas Resize ====================
    def on_canvas_resize(self, event):
        canvas = event.widget
        if canvas == self.canvas1:
            self.show_image_on_canvas(self.img1, canvas)
        elif canvas == self.canvas2:
            self.show_image_on_canvas(self.img2, canvas)
        elif canvas == self.canvas_diff_gray:
            self.show_image_on_canvas(self.diff_gray, canvas, is_gray=True, zoom=self.zoom_levels["diff_gray"], offset=self.offsets["diff_gray"])
        elif canvas == self.canvas_diff_red:
            self.show_image_on_canvas(self.diff_red, canvas, zoom=self.zoom_levels["diff_red"], offset=self.offsets["diff_red"])
        elif canvas == self.canvas_thresh:
            self.show_image_on_canvas(self.thresh, canvas, is_gray=True, zoom=self.zoom_levels["thresh"], offset=self.offsets["thresh"])

    # ==================== Save ====================
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
