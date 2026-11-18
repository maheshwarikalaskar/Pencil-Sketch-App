# Pencil Sketch App

A Streamlit app that turns a photo into a pencil sketch using OpenCV. It is packaged with Docker, so it runs the same way on any machine.

## Features

- Upload a JPG or PNG and see the original next to the sketch
- Adjustable sketch softness with a slider
- Download the result as a lossless PNG
- Handles transparent PNGs (placed on white paper), greyscale images and phone photos that carry a rotation flag
- Very large photos are scaled down to 2000 px on the longest side to keep the app responsive

## How it works

The sketch is made with the classic colour-dodge technique:

1. Convert the image to greyscale
2. Invert the greyscale image
3. Blur the inverted image with a Gaussian blur
4. Invert the blurred image
5. Divide the greyscale image by the inverted blur (`cv2.divide(gray, inverted_blur, scale=256)`)

Dividing by the blurred negative keeps edges dark and turns flat areas white, which looks like pencil strokes on paper. A larger blur makes the shading softer and bolder.

`pencil-sketch-app.ipynb` walks through the same pipeline step by step in Google Colab.

## Run locally

```bash
git clone https://github.com/maheshwarikalaskar/Pencil-Sketch-App.git
cd Pencil-Sketch-App
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Run with Docker

```bash
docker build -t pencil-sketch-app .
docker run -p 8501:8501 pencil-sketch-app
```

Open http://localhost:8501 in your browser.

### Publish to Docker Hub

```bash
docker login
docker tag pencil-sketch-app <dockerhub-username>/pencil-sketch-app:latest
docker push <dockerhub-username>/pencil-sketch-app:latest
```

## Files

```
.
├── app.py                      # Streamlit app
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── pencil-sketch-app.ipynb     # step-by-step Colab notebook
└── README.md
```

## Tech stack

Python, Streamlit, OpenCV, NumPy, Pillow, Docker

## Possible improvements

- Colour pencil-sketch mode
- Paper texture and stroke-intensity controls
- Webcam input

## Author

**Maheshwari Kalaskar**: [GitHub](https://github.com/maheshwarikalaskar) · [LinkedIn](https://www.linkedin.com/in/maheshwarikalaskar/)
