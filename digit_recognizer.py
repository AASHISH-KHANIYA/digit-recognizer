"""
        HANDWRITTEN DIGIT RECOGNIZER (LIVE PREDICTION)

This program allows the user to:

1. Draw a digit (0-9) with smooth, continuous strokes
2. See the prediction update live as they draw
3. Clear and try again

Workflow

User Draws (smooth lines, not dots)
      ↓
Canvas stores drawing (mirrored into a Pillow image)
      ↓
Crop to bounding box, pad to square, add margin (centering)
      ↓
Resize to 28x28
      ↓
Normalize (0-255 → 0-1)
      ↓
Neural Network
      ↓
Prediction + Confidence
"""

# IMPORT LIBRARIES

import tkinter as tk              # GUI
from PIL import Image, ImageDraw  # Image processing
import tensorflow as tf           # Load AI model
import numpy as np                # Arrays & Math
import sys
import os


# LOAD TRAINED MODEL


def resource_path(relative_path):
    """Get the absolute path to a resource, works for dev and for PyInstaller .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

model = tf.keras.models.load_model(resource_path("digit_model.keras"))


# CREATE MAIN WINDOW

root = tk.Tk()
root.title("Handwritten Digit Recognizer")
root.geometry("420x520")
root.configure(bg="#2b2b2b")


# HEADING

title = tk.Label(
    root,
    text="Draw a Digit",
    font=("Arial", 18, "bold"),
    bg="#2b2b2b",
    fg="white"
)
title.pack(pady=10)


# DRAWING CANVAS

canvas_width = 280
canvas_height = 280

canvas = tk.Canvas(
    root,
    width=canvas_width,
    height=canvas_height,
    bg="black",
    highlightthickness=2,
    highlightbackground="white"
)
canvas.pack()


# PIL IMAGE (mirrors the canvas so we can read pixels)

image = Image.new("L", (canvas_width, canvas_height), color=0)
draw = ImageDraw.Draw(image)


# RESULT LABEL

result_label = tk.Label(
    root,
    text="Start drawing...",
    font=("Arial", 16),
    bg="#2b2b2b",
    fg="cyan"
)
result_label.pack(pady=10)


# STATE

predict_job = None       # holds the scheduled "after" call so we can cancel/reschedule it
last_x, last_y = None, None   # tracks the previous point in the current stroke


# DRAW FUNCTION

def paint(event):
    """
    Called whenever the user moves the mouse while holding the left
    mouse button. Connects the previous point to the current one with
    a line (so fast strokes come out solid, not dotted), draws on both
    the visible canvas and the in-memory Pillow image, then schedules
    a prediction.
    """
    global last_x, last_y

    x = event.x
    y = event.y
    radius = 5

    if last_x is not None:
        # Connect the previous point to this one -- fills the gaps
        canvas.create_line(
            last_x, last_y, x, y,
            fill="white", width=radius * 2,
            capstyle=tk.ROUND, smooth=True
        )
        draw.line(
            [last_x, last_y, x, y],
            fill=255, width=radius * 2
        )

    # Also draw a dot, so single clicks (no drag) still show something
    # and stroke ends look rounded rather than flat
    canvas.create_oval(
        x-radius, y-radius, x+radius, y+radius,
        fill="white", outline="white"
    )
    draw.ellipse(
        (x-radius, y-radius, x+radius, y+radius),
        fill=255
    )

    last_x, last_y = x, y
    schedule_predict()


def reset_stroke(event):
    """
    Called when the mouse button is released, so the next stroke
    starts fresh instead of drawing a stray line connecting it
    to where the last stroke ended.
    """
    global last_x, last_y
    last_x, last_y = None, None


def schedule_predict():
    """
    Debounce: cancel any pending prediction and schedule a new one
    1ms from now. If the user is still actively drawing, this keeps
    getting cancelled and rescheduled, so predict() only actually runs
    once movement pauses briefly -- not on every single mouse-move event.
    """
    global predict_job
    if predict_job is not None:
        root.after_cancel(predict_job)
    predict_job = root.after(1, predict)


canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", reset_stroke)


# PREDICT FUNCTION

def predict():

    # Find the bounding box of the drawing
    bbox = image.getbbox()

    # If nothing is drawn
    if bbox is None:
        result_label.config(text="Start drawing...")
        return

    # Crop only the digit
    cropped = image.crop(bbox)

    # --- Make it square, preserving aspect ratio ---
    w, h = cropped.size
    side = max(w, h)

    square = Image.new("L", (side, side), color=0)
    paste_x = (side - w) // 2
    paste_y = (side - h) // 2
    square.paste(cropped, (paste_x, paste_y))

    # --- Add margin so the digit doesn't touch the edges (like MNIST) ---
    margin = int(side * 0.2)
    padded_side = side + 2 * margin

    padded = Image.new("L", (padded_side, padded_side), color=0)
    padded.paste(square, (margin, margin))

    # --- Resize the padded square to 28x28 ---
    img = padded.resize((28, 28), Image.LANCZOS)

    # --- Normalize and predict ---
    img_arr = np.array(img).astype("float32") / 255.0
    img_arr = img_arr.reshape(1, 28, 28)

    prediction = model.predict(img_arr, verbose=0)
    digit = np.argmax(prediction)
    confidence = np.max(prediction) * 100

    result_label.config(
        text=f"Prediction : {digit}\nConfidence : {confidence:.2f}%"
    )


# CLEAR FUNCTION

def clear_canvas():
    global predict_job, last_x, last_y

    # Cancel any pending live prediction so it doesn't fire on a blank canvas
    if predict_job is not None:
        root.after_cancel(predict_job)
        predict_job = None

    last_x, last_y = None, None

    canvas.delete("all")

    draw.rectangle(
        (0, 0, canvas_width, canvas_height),
        fill=0
    )

    result_label.config(text="Start drawing...")


# BUTTON FRAME

button_frame = tk.Frame(root, bg="#2b2b2b")
button_frame.pack(pady=10)

clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_canvas,
    font=("Arial", 13, "bold"),
    bg="#f44336",
    fg="white",
    width=12
)
clear_button.grid(row=0, column=0, padx=10)


# START APPLICATION

root.mainloop()