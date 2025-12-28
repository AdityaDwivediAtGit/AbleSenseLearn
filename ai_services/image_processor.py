import cv2
import numpy as np
from PIL import Image
import io
import base64
from typing import Optional, Dict, List, Tuple
import torch
from torchvision import models, transforms
from torchvision.models import ResNet50_Weights
import json

class ImageProcessor:
    """AI-powered image processing for accessibility"""
    
    def __init__(self, use_deep_learning=True):
        """
        Initialize image processor
        
        Args:
            use_deep_learning: Whether to use deep learning models
        """
        self.use_deep_learning = use_deep_learning
        
        # Initialize models if using deep learning
        if self.use_deep_learning:
            self._init_models()
        
        # Image transformation pipeline
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        # Common object labels (for basic detection)
        self.common_objects = {
            'person', 'bicycle', 'car', 'motorcycle', 'bus', 'truck',
            'traffic light', 'stop sign', 'parking meter', 'bench',
            'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant',
            'bear', 'zebra', 'giraffe',
            'backpack', 'umbrella', 'handbag', 'tie', 'suitcase',
            'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
            'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
            'tennis racket',
            'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon',
            'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli',
            'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
            'couch', 'potted plant', 'bed', 'dining table', 'toilet',
            'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
            'microwave', 'oven', 'toaster', 'sink', 'refrigerator',
            'book', 'clock', 'vase', 'scissors', 'teddy bear',
            'hair drier', 'toothbrush'
        }
        
        # Color names for color detection
        self.color_names = {
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'orange': (255, 165, 0),
            'purple': (128, 0, 128),
            'pink': (255, 192, 203),
            'brown': (165, 42, 42),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'gray': (128, 128, 128)
        }
    
    def _init_models(self):
        """Initialize deep learning models"""
        try:
            # Load pre-trained models
            self.resnet = models.resnet50(weights=ResNet50_Weights.DEFAULT)
            self.resnet.eval()
            
            # Load class labels
            import requests
            response = requests.get(
                "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
            )
            self.imagenet_labels = response.json() if response.status_code == 200 else []
            
            print("Deep learning models loaded successfully")
        except Exception as e:
            print(f"Failed to load deep learning models: {e}")
            self.use_deep_learning = False
    
    def generate_alt_text(self, image_file, detailed: bool = False) -> str:
        """
        Generate alt-text description for an image
        
        Args:
            image_file: File-like object or path to image
            detailed: Whether to generate detailed description
            
        Returns:
            Alt-text description
        """
        try:
            # Load image
            if hasattr(image_file, 'read'):
                image = Image.open(image_file)
            else:
                image = Image.open(image_file)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Get basic image info
            width, height = image.size
            aspect_ratio = width / height if height > 0 else 1
            
            # Analyze image
            if self.use_deep_learning:
                description = self._analyze_with_dl(image, detailed)
            else:
                description = self._analyze_without_dl(image)
            
            # Add basic info
            shape_desc = self._describe_shape(width, height)
            
            if detailed:
                # Get colors
                colors = self._detect_colors(image)
                color_desc = self._describe_colors(colors)
                
                # Get texture/pattern info
                texture = self._analyze_texture(image)
                
                alt_text = f"{shape_desc} {color_desc} {texture} {description}"
            else:
                alt_text = f"{shape_desc} showing {description}"
            
            # Clean up description
            alt_text = alt_text.strip()
            alt_text = alt_text[0].upper() + alt_text[1:] if alt_text else ""
            
            return alt_text
            
        except Exception as e:
            print(f"Error generating alt-text: {e}")
            return "An image that could not be analyzed"
    
    def _analyze_with_dl(self, image: Image.Image, detailed: bool = False) -> str:
        """Analyze image using deep learning"""
        try:
            # Prepare image for model
            img_tensor = self.transform(image).unsqueeze(0)
            
            # Get predictions
            with torch.no_grad():
                outputs = self.resnet(img_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                top_prob, top_cat = torch.topk(probabilities, 3)
            
            # Get labels
            labels = []
            for i in range(3):
                if top_cat[i].item() < len(self.imagenet_labels):
                    label = self.imagenet_labels[top_cat[i].item()]
                    prob = top_prob[i].item()
                    
                    # Filter out abstract concepts for alt-text
                    if not any(word in label.lower() for word in ['abstract', 'pattern', 'texture', 'background']):
                        labels.append((label, prob))
            
            # Build description
            if labels:
                primary_label = labels[0][0].replace('_', ' ')
                
                if detailed and len(labels) > 1:
                    secondary_labels = [l[0].replace('_', ' ') for l in labels[1:3]]
                    return f"a {primary_label}, possibly also containing {', '.join(secondary_labels[:-1])} and {secondary_labels[-1]}"
                else:
                    return f"a {primary_label}"
            else:
                return "an image"
                
        except Exception as e:
            print(f"Deep learning analysis failed: {e}")
            return self._analyze_without_dl(image)
    
    def _analyze_without_dl(self, image: Image.Image) -> str:
        """Analyze image without deep learning (rule-based)"""
        # Convert to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Simple analysis
        is_photograph = self._is_likely_photograph(cv_image)
        has_faces = self._detect_faces(cv_image)
        is_text_dense = self._has_dense_text(cv_image)
        
        if has_faces:
            num_faces = len(has_faces)
            if num_faces == 1:
                return "a person"
            else:
                return f"{num_faces} people"
        elif is_text_dense:
            return "text or a document"
        elif is_photograph:
            return "a photograph"
        else:
            return "an image"
    
    def _describe_shape(self, width: int, height: int) -> str:
        """Describe image shape/orientation"""
        if width > height * 1.5:
            return "A wide"
        elif height > width * 1.5:
            return "A tall"
        else:
            return "A"
    
    def _detect_colors(self, image: Image.Image, n_colors: int = 3) -> List[Tuple[str, float]]:
        """Detect dominant colors in image"""
        try:
            # Resize for faster processing
            small_image = image.resize((100, 100))
            pixels = np.array(small_image).reshape(-1, 3)
            
            # Use k-means to find dominant colors
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            # Get colors and proportions
            colors = []
            labels = kmeans.labels_
            centers = kmeans.cluster_centers_.astype(int)
            
            for i in range(n_colors):
                proportion = np.sum(labels == i) / len(labels)
                if proportion > 0.05:  # Ignore very small clusters
                    # Find closest named color
                    color_rgb = tuple(centers[i])
                    color_name = self._get_closest_color_name(color_rgb)
                    colors.append((color_name, proportion))
            
            # Sort by proportion
            colors.sort(key=lambda x: x[1], reverse=True)
            return colors[:3]  # Return top 3
            
        except Exception:
            return []
    
    def _get_closest_color_name(self, rgb: Tuple[int, int, int]) -> str:
        """Get closest named color for RGB value"""
        min_distance = float('inf')
        closest_color = "colorful"
        
        for name, color_rgb in self.color_names.items():
            distance = sum((c1 - c2) ** 2 for c1, c2 in zip(rgb, color_rgb))
            if distance < min_distance:
                min_distance = distance
                closest_color = name
        
        return closest_color
    
    def _describe_colors(self, colors: List[Tuple[str, float]]) -> str:
        """Describe color composition"""
        if not colors:
            return ""
        
        if len(colors) == 1:
            return f"{colors[0][0]}"
        elif len(colors) == 2:
            return f"{colors[0][0]} and {colors[1][0]}"
        else:
            return f"{colors[0][0]}, {colors[1][0]}, and {colors[2][0]}"
    
    def _analyze_texture(self, image: Image.Image) -> str:
        """Analyze texture/pattern in image"""
        try:
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
            
            # Calculate texture metrics
            laplacian_var = cv2.Laplacian(cv_image, cv2.CV_64F).var()
            
            if laplacian_var < 100:
                return "blurry or smooth"
            elif laplacian_var > 1000:
                return "sharp and detailed"
            else:
                return ""
                
        except Exception:
            return ""
    
    def _is_likely_photograph(self, cv_image) -> bool:
        """Check if image is likely a photograph"""
        # Simple heuristic based on color variance
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        saturation = hsv[:, :, 1]
        
        return np.mean(saturation) > 30  # Photographs usually have decent saturation
    
    def _detect_faces(self, cv_image):
        """Simple face detection"""
        try:
            # Load Haar cascade
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            return faces
        except:
            return []
    
    def _has_dense_text(self, cv_image) -> bool:
        """Check if image contains dense text"""
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
            
            # Calculate text density
            text_pixels = np.sum(thresh > 0)
            total_pixels = thresh.size
            
            return text_pixels / total_pixels > 0.1  # More than 10% text
            
        except:
            return False
    
    def generate_tactile_diagram(self, image_file, output_format: str = "svg") -> Dict:
        """
        Generate data for tactile diagrams
        
        Args:
            image_file: Input image
            output_format: Output format ('svg', 'braille', '3d')
            
        Returns:
            Dictionary with diagram data
        """
        try:
            # Load image
            if hasattr(image_file, 'read'):
                image = Image.open(image_file)
            else:
                image = Image.open(image_file)
            
            # Convert to grayscale
            gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
            
            # Edge detection for outline
            edges = cv2.Canny(gray, 50, 150)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Simplify contours for tactile representation
            simplified_contours = []
            for contour in contours:
                if len(contour) > 10:  # Only keep significant contours
                    epsilon = 0.01 * cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, epsilon, True)
                    simplified_contours.append(approx.tolist())
            
            # Create description
            description = self._describe_for_tactile(gray, simplified_contours)
            
            return {
                'format': output_format,
                'contours': simplified_contours,
                'description': description,
                'image_size': image.size,
                'num_contours': len(simplified_contours)
            }
            
        except Exception as e:
            print(f"Error generating tactile diagram: {e}")
            return {
                'format': output_format,
                'contours': [],
                'description': 'Unable to generate tactile diagram',
                'error': str(e)
            }
    
    def _describe_for_tactile(self, gray_image, contours) -> str:
        """Generate description for tactile diagram"""
        if not contours:
            return "A simple image with no distinct shapes"
        
        # Analyze shape complexity
        total_points = sum(len(c) for c in contours)
        
        if len(contours) == 1:
            shape_desc = "a single shape"
        elif len(contours) <= 3:
            shape_desc = f"{len(contours)} main shapes"
        else:
            shape_desc = f"multiple ({len(contours)}) shapes"
        
        # Analyze size distribution
        if total_points < 50:
            complexity = "simple"
        elif total_points < 200:
            complexity = "moderately detailed"
        else:
            complexity = "detailed"
        
        return f"A {complexity} {shape_desc}"
    
    def extract_text_from_image(self, image_file) -> Dict:
        """
        Extract text from image using OCR
        
        Args:
            image_file: Input image
            
        Returns:
            Dictionary with extracted text and confidence
        """
        try:
            import pytesseract
            
            # Load image
            if hasattr(image_file, 'read'):
                image = Image.open(image_file)
            else:
                image = Image.open(image_file)
            
            # Convert to grayscale
            gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
            
            # Apply preprocessing
            processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            
            # Extract text
            text = pytesseract.image_to_string(processed)
            data = pytesseract.image_to_data(processed, output_type=pytesseract.Output.DICT)
            
            # Calculate average confidence
            confidences = [int(c) for c in data['conf'] if int(c) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'text': text.strip(),
                'confidence': avg_confidence,
                'words': len(text.split()),
                'lines': len(text.strip().split('\n'))
            }
            
        except ImportError:
            return {
                'text': '',
                'confidence': 0,
                'error': 'pytesseract not installed. Install with: pip install pytesseract'
            }
        except Exception as e:
            return {
                'text': '',
                'confidence': 0,
                'error': str(e)
            }