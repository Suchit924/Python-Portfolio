import tkinter as tk
import time
import threading
from tkinter import filedialog


class DangerousWritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Most Dangerous Writing App")

        # Initialize variables
        self.timer_interval = 5  
        self.last_key_time = time.time()
        self.time_left = self.timer_interval

        # Set up text area
        self.text_area = tk.Text(root, height=15, width=80)
        self.text_area.pack()

        # Set up progress bar
        self.progress = tk.Scale(root, from_=self.timer_interval, to=0, orient="horizontal", length=500,
                                 showvalue=False)
        self.progress.pack()

        # Set up time limit input
        self.time_limit_label = tk.Label(root, text="Set time limit (seconds):")
        self.time_limit_label.pack()
        self.time_limit_entry = tk.Entry(root)
        self.time_limit_entry.insert(0, str(self.timer_interval))
        self.time_limit_entry.pack()

        # Set up save button
        self.save_button = tk.Button(root, text="Save Text", command=self.save_text)
        self.save_button.pack()

        # Start the timer thread
        self.timer_thread = threading.Thread(target=self.check_inactivity)
        self.timer_thread.daemon = True
        self.timer_thread.start()

        # Bind keypress event
        self.text_area.bind("<KeyPress>", self.on_key_press)

    def check_inactivity(self):
        while True:
            current_time = time.time()
            self.time_left = max(self.timer_interval - (current_time - self.last_key_time), 0)
            self.progress.set(self.time_left)

            if self.time_left == 0:
                self.delete_text()

            time.sleep(1)

    def delete_text(self):
        self.text_area.delete(1.0, tk.END)
        self.last_key_time = time.time()  # reset time after deletion

    def on_key_press(self, event):
        # Reset the timer whenever a key is pressed
        self.last_key_time = time.time()

        # Update the progress bar
        try:
            self.timer_interval = int(self.time_limit_entry.get())  # Set time limit dynamically
        except ValueError:
            pass  # In case of invalid input, keep the default value

    def save_text(self):
        # Get text from text area
        text = self.text_area.get(1.0, tk.END).strip()

        if text:  # Only save if there's some text
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, "w") as file:
                    file.write(text)
                print(f"Text saved to {file_path}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = DangerousWritingApp(root)
    app.run()
