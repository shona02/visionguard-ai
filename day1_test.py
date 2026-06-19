# day1_test.py

from ultralytics import YOLO   # The entire YOLOv8 library in one import
import cv2                      # OpenCV for image I/O

# Load a pretrained model. 'yolov8n' = nano (smallest/fastest).
# On first run, this downloads ~6MB weights from the internet.
# n=nano, s=small, m=medium, l=large, x=xlarge — trade speed for accuracy
model = YOLO('yolov8n.pt')

# Run inference on a test image
# You can pass: a file path, a URL, a numpy array, or a cv2 frame
results = model('https://ultralytics.com/images/bus.jpg')

# results is a list — one element per image you passed in
result = results[0]

# Print what was detected
for box in result.boxes:
    class_id = int(box.cls)                    # integer class index
    class_name = model.names[class_id]         # human-readable name
    confidence = float(box.conf)               # 0.0 to 1.0
    x1, y1, x2, y2 = box.xyxy[0].tolist()    # top-left, bottom-right corners

    print(f"{class_name}: {confidence:.2f} at [{x1:.0f},{y1:.0f},{x2:.0f},{y2:.0f}]")

# Save the annotated image (boxes already drawn by ultralytics)
result.save('output.jpg')
print("Saved output.jpg — open it to see the boxes!")