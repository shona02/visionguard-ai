# backend/detector.py

from ultralytics import YOLO
import cv2

class SafetyDetector:
    def __init__(self, model_path='../runs/detect/visionguard/weights/best.pt', confidence=0.5):
        # Load the model once when the class is created
        # Loading is expensive — we never want to do it per frame
        self.model = YOLO(model_path)
        self.confidence = confidence

    def detect(self, frame):
        # Run inference on a single frame
        # conf= filters out low confidence detections at the model level
        results = self.model(frame, conf=self.confidence, verbose=False)

        detections = []

        for box in results[0].boxes:
            detection = {
                'class_name': self.model.names[int(box.cls)],
                'confidence': round(float(box.conf), 2),
                'bbox': [round(x) for x in box.xyxy[0].tolist()]
            }
            detections.append(detection)

        return detections

    def annotate(self, frame):
        # Returns the frame with boxes drawn on it
        # This is what we'll send as MJPEG
        results = self.model(frame, conf=self.confidence, verbose=False)
        return results[0].plot()