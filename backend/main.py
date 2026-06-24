# backend/main.py

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import sys
import os

sys.path.append(os.path.dirname(__file__))
from tracker import VisionTracker
from violation_tracker import ViolationTracker

app = FastAPI(title="VisionGuard AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

tracker = VisionTracker()
violation_tracker = ViolationTracker(alert_seconds=5)

# Store latest data globally
latest_tracked = []
latest_alerts = []

def generate_frames():
    global latest_tracked, latest_alerts
    cap = cv2.VideoCapture(0)
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame_count += 1

        # Run YOLO every 3rd frame only
        if frame_count % 5 == 0:
    # Resize to smaller image for faster inference
            small = cv2.resize(frame, (320, 240))
            latest_tracked = tracker.track(small)
            violation_tracker.update(latest_tracked)
            latest_alerts = violation_tracker.active_alerts
            annotated = tracker.annotate(small)
            # Resize back to display size
            annotated = cv2.resize(annotated, (640, 480))
        else:
            annotated = frame

        _, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame_bytes +
            b'\r\n'
        )

    cap.release()

@app.get("/")
def root():
    return {"status": "VisionGuard AI is running"}

@app.get("/video")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/tracked")
def get_tracked():
    return {"tracked": latest_tracked}

@app.get("/alerts")
def get_alerts():
    return {"alerts": latest_alerts}