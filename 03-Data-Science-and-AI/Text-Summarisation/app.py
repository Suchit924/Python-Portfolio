from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from predict import summarize
from preprocing import get
import requests
from text_to_speech_summarizer import summarize_and_read  # Import the text-to-speech function

app = Flask(__name__)

# Function to create SQLite database
def create_connection():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

create_connection()

# api-endpoint
@app.route("/")
def home():
    URL = "https://newsapi.org/v2/everything?q=apple&from=2025-04-30&to=2025-04-30&sortBy=popularity&apiKey=8ab298c2994346dda6a7eb5b110a4df7"
    r = requests.get(url = URL)
    data = r.json()
    print(data)
    #title=data["articles"]["title"]
    #discriptions=data["articles"]["description"]
    return render_template("Home.html",data=data)


@app.route("/text", methods=["GET", "POST"])
def predict():
    return render_template("text.html")

@app.route("/output", methods=["POST"])
def output():
    text = request.form.get("text")
    summarized_text = summarize(paragraph=text)
    
    # Call the text-to-speech function to read the summarized text aloud
    summarize_and_read(summarized_text)
    
    output = get(text)
    return render_template("text.html", output=output)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            # Redirect to home page after successful login
            return redirect(url_for('home'))
        else:
            return "Invalid username or password"
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)
