# Base image with Python
FROM python:3.11-slim

# Tkinter isn't included in the base Python image on Debian/Ubuntu --
# it needs the system package python3-tk, plus some X11 libs it depends on.
RUN apt-get update && apt-get install -y \
    python3-tk \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first so Docker can cache this layer
# (rebuilds are faster if you only change app code, not dependencies)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code and the trained model
COPY digit_recognizer.py .
COPY digit_model.keras .

# Tkinter needs a DISPLAY to draw its window -- this gets passed in
# at "docker run" time via -e DISPLAY=$DISPLAY, not set here.
CMD ["python", "digit_recognizer.py"]
