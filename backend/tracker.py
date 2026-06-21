# backend/tracker.py

from ultralytics import YOLO
import cv2

class VisionTracker:
    def __init__(self, model_path='../runs/detect/visionguard/weights/best.pt', confidence=0.5):
        # Same model as detector but we use track() instead of __call__()
        self.model = YOLO(model_path)
        self.confidence = confidence

    def track(self, frame):
        # .track() runs YOLO + ByteTrack in one call
        # persist=True tells ByteTrack to remember IDs across frames
        results = self.model.track(
            frame,
            conf=self.confidence,
            persist=True,
            verbose=False,
            tracker="bytetrack.yaml"
        )

        tracked_objects = []

        # No detections this frame
        if results[0].boxes.id is None:
            return tracked_objects

        for box in results[0].boxes:
            # box.id is the persistent track ID assigned by ByteTrack
            # It stays the same across frames for the same person
            track_id = int(box.id)
            class_name = self.model.names[int(box.cls)]
            confidence = round(float(box.conf), 2)
            bbox = [round(x) for x in box.xyxy[0].tolist()]

            tracked_objects.append({
                'track_id': track_id,
                'class_name': class_name,
                'confidence': confidence,
                'bbox': bbox
            })

        return tracked_objects

    def annotate(self, frame):
        # Returns frame with track IDs drawn on boxes
        results = self.model.track(
            frame,
            conf=self.confidence,
            persist=True,
            verbose=False,
            tracker="bytetrack.yaml"
        )
        return results[0].plot()