# 🎨 Color Extractor

A Python-based application that extracts the most dominant colors from any image using KMeans clustering. Perfect for designers, artists, or developers who want to quickly get a color palette from an image.

---

## 📌 Features

- 🔍 Automatically identifies the top **N dominant colors** in an image.
- 🎯 Supports multiple image formats (`.jpg`, `.png`, `.jpeg`, etc.)
- 🧠 Uses **KMeans clustering** to find representative color centroids.
- 🌈 Visualizes the color palette alongside RGB or HEX values.
- 🖼️ Optional: Save the palette as an image or JSON file.

---

## 🛠️ Technologies Used

- Python
- `OpenCV` or `Pillow` – for image processing
- `scikit-learn` – for KMeans clustering
- `matplotlib` – for plotting the extracted colors
- `NumPy` – for efficient array manipulation

---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Suchit924/Color-Extractor.git
   cd Color-Extractor

2. Install the dependencies:
   ```bash
   pip install -requirement

3. Run the script:
   ```bash
   python app.py
