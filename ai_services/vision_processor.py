from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image

class VisionProcessor:
    def __init__(self):
        # Initialize YOLO model (lazily loaded to speed up app start)
        self.model = None
        
    def _load_model(self):
        if self.model is None:
            # Using a small model for speed and low resource usage
            self.model = YOLO('yolov8n.pt') 

    def describe_image(self, image_input):
        """
        Analyzes an image and returns a description of objects found.
        image_input: PIL Image or bytes
        """
        self._load_model()
        
        # Convert PIL image to format expected by YOLO if needed
        if isinstance(image_input, Image.Image):
            # Convert to numpy array (RGB to BGR for OpenCV compatibility if needed, but YOLO handles PIL)
            pass

        results = self.model(image_input)
        
        # Parse results
        found_objects = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                found_objects.append(class_name)
        
        if not found_objects:
            return "I couldn't identify any specific objects in this image, but it looks clear."
            
        # Group counts
        counts = {}
        for obj in found_objects:
            counts[obj] = counts.get(obj, 0) + 1
            
        description_parts = []
        for obj, count in counts.items():
            if count == 1:
                description_parts.append(f"a {obj}")
            else:
                description_parts.append(f"{count} {obj}s")
                
        return "I see " + ", ".join(description_parts) + "."
