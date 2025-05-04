import tkinter as tk
from tkinter import filedialog, messagebox
from gtts import gTTS
import PyPDF2
import os
from tkinter import ttk


def pdf_to_text(pdf_file):
    """Extracts text from a PDF file."""
    try:
        with open(pdf_file, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            return text
    except Exception as e:
        messagebox.showerror("Error", f"Error reading PDF: {e}")
        return None


def text_to_speech(text, output_file="output.mp3", lang="en"):
    """Converts extracted text to speech and saves it as an MP3 file."""
    try:
        tts = gTTS(text, lang=lang)
        tts.save(output_file)
        messagebox.showinfo("Success", f"Audio saved as {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Error during text-to-speech conversion: {e}")


def get_language_choice():
    """Gets language choice from dropdown."""
    return language_var.get()


def handle_large_pdfs(pdf_file, progress_var):
    """Handles large PDFs by processing each page with user confirmation."""
    with open(pdf_file, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        for page_num in range(total_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            if text:
                output_file = f"page_{page_num + 1}.mp3"
                text_to_speech(text, output_file=output_file, lang=get_language_choice())
            else:
                print(f"Page {page_num + 1} has no extractable text.")

            # Update the progress bar
            progress_var.set((page_num + 1) / total_pages * 100)
            root.update_idletasks()  # Update the UI
            if page_num < total_pages - 1:
                progress_var.set((page_num + 1) / total_pages * 100)


def select_pdf_file():
    """Opens a file dialog to select a PDF file."""
    pdf_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if pdf_file:
        pdf_entry.delete(0, tk.END)  # Clear the entry field
        pdf_entry.insert(0, pdf_file)  # Insert the selected file path


def convert_pdf_to_speech():
    """Main function to convert PDF to speech."""
    pdf_file = pdf_entry.get()
    if not os.path.isfile(pdf_file):
        messagebox.showerror("Error", "Invalid file path.")
        return

    text = pdf_to_text(pdf_file)
    if text:
        lang = get_language_choice()

        # Get custom output file name and add .mp3 extension if not provided
        output_file = output_file_entry.get().strip()
        if not output_file:
            output_file = "../output.mp3"
        elif not output_file.endswith(".mp3"):
            output_file += ".mp3"

        # Process the PDF with a progress bar
        progress_var.set(0)
        handle_large_pdfs(pdf_file, progress_var)


def setup_gui():
    """Sets up the main Tkinter GUI window."""
    global root, pdf_entry, output_file_entry, language_var, progress_var

    root = tk.Tk()
    root.title("PDF to Speech Converter")

    # PDF file selection
    tk.Label(root, text="Select PDF File:").pack(padx=20, pady=5)
    pdf_entry = tk.Entry(root, width=40)
    pdf_entry.pack(padx=20, pady=5)
    tk.Button(root, text="Browse", command=select_pdf_file).pack(padx=20, pady=5)

    # Language selection
    tk.Label(root, text="Select Language:").pack(padx=20, pady=5)
    language_var = tk.StringVar(value="en")
    language_choices = ["en", "es", "fr", "de"]
    language_menu = ttk.Combobox(root, textvariable=language_var, values=language_choices)
    language_menu.pack(padx=20, pady=5)

    # Output file name
    tk.Label(root, text="Enter Output File Name (Optional):").pack(padx=20, pady=5)
    output_file_entry = tk.Entry(root, width=40)
    output_file_entry.pack(padx=20, pady=5)

    # Convert button
    tk.Button(root, text="Convert to Speech", command=convert_pdf_to_speech).pack(pady=20)

    # Progress bar
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.pack(padx=20, pady=20, fill="x")

    root.mainloop()


if __name__ == "__main__":
    setup_gui()
