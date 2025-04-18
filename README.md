# Sleep Detection using Eye Aspect Ratio (EAR)

This project implements a real-time sleep detection system using OpenCV, MediaPipe, and SciPy. The system detects facial landmarks via MediaPipe and calculates the Eye Aspect Ratio (EAR) to determine whether a person's eyes are closed for an extended period, indicating possible drowsiness.

## Features
- Real-time face and eye detection using MediaPipe's Face Mesh.
- Calculation of the Eye Aspect Ratio (EAR) to detect eye closure.
- Visual indication when eyes are closed for a predefined number of frames.
- Uses OpenCV for video capture and GUI display.

## Requirements
Ensure you have the following dependencies installed:

```bash
pip install opencv-python mediapipe numpy scipy

```

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/coolbrickv314/drowsy_driver_coolbrick.git
   cd <repository_folder>
   ```

2. Place the `shape_predictor_68_face_landmarks.dat` file in the same directory as `sleep.py`. You can download it from:
   [Dlib's Pretrained Model](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)

3. Extract and ensure the `.dat` file is in the correct location.

## Running the Script

create a virtual environment

```bash

python3 -m venv env_name

```
source it 

```bash
source sleep-detection-env/bin/activate
```

Run the script:

```bash
python sleep.py
```

## How It Works
- Captures video from your webcam.
- Detects 468 face landmarks using MediaPipe Face Mesh.
- Calculates the EAR for both eyes using selected landmark points.
- Displays "EYES CLOSED!" if the EAR remains below a threshold (default: 0.2) for a set number of consecutive frames (default: 5).
- Displays real-time EAR and facial eye contours.

  
## Parameters
You can fine-tune the detection sensitivity by modifying these parameters in `sleep.py`:

```python
EAR_THRESHOLD = 0.2  # Adjust based on testing
CLOSED_FRAMES_THRESHOLD = 5  # Number of consecutive frames before triggering an alert
```

## Expected Output
- A real-time webcam feed showing face mesh with eye outline, EAR value and "EYES CLOSED!" alert if drowsiness is deteced. 
  

## Troubleshooting
### Common Issues & Fixes

1. **No webcam feed**
   - Chnage camera address. 
     ```bash
     cv2.VideoCapture(1)  # or cv2.VideoCapture(2)
     ```
   - Or test if the webcam is accessible with:
     ```bash
     v4l2-ctl --list-devices
     ```

2. **MediaPipe errors**
   - Reinstall MediaPipe
     ```python
     pip install mediapipe -y
     pip install mediapipe
     ```

3. **Blank window (no face detection)**
   - Ensure lighting and camera permissions
     ```bash
     sudo usermod -aG video $USER # add permission
     groups $USER  # make sure you're in the 'video' group
     ```
   - Try changing the video capture index in `cap = cv2.VideoCapture(0)`. Replace `0` with `1` or `2` if necessary.

## License
This project is open-source and available under the [MIT License](LICENSE).

## Acknowledgments
- MediaPipe for advanced facial landmark detection.
- OpenCV for video processing and display.
- SciPy for geometric distance calculations.
