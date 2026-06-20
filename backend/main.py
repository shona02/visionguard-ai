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

# Create tracker and violation tracker ONCE at startup
tracker = VisionTracker()
violation_tracker = ViolationTracker(alert_seconds=5)

def generate_frames():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Get tracked objects with IDs
        tracked_objects = tracker.track(frame)

        # Update violation timers
        violation_tracker.update(tracked_objects)

        # Get annotated frame with track IDs drawn
        annotated = tracker.annotate(frame)

        # Encode to JPEG
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
    # Returns currently tracked objects with their IDs
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return {"tracked": []}
    return {"tracked": tracker.track(frame)}

@app.get("/alerts")
def get_alerts():
    # Returns active safety violations
    # React frontend polls this every second to show alerts
    return {"alerts": violation_tracker.active_alerts}