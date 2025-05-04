import PyPDF2
from gtts import gTTS
import os

def pdf_to_text(pdf_file):
    """Extracts text from a PDF file."""
    with open(pdf_file, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def text_to_speech(text, output_file="output.mp3"):
    """Converts extracted text to speech and saves it as an MP3 file."""
    tts = gTTS(text)
    tts.save(output_file)
    print(f"Audio saved as {output_file}")

def main():
    pdf_file = input("Enter the path to the PDF file: ")
    text = pdf_to_text(pdf_file)
    if text:
        print("Converting text to speech...")
        text_to_speech(text)
    else:
        print("No text extracted from the PDF.")

if __name__ == "__main__":
    main()
