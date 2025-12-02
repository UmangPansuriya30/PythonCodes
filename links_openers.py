import time
import tkinter as tk
from tkinter import messagebox
import subprocess
import re
THEMES = {
    "dark": {
        "bg": "#1e1e1e",
        "fg": "white",
        "text_bg": "#2b2b2b",
        "text_fg": "white",
        "cursor": "white",
        "btn_bg": "#444",
        "btn_fg": "white",
        "btn_active": "#555",
    },
    "light": {
<<<<<<< HEAD
        "bg": "#cacaca",
=======
        "bg": "#f0f0f0",
>>>>>>> 01b79febe519aea03d35aad4b9d4656553c5bf7d
        "fg": "black",
        "text_bg": "white",
        "text_fg": "black",
        "cursor": "black",
        "btn_bg": "#c1bfbf",
        "btn_fg": "black",
        "btn_active": "#d5d5d5",
    }
}
current_theme = "dark"

class ThemeSwitch(tk.Frame):
    def __init__(self, master, command, initial_state="dark"):
        super().__init__(master, bg=THEMES[initial_state]["bg"])

        self.state = initial_state
        self.command = command

        self.canvas = tk.Canvas(
            self, width=60, height=28,
            bg=THEMES[self.state]["bg"], highlightthickness=0
        )
        self.canvas.pack()

        self.draw_switch()

        self.canvas.bind("<Button-1>", self.toggle)

    # Draw a rounded rectangle without smooth=True
    def rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def draw_switch(self):
        theme = THEMES[self.state]

        self.canvas.delete("all")

        # Rounded background
        self.rounded_rect(2, 2, 58, 26, 33,
                          fill=theme["btn_bg"])

        # Knob position
        if self.state == "dark":
            x0, x1 = 7, 24
        else:
            x0, x1 = 37, 54

        # Round knob
        self.canvas.create_oval(
            x0, 6, x1, 22,
            fill=theme["btn_fg"],
            outline=theme["btn_fg"]
        )

        # Icons
        if self.state == "dark":
            self.canvas.create_text(45, 14, text="☀", fill=theme["fg"], font=("Arial", 10))
        else:
            self.canvas.create_text(15, 11, text="🌙", fill=theme["fg"], font=("Arial", 10))

    def toggle(self, _=None):
        self.state = "light" if self.state == "dark" else "dark"
        self.draw_switch()
        self.command(self.state)
def switch_theme(state):
    global current_theme
    current_theme = state
    apply_theme()
def apply_theme():
    theme = THEMES[current_theme]

    # Window
    root.configure(bg=theme["bg"])

    # Update the top bar background
    top_bar.configure(bg=theme["bg"])
    label.configure(bg=theme["bg"], fg=theme["fg"])

    # Update theme switch container + canvas
    theme_switch.configure(bg=theme["bg"])
    theme_switch.canvas.configure(bg=theme["bg"])
    theme_switch.draw_switch()


    # Text Area
    text_area.configure(
        bg=theme["text_bg"],
        fg=theme["text_fg"],
        insertbackground=theme["cursor"]
    )

    # Buttons
    for btn in [ format_button, open_button]:
        btn.configure(
            bg=theme["btn_bg"],
            fg=theme["btn_fg"],
            activebackground=theme["btn_active"]
        )

    # Button frame background
    button_frame.configure(bg=theme["bg"])
def toggle_theme(new_state):
    global current_theme
    current_theme = new_state
    apply_theme()

def open_links():
    # Get the text content
    text_content = text_area.get("1.0", tk.END).strip()

    # Split by newline OR comma using regex
    raw_links = re.split(r'[\n,]+', text_content)

    # Clean up and remove empty entries
    links = [link.strip() for link in raw_links if link.strip()]

    if not links:
        messagebox.showwarning("No Links", "Please paste at least one link.")
        return

    # Open first link in new window
    subprocess.run(f"start chrome --incognito --new-window {links[0]}", shell=True)

    # Open remaining links in new tabs
    for link in links[1:]:
        subprocess.run(f"start chrome --incognito {link}", shell=True)
        time.sleep(0.2)  # Slight delay to ensure tabs open properly
def show_copy_dialog(title, content):
    theme = THEMES[current_theme]

    popup = tk.Toplevel(root)
    popup.title(title)
    popup.geometry("500x200")
    popup.configure(bg=theme["bg"])

    text_box = tk.Text(popup,height=5,wrap="word",bg=theme["text_bg"],fg=theme["text_fg"],insertbackground=theme["cursor"])
    text_box.pack(padx=10, pady=10, fill="both", expand=True)
    text_box.insert("1.0", content)
    text_box.config(state="disabled")

    def copy_to_clipboard():
        root.clipboard_clear()
        root.clipboard_append(content)
        popup.destroy()

    copy_btn = tk.Button(popup,text="Copy",command=copy_to_clipboard,bg=theme["btn_bg"],fg=theme["btn_fg"],activebackground=theme["btn_active"],font=("Arial", 11, "bold"))
    copy_btn.pack(pady=5)
def format_ids():
    # Get the text content
    text_content = text_area.get("1.0", tk.END).strip()

    # Split by newline or comma
    raw_ids = re.split(r'[\n,]+', text_content)

    # Clean and keep only digits
    ids = [i.strip() for i in raw_ids if i.strip().isdigit()]

    if not ids:
        messagebox.showwarning("No IDs", "Please enter valid numeric IDs.")
        return

    # Format like: ('1','2','3')
    formatted = "('" + "','".join(ids) + "')"

    # Show popup with copy button
    show_copy_dialog("Formatted IDs", formatted)

# Create main window
root = tk.Tk()
root.title("Open Links Tool")
root.geometry("900x500")

top_bar = tk.Frame(root, bg=THEMES[current_theme]["bg"])
top_bar.pack(fill="x", pady=5, padx=10)

# Instructions label
label = tk.Label(top_bar, text="Paste your links (one per line):",bg=THEMES[current_theme]["bg"],fg=THEMES[current_theme]["fg"])
label.pack(side="left")

theme_switch = ThemeSwitch(
    top_bar,
    command=lambda state: switch_theme(state),
    initial_state=current_theme
)
theme_switch.pack(side="right")

# Text area for links
text_area = tk.Text(root, wrap="word", height=15, width=60)
text_area.pack(padx=10, pady=2, fill="both", expand=True)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

open_button = tk.Button(button_frame,text="Open Links",command=open_links,font=("Arial", 12, "bold"))
open_button.pack(side="left", padx=10)

format_button = tk.Button(button_frame,text="IDs Formatter",command=format_ids,font=("Arial", 12, "bold"))
format_button.pack(side="left", padx=10)

apply_theme() # starts in dark theme
# Run the app
root.mainloop()
