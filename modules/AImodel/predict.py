import sys
import os
import cv2
import torch

# Add the network directory to the system path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'network'))

from network.footandball import build_footandball_detector1  # Use the factory function to build the model
from network.utils import draw_detections

# Instantiate the model using the factory function
model = build_footandball_detector1(phase='detect')
model.load_state_dict(torch.load('models\model_20201019_1416_final.pth', map_location=torch.device('cpu')))
model.eval()

# Load the video
video_path = "NB I_ Kecskemét–ZTE 2–1 _ összefoglaló.mp4"
cap = cv2.VideoCapture(video_path)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

# Process each frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame
    input_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    input_frame = torch.from_numpy(input_frame).permute(2, 0, 1).float().unsqueeze(0) / 255.0

    # Perform detection
    with torch.no_grad():
        detections = model(input_frame)

    # Draw detections on the frame
    output_frame = draw_detections(frame, detections)

    # Write the frame to the output video
    out.write(output_frame)

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
