"""

TagFlow — an automatic tag inserter program.

Copyright (C) 2025 - 1mcold
This code is distributed under the GNU General Public License v3.0.
You are free to use, modify, and distribute it,
but you must keep the source code open.

Created by 1mcold
GitHub: https://github.com/1mcold


"""

import tkinter as tk
from tkinter import messagebox, filedialog
import keyboard
import json
import pyperclip
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image, ImageDraw, ImageTk
import sys

# Global Variables
filename = "tags.txt"
tags = []  # List to hold tags
index = 0  # Index to track the current tag
autotyper_enabled = False  # Flag to control the state of the autotyper
autotyper_active = False  # Flag to control if the autotyper is currently running
autotyper_thread = None  # Thread for the autotyper process

# Load Tags from the tags file
def load_tags():
    global tags, index
    try:
        with open(filename, "r", encoding="utf-8") as file:
            new_tags = [line.strip() for line in file if line.strip()]
        if new_tags != tags:
            tags[:] = new_tags  # Update tags if they have changed
            index = 0  # Reset the index
            update_label()  # Update the status label
    except Exception as e:
        print(f"File read error: {e}")

# Function to paste the next tag (either automatically or manually)
def paste_next_tag():
    global index, autotyper_enabled, autotyper_active, autotyper_thread
    if autotyper_enabled:
        if not autotyper_active:
            autotyper_active = True  # Start the auto-typing process
            autotyper_thread = threading.Thread(target=auto_typing)
            autotyper_thread.start()  # Run the auto-typing in a separate thread
        else:
            autotyper_active = False  # Stop the auto-typing
            if autotyper_thread is not None:
                autotyper_thread.join()  # Wait for the thread to finish
            update_label()  # Update the status label
    else:
        if index < len(tags):
            tag = tags[index]
            pyperclip.copy(tag)
            keyboard.press_and_release('ctrl+v')
            time.sleep(0.1)  # Short delay to mimic typing speed
            keyboard.press_and_release('enter')
            index += 1
            update_label()
        else:
            messagebox.showinfo("Info", "All tags are inserted.")

# Auto-typing function that runs in a separate thread
def auto_typing():
    global index, autotyper_active
    while index < len(tags) and autotyper_active:
        tag = tags[index]
        pyperclip.copy(tag)
        keyboard.press_and_release('ctrl+v')
        time.sleep(0.1)  # Adjust delay for typing speed
        keyboard.press_and_release('enter')
        index += 1
        update_label()

# Update the status label to show the next tag or that all tags are inserted
def update_label():
    if index < len(tags):
        status_var.set(f"Next tag: {tags[index]}")
    else:
        status_var.set("All tags are inserted.")

# Toggle the state of the autotyper (on/off)
def toggle_autotyper():
    global autotyper_enabled
    autotyper_enabled = not autotyper_enabled  # Toggle the autotyper state
    update_button_text()  # Update the button text accordingly

# Update the button text based on the autotyper state
def update_button_text():
    if autotyper_enabled:
        btn_autotyper.config(text="⌨ AutoTyper: On")
    else:
        btn_autotyper.config(text="⌨ AutoTyper: Off")

def change_theme():
    file_path = filedialog.askopenfilename(
        title="Choose theme file",
        filetypes=[("JSON Files", "*.json")],
        initialdir="themes"
    )
    if file_path:
        try:
            theme = load_theme_from_file(file_path)
            apply_theme(theme)
        except Exception as e:
            messagebox.showerror("Theme Error", f"Failed to load theme: {e}")

def apply_theme(theme):
    global current_theme, backgroundcolor, backgroundcolorforbutton, foregroundcolor
    current_theme = theme
    backgroundcolor = current_theme["backgroundcolor"]
    backgroundcolorforbutton = current_theme["backgroundcolorforbutton"]
    foregroundcolor = current_theme["foregroundcolor"]

    # Update the colors of the main window
    root.configure(bg=backgroundcolor)
    status_label.configure(bg=backgroundcolor, fg=foregroundcolor)
    info_label.configure(bg=backgroundcolor, fg=foregroundcolor)
    info_label1.configure(bg=backgroundcolor, fg=foregroundcolor)
    root.iconphoto(False, ImageTk.PhotoImage(create_icon(backgroundcolor)))

    # If the settings window is already open - let's update it too
    if settings_win is not None and settings_label is not None:
        settings_win.configure(bg=backgroundcolor)
        settings_label.configure(bg=backgroundcolor, fg=foregroundcolor)
        btn_autotyper.configure(bg=backgroundcolorforbutton, fg=foregroundcolor, activebackground=backgroundcolorforbutton)
        btn_changetheme.configure(bg=backgroundcolorforbutton, fg=foregroundcolor, activebackground=backgroundcolorforbutton)

        settings_win.iconphoto(False, ImageTk.PhotoImage(create_icon(backgroundcolor)))

def open_settings():
    global settings_win, settings_label, btn_autotyper, btn_changetheme

    settings_win = tk.Toplevel(root)
    settings_win.title("Settings")
    settings_win.geometry("320x290")
    settings_win.configure(bg=backgroundcolor)
    settings_win.resizable(False, False)
    settings_win.attributes('-topmost', True)

    icon_color = current_theme["backgroundcolor"]
    icon_img = create_icon(icon_color)
    icon_tk = ImageTk.PhotoImage(icon_img)
    settings_win.iconphoto(False, icon_tk)

    settings_label = tk.Label(settings_win, text="\n\n⚙️ Settings ⚙️", font=(font_name, 16, "bold"),
             fg=foregroundcolor, bg=backgroundcolor)
    settings_label.pack(pady=(15, 5))

    global btn_autotyper
    btn_autotyper = tk.Button(settings_win, text="⌨ AutoTyper: Off",
                              font=(font_name, 12),
                              bg=backgroundcolorforbutton,
                              fg=foregroundcolor,
                              activebackground=backgroundcolorforbutton,
                              bd=0,
                              relief="flat",
                              cursor="hand2",
                              highlightthickness=0,
                              command=toggle_autotyper)
    btn_autotyper.pack(pady=10, ipadx=10, ipady=5)

    btn_changetheme = tk.Button(settings_win, text="📁 Change theme",
                     font=(font_name, 12),
                     bg=backgroundcolorforbutton,
                     fg=foregroundcolor,
                     activebackground=backgroundcolorforbutton,
                     bd=0,
                     relief="flat",
                     cursor="hand2",
                     highlightthickness=0,
                     command=change_theme)
    btn_changetheme.pack(pady=5, ipadx=10, ipady=5)

# Reset the tags list (start from the first tag)
def reset_tags():
    global index
    index = 0
    update_label()

# Exit the application
def exit_window():
    root.destroy()
    sys.exit()

# Hotkey listener to bind keys to specific actions
def start_hotkey_listener():
    keyboard.add_hotkey('F4', paste_next_tag)
    keyboard.add_hotkey('F8', load_tags)  # Reload tags manually
    keyboard.add_hotkey('F7', reset_tags)
    keyboard.add_hotkey('F6', open_settings)
    keyboard.add_hotkey('F2', exit_window)

# File system event handler to watch changes in the tags file
class TagFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if filename in event.src_path:
            load_tags()

# Start the file system observer to watch for changes in the tags file
def start_file_watcher():
    observer = Observer()
    handler = TagFileHandler()
    observer.schedule(handler, ".", recursive=False)
    observer.start()

# Load theme settings from a JSON file
def load_theme_from_file(file_path="themes/silver-glow.json"):
    with open(file_path, "r", encoding="utf-8") as file:
        theme = json.load(file)
    return theme

# Create an icon for the application based on the theme color
def create_icon(theme_color):
    size = (16, 16)
    img = Image.new("RGB", size, theme_color)
    draw = ImageDraw.Draw(img)
    draw.ellipse((8, 8, 24, 24), fill=(255, 255, 255))  # Draw a white circle
    return img

# Toggle borderless window mode (for customization)
def toggle_borderless(self, event=None):
    root.overrideredirect(not root.overrideredirect())

# GUI Setup
current_theme = load_theme_from_file()  # Load theme settings
backgroundcolor = current_theme["backgroundcolor"]
backgroundcolorforbutton = current_theme["backgroundcolorforbutton"]
foregroundcolor = current_theme["foregroundcolor"]

root = tk.Tk()
root.title("TagFlow")
root.geometry("400x300")
root.configure(bg=backgroundcolor)

root.bind("<F12>", toggle_borderless)
root.overrideredirect(False)

# Create an icon based on the theme color
icon_color = current_theme["backgroundcolor"]
icon_img = create_icon(icon_color)
icon_tk = ImageTk.PhotoImage(icon_img)
root.iconphoto(False, icon_tk)

font_name = "Consolas"

# Status label to display the current state
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, font=(font_name, 14), fg=foregroundcolor, bg=backgroundcolor)
status_label.pack(pady=40)

# Information label to guide users
info_label = tk.Label(root, text="\nPress F4 to insert the tag\nPress F6 to open settings\nPress F7 to reset\nF2 — exit", font=(font_name, 10), fg=foregroundcolor, bg=backgroundcolor)
info_label.pack()

# Credits label
info_label1 = tk.Label(root, text="\n\n\n\nMade with ❤ by 1mcold", font=(font_name, 10), fg=foregroundcolor, bg=backgroundcolor)
info_label1.pack()

# Load tags initially and start the background threads
load_tags()
threading.Thread(target=start_hotkey_listener, daemon=True).start()
threading.Thread(target=start_file_watcher, daemon=True).start()

root.mainloop()
