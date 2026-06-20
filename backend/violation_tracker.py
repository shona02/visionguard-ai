# backend/violation_tracker.py

import time

class ViolationTracker:
    def __init__(self, alert_seconds=5):
        # How many seconds without a hardhat before we alert
        self.alert_seconds = alert_seconds

        # Dict to track when each person ID first violated
        # { track_id: timestamp_of_first_violation }
        self.violation_start = {}

        # Active alerts right now
        self.active_alerts = []

    def update(self, tracked_objects):
        # Get all person IDs currently visible
        current_ids = set()

        for obj in tracked_objects:
            if obj['class_name'] == 'person':
                current_ids.add(obj['track_id'])

        # Check each visible person for hardhat
        person_ids_with_hardhat = set()

        for obj in tracked_objects:
            if obj['class_name'] == 'hardhat':
                # Find the nearest person to this hardhat
                # Simple approach: any person in the same region
                # We'll improve this in Day 4
                pass

        # For now: flag ALL visible persons as potential violations
        # (since our model is yolov8n trained on COCO which has no hardhat class)
        # On Day 4 we fine-tune on safety dataset with hardhat/no-hardhat classes
        self.active_alerts = []

        for track_id in current_ids:
            if track_id not in self.violation_start:
                # First time seeing this person without hardhat
                self.violation_start[track_id] = time.time()

            elapsed = time.time() - self.violation_start[track_id]

            if elapsed >= self.alert_seconds:
                self.active_alerts.append({
                    'track_id': track_id,
                    'violation': 'Person detected — safety check required',
                    'duration_seconds': round(elapsed, 1)
                })

        # Clean up IDs that left the frame
        ids_to_remove = set(self.violation_start.keys()) - current_ids
        for track_id in ids_to_remove:
            del self.violation_start[track_id]

        return self.active_alerts