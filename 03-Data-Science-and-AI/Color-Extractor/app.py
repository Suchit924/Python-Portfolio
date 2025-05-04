from flask import Flask, render_template, request, send_from_directory
import os
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def extract_colors(image_path, num_colors=10):
    image = Image.open(image_path)
    image = image.convert('RGB')
    image = image.resize((300, 300))  # Resize for faster processing
    np_image = np.array(image).reshape((-1, 3))
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(np_image)
    colors = kmeans.cluster_centers_.astype(int)
    hex_colors = ['#%02x%02x%02x' % tuple(color) for color in colors]
    return hex_colors

@app.route('/', methods=['GET', 'POST'])
def index():
    colors = []
    image_url = None
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            colors = extract_colors(filepath)
            image_url = f'/static/uploads/{filename}'
    return render_template('index.html', colors=colors, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True)
