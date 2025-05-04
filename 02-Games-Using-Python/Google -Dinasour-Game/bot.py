import pyautogui
from PIL import ImageGrab, ImageTk
import tkinter as tk
import threading
import time

# Detection box default values (these should be tweaked)
left, top, right, bottom = 340, 390, 440, 410
bot_running = False

def is_obstacle_in_path():
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    pixels = screenshot.load()

    dark_pixel_count = 0
    for x in range(screenshot.size[0]):
        for y in range(screenshot.size[1]):
            r, g, b = pixels[x, y]
            if r < 100 and g < 100 and b < 100:
                dark_pixel_count += 1

    # Only jump if a significant number of dark pixels (e.g. cactus) appear
    return dark_pixel_count > 15

def play_game():
    global bot_running
    time.sleep(2)
    pyautogui.press('space')  # Start the game

    while bot_running:
        if is_obstacle_in_path():
            pyautogui.press('space')
            time.sleep(0.15)

def start_bot():
    global bot_running
    bot_running = True
    status_label.config(text="Bot Running...", fg="green")
    threading.Thread(target=play_game).start()

def stop_bot():
    global bot_running
    bot_running = False
    status_label.config(text="Bot Stopped", fg="red")

def show_preview():
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    screenshot = screenshot.resize((200, 50))
    img = ImageTk.PhotoImage(screenshot)
    preview_label.config(image=img)
    preview_label.image = img
    root.after(500, show_preview)

# GUI
root = tk.Tk()
root.title("T-Rex Auto Player")
root.geometry("350x300")

tk.Label(root, text="Google Dino Bot", font=("Arial", 16)).pack(pady=10)

tk.Button(root, text="Start Bot", command=start_bot, bg="green", fg="white").pack(pady=5)
tk.Button(root, text="Stop Bot", command=stop_bot, bg="red", fg="white").pack(pady=5)

status_label = tk.Label(root, text="Bot Not Running", fg="red")
status_label.pack(pady=10)

tk.Label(root, text="Detection Area Preview").pack()
preview_label = tk.Label(root)
preview_label.pack()

tk.Label(root, text="Make sure Chrome is fullscreen on https://elgoog.im/t-rex").pack(pady=5)

# Start live preview
show_preview()

root.mainloop()
