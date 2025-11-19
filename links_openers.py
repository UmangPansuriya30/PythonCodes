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
        "bg": "white",
        "fg": "black",
        "text_bg": "white",
        "text_fg": "black",
        "cursor": "black",
        "btn_bg": "#e0e0e0",
        "btn_fg": "black",
        "btn_active": "#d5d5d5",
    }
}
current_theme = "dark"

def apply_theme():
    theme = THEMES[current_theme]

    # Window
    root.configure(bg=theme["bg"])

    # Label
    label.configure(bg=theme["bg"], fg=theme["fg"])

    # Text Area
    text_area.configure(
        bg=theme["text_bg"],
        fg=theme["text_fg"],
        insertbackground=theme["cursor"]
    )

    # Buttons
    for btn in [toggle_button, format_button, open_button]:
        btn.configure(
            bg=theme["btn_bg"],
            fg=theme["btn_fg"],
            activebackground=theme["btn_active"]
        )

    # Button frame background
    button_frame.configure(bg=theme["bg"])
def toggle_theme():
    global current_theme
    current_theme = "light" if current_theme == "dark" else "dark"
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

# Instructions label
label = tk.Label(root, text="Paste your links (one per line):")
label.pack(pady=5)
    
# Text area for links
text_area = tk.Text(root, wrap="word", height=15, width=60)
text_area.pack(padx=10, pady=10, fill="both", expand=True)

# # Open Links button
# open_button = tk.Button(root, text="Open Links", command=open_links, bg="lightblue", font=("Arial", 12, "bold"))
# open_button.pack(pady=10)


button_frame = tk.Frame(root)
button_frame.pack(pady=10)

toggle_button = tk.Button(button_frame,text="Toggle Theme",command=toggle_theme,font=("Arial", 12, "bold"))
toggle_button.pack(side="left", padx=10)

format_button = tk.Button(button_frame,text="IDs Formatter",command=format_ids,font=("Arial", 12, "bold"))
format_button.pack(side="left", padx=10)

open_button = tk.Button(button_frame,text="Open Links",command=open_links,font=("Arial", 12, "bold"))
open_button.pack(side="left", padx=10)


apply_theme() # starts in dark theme
# Run the app
root.mainloop()