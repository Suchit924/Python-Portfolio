import tkinter as tk
import time
import random
from datetime import datetime

# Sample texts for different difficulty levels
SAMPLE_TEXTS = {
    "Easy": [
        "The quick brown fox jumps over the lazy dog.",
        "Typing is fun.",
        "I love programming."
    ],
    "Medium": [
        "Practice makes perfect when it comes to typing.",
        "Python is a powerful language for building applications.",
        "A journey of a thousand miles begins with a single step."
    ],
    "Hard": [
        "The curious case of the fast fox jumps over complex obstacles.",
        "With great power comes great responsibility in the programming world.",
        "Solving intricate puzzles with precision is the key to mastering algorithms."
    ]
}

LEADERBOARD_FILE = "leaderboard.txt"

class TypingSpeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test with Timer & Difficulty")
        self.root.geometry("800x600")
        self.start_time = None
        self.sample_text = ""
        self.timer_running = False
        self.time_left = 60
        self.difficulty = "Easy"

        # Dropdown for selecting difficulty level
        self.difficulty_label = tk.Label(root, text="Select Difficulty", font=("Arial", 12))
        self.difficulty_label.pack(pady=10)
        self.difficulty_dropdown = tk.OptionMenu(root, tk.StringVar(value=self.difficulty), "Easy", "Medium", "Hard", command=self.set_difficulty)
        self.difficulty_dropdown.pack()

        # Sample text
        self.sample_label = tk.Label(root, text="", wraplength=700, font=("Arial", 14))
        self.sample_label.pack(pady=20)

        # Timer label
        self.timer_label = tk.Label(root, text=f"Time left: {self.time_left}s", font=("Arial", 12))
        self.timer_label.pack(pady=10)

        # Text input box
        self.input_text = tk.Text(root, height=5, font=("Arial", 14))
        self.input_text.pack()
        self.input_text.bind("<KeyPress>", self.start_typing)
        self.input_text.bind("<Return>", self.complete_task)  # Bind Enter key

        # Result label
        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        # Buttons
        self.reset_button = tk.Button(root, text="Reset", command=self.reset, font=("Arial", 12))
        self.reset_button.pack(pady=5)

        # Leaderboard label
        self.leaderboard_title = tk.Label(root, text="🏆 Leaderboard (Top 5)", font=("Arial", 14, "bold"))
        self.leaderboard_title.pack(pady=10)

        self.leaderboard_box = tk.Text(root, height=8, width=70, font=("Courier", 12))
        self.leaderboard_box.pack()
        self.leaderboard_box.config(state=tk.DISABLED)

        self.show_leaderboard()
        self.set_difficulty(self.difficulty)

    def set_difficulty(self, level):
        self.difficulty = level
        self.sample_text = random.choice(SAMPLE_TEXTS[self.difficulty])
        self.sample_label.config(text=self.sample_text)
        self.time_left = 60
        self.timer_label.config(text=f"Time left: {self.time_left}s")
        self.reset()

    def start_typing(self, event):
        if self.start_time is None and not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True
            self.start_timer()

    def complete_task(self, event):
        """Complete task on Enter key press."""
        if not self.timer_running:
            return  # Prevent action if timer isn't running
        self.calculate_results()

    def start_timer(self):
        if self.time_left > 0 and self.timer_running:
            self.time_left = 60 - int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.root.after(1000, self.start_timer)  # Update every second
        else:
            if self.time_left <= 0:
                self.calculate_results()

    def calculate_results(self):
        end_time = time.time()
        time_taken = end_time - self.start_time
        typed_text = self.input_text.get("1.0", tk.END).strip()
        word_count = len(typed_text.split())
        wpm = round((word_count / time_taken) * 60)

        correct_chars = sum(1 for i, c in enumerate(typed_text) if i < len(self.sample_text) and c == self.sample_text[i])
        accuracy = round((correct_chars / len(self.sample_text)) * 100)

        result = f"Speed: {wpm} WPM | Accuracy: {accuracy}%"
        self.result_label.config(text=result)
        self.input_text.config(state=tk.DISABLED)

        # Save to leaderboard
        self.save_to_leaderboard(wpm, accuracy)
        self.show_leaderboard()

    def reset(self):
        self.sample_text = random.choice(SAMPLE_TEXTS[self.difficulty])
        self.sample_label.config(text=self.sample_text)
        self.input_text.config(state=tk.NORMAL)
        self.input_text.delete("1.0", tk.END)
        self.result_label.config(text="")
        self.start_time = None
        self.timer_running = False
        self.time_left = 60
        self.timer_label.config(text=f"Time left: {self.time_left}s")

    def save_to_leaderboard(self, wpm, accuracy):
        with open(LEADERBOARD_FILE, "a") as file:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{now} | {wpm} WPM | {accuracy}% Accuracy\n")

    def show_leaderboard(self):
        try:
            with open(LEADERBOARD_FILE, "r") as file:
                lines = file.readlines()
            # Show top 5 most recent
            top_scores = lines[-5:]
            top_scores.reverse()
        except FileNotFoundError:
            top_scores = ["No data yet.\n"]

        self.leaderboard_box.config(state=tk.NORMAL)
        self.leaderboard_box.delete("1.0", tk.END)
        for line in top_scores:
            self.leaderboard_box.insert(tk.END, line)
        self.leaderboard_box.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedApp(root)
    root.mainloop()
