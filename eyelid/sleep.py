import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist

# EAR function
def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                  max_num_faces=1,
                                  refine_landmarks=True,
                                  min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5)

# Indices for left and right eye (MediaPipe 468 landmarks)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# EAR thresholding
EAR_THRESHOLD = 0.2
CLOSED_FRAMES_THRESHOLD = 5
closed_frames = 0

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        mesh_points = results.multi_face_landmarks[0].landmark

        leftEye = [(int(mesh_points[p].x * w), int(mesh_points[p].y * h)) for p in LEFT_EYE]
        rightEye = [(int(mesh_points[p].x * w), int(mesh_points[p].y * h)) for p in RIGHT_EYE]

        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        # Draw
        cv2.polylines(frame, [np.array(leftEye, dtype=np.int32)], True, (0, 255, 0), 1)
        cv2.polylines(frame, [np.array(rightEye, dtype=np.int32)], True, (0, 255, 0), 1)

        if ear < EAR_THRESHOLD:
            closed_frames += 1
            if closed_frames >= CLOSED_FRAMES_THRESHOLD:
                cv2.putText(frame, "EYES CLOSED!", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            closed_frames = 0

        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Eye Blink Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()