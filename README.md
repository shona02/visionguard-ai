# VisionGuard AI 🛡️

Real-time workplace safety monitoring system using computer vision.

## Tech Stack
- **YOLOv8** — object detection
- **ByteTrack** — person tracking across frames  
- **FastAPI** — backend API with MJPEG streaming
- **React** — live dashboard with alert panels

## Features
- Live video stream with bounding boxes
- Persistent person tracking with IDs
- Safety violation alerts with timers
- REST API with /video, /tracked, /alerts endpoints

## How to Run

### Backend
```bash
cd backend
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm start
```

## Project Structure