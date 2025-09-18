# Pencil-Sketch-App

This is a Streamlit app that converts images into pencil sketches. The app is dockerized so it can run anywhere easily.

# How We Created the Docker Image

1)Prepare the project folder
Keep your app.py (Streamlit app) and requirements.txt (list of Python packages your app needs) in the folder.

2)Create requirements.txt
Example packages:

streamlit
opencv-python
numpy


3)Write a Dockerfile

Example:

FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]


4)Build the Docker image

docker build -t pencil-sketch-app .


5)Run the app locally (optional)

docker run -p 8501:8501 pencil-sketch-app


Open http://localhost:8501 in your browser.

6)Login to Docker Hub
docker login


7)Tag the image
docker tag pencil-sketch-app yourdockerhubusername/pencil-sketch-app:latest


8)Push to Docker Hub
docker push yourdockerhubusername/pencil-sketch-app:latest


9)Check your Docker Hub
Go to your account → Repositories → Pencil Sketch App
You should see your image there.
