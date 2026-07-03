#  Handwritten Digit Recognizer

A neural network that recognizes handwritten digits (0–9) in real time. Draw
on the canvas and watch the prediction update live as you write — powered by
a TensorFlow/Keras model trained on MNIST, wrapped in a Tkinter desktop app.

## Demo

> Draw a digit → the model predicts it instantly, with a confidence score.

*(Add a screenshot or GIF of the app here — drag an image into this README
on GitHub's web editor and it'll generate the markdown for you.)*

## Features

- **Live prediction** — no button click needed, the model predicts as you draw
- **Smooth strokes** — connected line drawing instead of dotted output
- **Auto-centering preprocessing** — crops, centers, and pads your drawing to
  match the MNIST format the model was trained on, for much better accuracy
- **Standalone .exe available** — no Python install required to run it (see
  [Releases](../../releases))

## Tech stack

| Layer          | Tool                          |
|-----------------|-------------------------------|
| Model           | TensorFlow / Keras (Dense neural network) |
| Training data   | MNIST (60,000 handwritten digit images)   |
| GUI             | Python Tkinter                |
| Image processing| Pillow (PIL)                  |
| Packaging       | PyInstaller (Windows .exe)    |

## Project structure

```
digit-recognizer/
├── train_model.py       # Trains the neural network on MNIST, saves digit_model.keras
├── digit_recognizer.py  # Tkinter app: draw a digit, get a live prediction
├── digit_model.keras    # Pre-trained model (included, no need to retrain)
├── requirements.txt     # Python dependencies
└── README.md
```

## How it works

```
User draws on canvas
        ↓
Drawing mirrored into a Pillow image (Tkinter can't be read as pixels directly)
        ↓
Crop to the drawing's bounding box
        ↓
Pad to a square + add margin (centers the digit, matching MNIST's format)
        ↓
Resize to 28x28, normalize pixel values to [0, 1]
        ↓
Neural network inference
        ↓
Predicted digit + confidence, updated live
```

The centering/padding step matters more than it might seem — without it, a
digit drawn off-center or with a different aspect ratio than training data
gets misclassified with high (and misleading) confidence.

## Getting started

### Option 1 — Download the standalone .exe (Windows, no setup required)

Grab the latest `DigitRecognizer.exe` from the [Releases](../../releases)
page and just run it. No Python, no dependencies.

### Option 2 — Run from source with Python

```bash
pip install -r requirements.txt
python digit_recognizer.py
```

(`digit_model.keras` is already included — no need to run `train_model.py`
unless you want to retrain it yourself.)

## Building the .exe yourself

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "digit_model.keras;." --name DigitRecognizer digit_recognizer.py
```

The resulting exe will be in `dist/DigitRecognizer.exe`. This bundles
TensorFlow and all dependencies into a single file, so expect a large
(300-600MB) executable and a build time of 5-15+ minutes.

## Retraining the model

If you want to retrain from scratch (e.g. with a different architecture or
more epochs):

```bash
python train_model.py
```

This downloads MNIST, trains a small neural network for 5 epochs, evaluates
it on the test set, and overwrites `digit_model.keras`.

## Known limitations

- Accuracy on handwriting can be lower than the ~98% test accuracy seen
  during training, since MNIST digits are cleaner and more standardized
  than freehand mouse drawings
- Very thin or very thick strokes, or digits drawn far off-center despite
  the auto-centering, can still occasionally confuse the model

## License

This project is open source and available for personal or educational use.