import tkinter as tk
from core import text_to_morse, morse_to_text


class MorseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Code Converter")

        # Text → Morse
        tk.Label(root, text="Text:").pack(pady=5)
        self.text_entry = tk.Entry(root, width=40)
        self.text_entry.pack(pady=5)

        tk.Button(root, text="→ Morse", command=self.to_morse).pack(pady=5)

        # Morse → Text
        tk.Label(root, text="Morse:").pack(pady=5)
        self.morse_entry = tk.Entry(root, width=40)
        self.morse_entry.pack(pady=5)

        tk.Button(root, text="→ Text", command=self.to_text).pack(pady=5)

        # Result
        self.result = tk.Text(root, height=5, width=40)
        self.result.pack(pady=10)

    def to_morse(self):
        text = self.text_entry.get()
        self.result.delete(1.0, tk.END)
        self.result.insert(tk.END, text_to_morse(text))

    def to_text(self):
        morse = self.morse_entry.get()
        self.result.delete(1.0, tk.END)
        self.result.insert(tk.END, morse_to_text(morse))


if __name__ == "__main__":
    root = tk.Tk()
    app = MorseGUI(root)
    root.mainloop()