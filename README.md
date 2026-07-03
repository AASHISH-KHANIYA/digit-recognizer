Handwritten Digit Recognizer

A neural network that recognizes handwritten digits (0–9) in real time. Draw
on the canvas and watch the prediction update live as you write — powered by
a TensorFlow/Keras model trained on MNIST, wrapped in a Tkinter desktop app,
and fully containerized with Docker.

Demo


Draw a digit → the model predicts it instantly, with a confidence score.



(Add a screenshot or GIF of the app here once you have one — drag an image
into this README on GitHub and it'll generate the markdown for you.)

Features


Live prediction — no button click needed, the model predicts as you draw
Smooth strokes — connected line drawing instead of dotted output
Auto-centering preprocessing — crops, centers, and pads your drawing to
match the MNIST format the model was trained on, for much better accuracy
Dockerized — run it in a container with no local Python setup required


Tech stack

LayerToolModelTensorFlow / Keras (Dense neural network)Training dataMNIST (60,000 handwritten digit images)GUIPython TkinterImage processingPillow (PIL)ContainerizationDocker / Docker Compose

Project structure

digit-recognizer/
├── train_model.py       # Trains the neural network on MNIST, saves digit_model.keras
├── digit_recognizer.py  # Tkinter app: draw a digit, get a live prediction
├── digit_model.keras    # Pre-trained model (included, no need to retrain)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container image definition
├── docker-compose.yml   # Compose config (Linux/macOS display forwarding)
└── README.md

How it works

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

The centering/padding step matters more than it might seem — without it, a
digit drawn off-center or with a different aspect ratio than training data
gets misclassified with high (and misleading) confidence.

Getting started

Option 1 — Run locally with Python

bashpip install -r requirements.txt
python digit_recognizer.py

(digit_model.keras is already included — no need to run train_model.py
unless you want to retrain it yourself.)

Option 2 — Run with Docker

Tkinter opens a GUI window, and Docker containers have no display by
default, so you need to forward your host's display into the container.

Build the image:

bashdocker build -t digit-recognizer .

Linux:

bashxhost +local:docker
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix digit-recognizer

macOS (requires XQuartz, with "Allow
connections from network clients" enabled in its preferences):

bashxhost + 127.0.0.1
docker run -e DISPLAY=host.docker.internal:0 digit-recognizer

Windows (requires VcXsrv,
launched via XLaunch with "Disable access control" checked):

powershelldocker run -e DISPLAY=host.docker.internal:0.0 digit-recognizer

Option 3 — Docker Compose (Linux/macOS)

bashxhost +local:docker      # or `xhost + 127.0.0.1` on macOS
export DISPLAY=$DISPLAY  # or host.docker.internal:0 on macOS
docker compose up --build


Note: the included docker-compose.yml uses the Linux/macOS X11
socket path and isn't compatible with Windows as-is. On Windows, use the
docker run command above instead.



Retraining the model

If you want to retrain from scratch (e.g. with a different architecture or
more epochs):

bashpython train_model.py

This downloads MNIST, trains a small neural network for 5 epochs, evaluates
it on the test set, and overwrites digit_model.keras.

Known limitations


Accuracy on handwriting can be lower than the ~98% test accuracy seen
during training, since MNIST digits are cleaner and more standardized
than freehand mouse drawings
Very thin or very thick strokes, or digits drawn far off-center despite
the auto-centering, can still occasionally confuse the model


License

This project is open source and available for personal or educational use.
