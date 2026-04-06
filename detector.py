import cv2
import mediapipe as mp
import numpy as np
import urllib.request
import os

MODEL_PATH = "face_landmarker.task"

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading model...")
        url = ("https://storage.googleapis.com/mediapipe-models/"
               "face_landmarker/face_landmarker/float16/1/face_landmarker.task")
        urllib.request.urlretrieve(url, MODEL_PATH)
        print("Model ready.")

download_model()

BaseOptions        = mp.tasks.BaseOptions
FaceLandmarker     = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOpts = mp.tasks.vision.FaceLandmarkerOptions
RunningMode        = mp.tasks.vision.RunningMode

options = FaceLandmarkerOpts(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.IMAGE,
    num_faces=10,
    min_face_detection_confidence=0.5,
    min_face_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

landmarker = FaceLandmarker.create_from_options(options)

# ── Pitch: how far nose drops below ear level ─────────────────────────────────
# y=0 is TOP of image, y=1 is BOTTOM
# Looking straight → nose.y ≈ ear.y  → pitch ≈ 0.00 to 0.05
# Looking down     → nose.y >> ear.y → pitch > 0.10
def get_head_pitch(landmarks):
    nose      = landmarks[1]
    left_ear  = landmarks[234]
    right_ear = landmarks[454]
    ear_mid_y = (left_ear.y + right_ear.y) / 2.0
    return nose.y - ear_mid_y   # positive = nose below ears = looking down

# ── Yaw: how much head is turned left/right ───────────────────────────────────
# Wide ear gap = facing camera. Narrow = turned away.
def get_head_yaw(landmarks):
    left_ear  = landmarks[234]
    right_ear = landmarks[454]
    return abs(right_ear.x - left_ear.x)   # small = turned away

# ── Gaze: iris position within eye socket ─────────────────────────────────────
def get_gaze_ratio(landmarks):
    try:
        l_left  = landmarks[33]
        l_right = landmarks[133]
        l_iris  = landmarks[468]
        r_left  = landmarks[362]
        r_right = landmarks[263]
        r_iris  = landmarks[473]

        def ratio(eye_l, eye_r, iris):
            width = abs(eye_r.x - eye_l.x)
            return (iris.x - eye_l.x) / width if width > 0.001 else 0.5

        return (ratio(l_left, l_right, l_iris) + ratio(r_left, r_right, r_iris)) / 2.0
    except Exception:
        return 0.5

# ── Mouth open (yawn) ─────────────────────────────────────────────────────────
def get_mouth_ratio(landmarks):
    vertical   = abs(landmarks[14].y - landmarks[13].y)
    horizontal = abs(landmarks[308].x - landmarks[78].x)
    return (vertical / horizontal) if horizontal != 0 else 0

# ── Main ──────────────────────────────────────────────────────────────────────
def analyze_frame(frame):
    rgb      = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result   = landmarker.detect(mp_image)

    face_data     = []
    engaged_count = 0
    total_faces   = len(result.face_landmarks)
    h, w, _       = frame.shape

    for landmarks in result.face_landmarks:

        pitch       = get_head_pitch(landmarks)    # >0.08 = looking down
        yaw         = get_head_yaw(landmarks)      # <0.10 = turned away
        gaze        = get_gaze_ratio(landmarks)    # <0.35 or >0.65 = side glance
        mouth_ratio = get_mouth_ratio(landmarks)   # >0.25 = yawning

        # Dot on forehead
        forehead = landmarks[10]
        dot_px   = (int(forehead.x * w), int(forehead.y * h))

        is_engaged = (
            pitch       < 0.08  and     # KEY FIX: nose not far below ears = head upright
            yaw         > 0.10  and     # not turned sideways
            0.30 < gaze < 0.70  and     # eyes pointing forward
            mouth_ratio < 0.25          # not yawning
        )

        if is_engaged:
            engaged_count += 1

        # Terminal debug — watch these values while testing
        print(f"pitch={pitch:.3f} | yaw={yaw:.3f} | "
              f"gaze={gaze:.2f} | mouth={mouth_ratio:.3f} | "
              f"{'✅ ENGAGED' if is_engaged else '❌ ZONED OUT'}")

        face_data.append({
            "position":    dot_px,
            "engaged":     is_engaged,
            "mouth_ratio": round(mouth_ratio, 3),
            "tilt":        round(pitch, 3)
        })

    score = int((engaged_count / total_faces) * 100) if total_faces > 0 else 0
    return score, total_faces, engaged_count, face_data
