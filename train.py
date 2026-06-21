# train.py
from ultralytics import YOLO

# Load pretrained yolov8n — we fine-tune from here
# This is transfer learning — model already knows edges, shapes, objects
# We just teach it the new 'head' class on top
model = YOLO('yolov8n.pt')

# Train on our dataset
results = model.train(
    data='Hard-Hat-Workers-14/data.yaml',  # dataset config
    epochs=20,          # how many times to go through all images
    imgsz=640,          # image size — same as inference
    batch=8,            # images per training step — lower if RAM issues
    name='visionguard', # folder name for saved results
    patience=5,         # stop early if no improvement for 5 epochs
    device='cpu'        # use CPU — change to 0 if you have NVIDIA GPU
)

print("Training complete!")
print(f"Best model saved to: runs/detect/visionguard/weights/best.pt")