# day1_webcam.py

from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)   # 0 = default webcam

while True:
    ret, frame = cap.read()       # frame is a numpy array: (H, W, 3)
    if not ret:
        break

    # Run model on numpy array directly — no saving to disk
    results = model(frame, verbose=False)   # verbose=False silences per-frame logs

    # result.plot() draws boxes + labels onto a copy of the frame
    annotated = results[0].plot()

    cv2.imshow('VisionGuard AI - Day 1', annotated)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()