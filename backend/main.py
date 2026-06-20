# backend/main.py

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import sys
import os

# This lets Python find detector.py in the same folder
sys.path.append(os.path.dirname(__file__))
from detector import SafetyDetector

# Create the FastAPI app
app = FastAPI(title="VisionGuard AI")

# Allow React frontend to talk to this backend
# Without this, the browser blocks cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create detector ONCE when server starts
# Not on every request — that would reload YOLO every time
detector = SafetyDetector()

def generate_frames():
    # Open webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Get annotated frame from detector
        annotated = detector.annotate(frame)

        # Convert frame to JPEG bytes
        # imencode returns (success, jpeg_bytes)
        _, buffer = cv2.imencode('.jpg', annotated)

        # Convert to bytes
        frame_bytes = buffer.tobytes()

        # Yield one JPEG frame in MJPEG format
        # This specific format is what browsers expect
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + frame_bytes +
            b'\r\n'
        )

    cap.release()

@app.get("/")
def root():
    # Health check — visit this to confirm server is running
    return {"status": "VisionGuard AI is running"}

@app.get("/video")
def video_feed():
    # StreamingResponse keeps the connection open and streams frames
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/detections")
def get_detections():
    # Returns current detections as JSON
    # React frontend will call this to show alerts
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        return {"detections": []}

    return {"detections": detector.detect(frame)}