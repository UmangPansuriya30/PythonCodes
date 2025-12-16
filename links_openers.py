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
        "bg": "#f0f0f0",
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
    # Bottom panels
    bottom_frame.configure(bg=theme["bg"])
    left_panel.configure(bg=theme["bg"])
    right_panel.configure(bg=theme["bg"])
    checks_frame.configure(bg=theme["bg"])


    # Checkboxes
    check_new_window.configure(
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["text_bg"],
        activebackground=theme["bg"]
    )

    check_incognito.configure(
        bg=theme["bg"],
        fg=theme["fg"],
        selectcolor=theme["text_bg"],
        activebackground=theme["bg"]
    )
def toggle_theme(new_state):
    global current_theme
    current_theme = new_state
    apply_theme()
def open_links():
    
    text_content = text_area.get("1.0", tk.END).strip()
    raw_links = re.split(r'[\n,]+', text_content)
    links = [link.strip() for link in raw_links if link.strip()]

    if not links:
        messagebox.showwarning("No Links", "Please paste at least one link.")
        return
    # ───────────────────────────────
    #   Checkbox Logic
    # ───────────────────────────────
    commandString = "start chrome"
    if  incognito_window_var.get():
        commandString += " --incognito"
    if new_window_var.get():
        commandString += " --new-window"
    # Default behavior (old logic)
    subprocess.run(f'{commandString} "{links[0]}"', shell=True)
    commandString = commandString.replace(" --new-window", "")
    for link in links[1:]:
        subprocess.run(f'{commandString} "{link}"', shell=True) 
        time.sleep(0.2)
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
    ids = [i.strip() for i in raw_ids if i.strip()]

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


# ────────────────────────────────────────────────
#   BOTTOM PANELS — Compact Height
# ────────────────────────────────────────────────

bottom_frame = tk.Frame(root, bg=THEMES[current_theme]["bg"])
bottom_frame.pack(fill="x", pady=8, padx=10)

bottom_frame.columnconfigure(0, weight=1)
bottom_frame.columnconfigure(1, weight=1)

# ============= LEFT PANEL =============
left_panel = tk.Frame(
    bottom_frame,
    bd=2,
    relief="groove",
    padx=12,
    pady=8,
    bg=THEMES[current_theme]["bg"]
)
left_panel.grid(row=0, column=0, sticky="nsew", padx=8, ipadx=5, ipady=5)

# Horizontal checkboxes — centered
checks_frame = tk.Frame(left_panel, bg=THEMES[current_theme]["bg"])
checks_frame.pack(pady=2)

new_window_var = tk.BooleanVar(value=True)
check_new_window = tk.Checkbutton(
    checks_frame,
    text="New Window",
    variable=new_window_var,
    bg=THEMES[current_theme]["bg"],
    fg=THEMES[current_theme]["fg"],
    selectcolor=THEMES[current_theme]["text_bg"]
)
check_new_window.pack(side="left", padx=8)

incognito_window_var = tk.BooleanVar(value=True)
check_incognito = tk.Checkbutton(
    checks_frame,
    text="Incognito",
    variable=incognito_window_var,
    bg=THEMES[current_theme]["bg"],
    fg=THEMES[current_theme]["fg"],
    selectcolor=THEMES[current_theme]["text_bg"]
)
check_incognito.pack(side="left", padx=8)


open_button = tk.Button(
    left_panel,
    text="Open Links",
    command=open_links,
    font=("Arial", 12, "bold")
)
open_button.pack(pady=8, fill="x")


# ============= RIGHT PANEL =============
right_panel = tk.Frame(
    bottom_frame,
    bd=2,
    relief="groove",
    padx=12,
    pady=8,
    bg=THEMES[current_theme]["bg"]
)
right_panel.grid(row=0, column=1, sticky="nsew", padx=8, ipadx=5, ipady=5)

format_button = tk.Button(
    right_panel,
    text="IDs Formatter",
    command=format_ids,
    font=("Arial", 12, "bold")
)
right_panel.grid_rowconfigure(0, weight=1)
right_panel.grid_rowconfigure(1, weight=1)

format_button.pack(expand=True, fill="x", pady=8)


apply_theme() # starts in dark theme
# Run the app
root.mainloop()
 