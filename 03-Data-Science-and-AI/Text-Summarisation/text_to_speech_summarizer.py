import torch
from transformers import pipeline
import pyttsx3

# Load the summarization pipeline using BART model
summarizer = pipeline("summarization")

# Function to summarize text and read it aloud
def summarize_and_read(text):
    # Generate summary
    summarized_text = summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']

    # Initialize pyttsx3 engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)    # Speed of speech
    engine.setProperty('volume', 1)    # Volume (0.0 to 1.0)

    # Read the summarized text aloud
    engine.say(summarized_text)
    engine.runAndWait()

# Test the summarize_and_read function
testing_text = "Your input text goes here..."
summarize_and_read(testing_text)
