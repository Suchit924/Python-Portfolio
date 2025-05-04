from flask import Flask, render_template, request
from core import text_to_morse, morse_to_text

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = ""
    if request.method == 'POST':
        if 'text' in request.form:
            result = text_to_morse(request.form['text'])
        elif 'morse' in request.form:
            result = morse_to_text(request.form['morse'])
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)