# Gesture Volume Control

Control your Windows system volume with hand gestures using your webcam.
Move your **thumb** and **index finger** apart to raise the volume, and bring them together to lower it.

Built with Python, OpenCV, MediaPipe and pycaw.

## How it works

1. OpenCV captures frames from the webcam.
2. MediaPipe Hands detects 21 landmarks on your hand.
3. The distance between the thumb tip (landmark 4) and index fingertip (landmark 8) is measured.
4. That distance is mapped to the system volume range and applied with pycaw.
5. A volume bar and percentage are drawn on screen, along with the FPS.

## Project structure

```
Gesture Volume Control/
├── HandTrackingModule.py   # Reusable hand detector class (MediaPipe wrapper)
├── VolumeHandControl.py    # Main app: gesture -> system volume
├── main.py                 # Quick check of installed library versions
├── requirements.txt        # Python dependencies
└── README.md
```

## Requirements

- Windows (pycaw only works on Windows)
- Python 3.9 - 3.12
- A working webcam

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/IshanNaikele/Gesture-Volume-Control.git
cd Gesture-Volume-Control.git

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

> MediaPipe is pinned to `0.10.21` because newer versions removed the `mp.solutions` API used here.

## Usage

Check the installation:

```bash
python main.py
```

Test hand tracking only:

```bash
python HandTrackingModule.py
```

Run the volume control:

```bash
python VolumeHandControl.py
```

Press **q** in the video window to quit.

## Configuration

Edit the settings at the top of `VolumeHandControl.py`:

| Setting | Default | Description |
|---|---|---|
| `CAMERA_INDEX` | `0` | Webcam to use (try `1` if the camera does not open) |
| `MIN_LEN`, `MAX_LEN` | `50`, `300` | Thumb-index distance range in pixels |
| `SMOOTHNESS` | `5` | Volume changes in steps of this percentage (`0` disables smoothing) |

## Troubleshooting

| Problem | Fix |
|---|---|
| "Could not read from camera" | Change `CAMERA_INDEX`, close other apps using the webcam |
| `module 'mediapipe' has no attribute 'solutions'` | `pip install mediapipe==0.10.21` |
| pycaw / comtypes errors | `pip install --upgrade pycaw comtypes` |
| Volume range feels off | Adjust `MIN_LEN` and `MAX_LEN` |

## Future improvements

- Gesture to "lock" the volume (for example, pinky down)
- Support for left and right hand
- Mute / unmute gesture
- Cross-platform volume control

## Acknowledgements

- [MediaPipe](https://developers.google.com/mediapipe)
- [OpenCV](https://opencv.org/)
- [pycaw](https://github.com/AndreMiras/pycaw)