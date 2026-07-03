# Handwritten Digit Recognizer

Draw a digit with your mouse and a neural network (trained on MNIST) predicts
it live as you draw.

## Project files

- `train_model.py` — trains the neural network on MNIST, saves `digit_model.keras`
- `digit_recognizer.py` — Tkinter app: draw a digit, see a live prediction
- `digit_model.keras` — the trained model (already included, no need to retrain)
- `requirements.txt` — Python dependencies
- `Dockerfile` — containerizes the app

## Run it locally (no Docker)

```bash
pip install -r requirements.txt
python digit_recognizer.py
```

## Run it with Docker

Tkinter opens a GUI window, and a Docker container has no display by
default. You need to forward your host machine's display into the
container. Steps differ slightly by OS.

### Build the image (same on every OS)

```bash
docker build -t digit-recognizer .
```

### Linux

```bash
xhost +local:docker
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix digit-recognizer
```

### macOS

1. Install [XQuartz](https://www.xquartz.org/) and open it once.
2. In XQuartz preferences → Security, enable "Allow connections from network clients".
3. Then:

```bash
xhost + 127.0.0.1
docker run -e DISPLAY=host.docker.internal:0 digit-recognizer
```

### Windows

1. Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) and launch it
   with "Disable access control" checked.
2. Then, in PowerShell:

```powershell
docker run -e DISPLAY=host.docker.internal:0.0 digit-recognizer
```

If the window doesn't appear, the display forwarding is almost always the
cause — double check the DISPLAY value and that the X server (XQuartz/VcXsrv)
is actually running before `docker run`.

## Run it with Docker Compose

Compose doesn't remove the display-forwarding requirement above — it just
saves you from typing the `-e`/`-v` flags every time. `docker-compose.yml`
reads `DISPLAY` from your shell's environment variable, so export it first.

### Linux

```bash
xhost +local:docker
export DISPLAY=$DISPLAY
docker compose up --build
```

### macOS

1. Install and open [XQuartz](https://www.xquartz.org/); enable "Allow
   connections from network clients" in its Security preferences.
2. Then:

```bash
xhost + 127.0.0.1
export DISPLAY=host.docker.internal:0
docker compose up --build
```

### Windows

`docker-compose.yml` as written uses the Linux/macOS X11 socket path, which
doesn't exist on Windows. Simplest option: skip Compose on Windows and use
the plain `docker run` command above with VcXsrv running. (If you want a
Compose file that works on Windows too, tell me and I'll add an
`environment`-only version without the `/tmp/.X11-unix` volume mount.)

To stop the container: `docker compose down`

## Push to GitHub

```bash
git init
git add .
git commit -m "Handwritten digit recognizer with live prediction"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

(Create the empty repo on GitHub first, without a README, so there's no
merge conflict on first push.)