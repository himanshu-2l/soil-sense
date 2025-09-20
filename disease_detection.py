#!/usr/bin/env python3
"""
Plant Disease Detection Module
Uses computer vision and AI to detect plant diseases from camera images
"""

import cv2
import numpy as np
from PIL import Image
import io
import base64
import json
from datetime import datetime
import os

class PlantDiseaseDetector:
    def __init__(self):
        """Initialize the disease detection system"""
        self.disease_classes = {
            0: "Healthy",
            1: "Bacterial Blight",
            2: "Fungal Infection",
            3: "Viral Disease",
            4: "Nutrient Deficiency",
            5: "Pest Damage",
            6: "Leaf Spot",
            7: "Powdery Mildew",
            8: "Rust",
            9: "Anthracnose"
        }
        
        self.treatment_recommendations = {
            "Healthy": "🌱 Plant is healthy! Continue current care routine.",
            "Bacterial Blight": "🦠 Remove affected leaves, apply copper-based fungicide, improve air circulation.",
            "Fungal Infection": "🍄 Apply fungicide, reduce humidity, ensure proper drainage.",
            "Viral Disease": "🦠 Remove infected plants, control insect vectors, use virus-free seeds.",
            "Nutrient Deficiency": "🌿 Apply balanced fertilizer, check soil pH, add organic matter.",
            "Pest Damage": "🐛 Use organic pesticides, introduce beneficial insects, remove affected areas.",
            "Leaf Spot": "🔍 Remove infected leaves, apply fungicide, improve air circulation.",
            "Powdery Mildew": "☁️ Apply sulfur-based fungicide, reduce humidity, increase air flow.",
            "Rust": "🦠 Remove affected parts, apply fungicide, improve plant spacing.",
            "Anthracnose": "🍂 Remove infected plant material, apply fungicide, improve drainage."
        }
        
        self.severity_levels = {
            "Low": "🟢 Minor issue - Monitor and treat preventively",
            "Medium": "🟡 Moderate issue - Requires treatment within a week",
            "High": "🔴 Severe issue - Immediate treatment required"
        }

    def preprocess_image(self, image_data):
        """Preprocess image for disease detection"""
        try:
            # Convert base64 to image
            if isinstance(image_data, str):
                image_data = base64.b64decode(image_data.split(',')[1])
            
            # Convert to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to standard size
            image = image.resize((224, 224))
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Normalize pixel values
            img_array = img_array.astype(np.float32) / 255.0
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None

    def detect_disease_simple(self, image_data):
        """Simple rule-based disease detection (for demo purposes)"""
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_data)
            if processed_image is None:
                return None
            
            # Convert to OpenCV format for analysis
            img = processed_image[0] * 255
            img = img.astype(np.uint8)
            img_cv = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            
            # Convert to HSV for better color analysis
            hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
            
            # Analyze color patterns
            results = self.analyze_color_patterns(hsv, img_cv)
            
            return results
            
        except Exception as e:
            print(f"Error in disease detection: {e}")
            return None

    def analyze_color_patterns(self, hsv, img):
        """Analyze color patterns to detect diseases"""
        # Define color ranges for different disease symptoms
        # Yellow/brown spots (common in many diseases)
        yellow_lower = np.array([20, 100, 100])
        yellow_upper = np.array([30, 255, 255])
        yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
        yellow_pixels = cv2.countNonZero(yellow_mask)
        
        # Brown/black spots
        brown_lower = np.array([0, 50, 20])
        brown_upper = np.array([20, 255, 200])
        brown_mask = cv2.inRange(hsv, brown_lower, brown_upper)
        brown_pixels = cv2.countNonZero(brown_mask)
        
        # White/powdery areas (powdery mildew)
        white_lower = np.array([0, 0, 200])
        white_upper = np.array([180, 30, 255])
        white_mask = cv2.inRange(hsv, white_lower, white_upper)
        white_pixels = cv2.countNonZero(white_mask)
        
        # Red/orange areas (rust)
        red_lower = np.array([0, 50, 50])
        red_upper = np.array([10, 255, 255])
        red_mask = cv2.inRange(hsv, red_lower, red_upper)
        red_pixels = cv2.countNonZero(red_mask)
        
        # Calculate percentages
        total_pixels = img.shape[0] * img.shape[1]
        yellow_percent = (yellow_pixels / total_pixels) * 100
        brown_percent = (brown_pixels / total_pixels) * 100
        white_percent = (white_pixels / total_pixels) * 100
        red_percent = (red_pixels / total_pixels) * 100
        
        # Determine disease based on patterns
        disease = "Healthy"
        confidence = 0.0
        severity = "Low"
        
        if yellow_percent > 5 or brown_percent > 3:
            if white_percent > 2:
                disease = "Powdery Mildew"
                confidence = min(0.9, (white_percent + yellow_percent) / 10)
            elif red_percent > 2:
                disease = "Rust"
                confidence = min(0.9, (red_percent + yellow_percent) / 10)
            elif brown_percent > yellow_percent:
                disease = "Leaf Spot"
                confidence = min(0.9, brown_percent / 5)
            else:
                disease = "Fungal Infection"
                confidence = min(0.9, (yellow_percent + brown_percent) / 8)
            
            # Determine severity
            if confidence > 0.7:
                severity = "High"
            elif confidence > 0.4:
                severity = "Medium"
            else:
                severity = "Low"
                
        elif white_percent > 3:
            disease = "Powdery Mildew"
            confidence = min(0.8, white_percent / 5)
            severity = "Medium" if confidence > 0.5 else "Low"
            
        elif red_percent > 2:
            disease = "Rust"
            confidence = min(0.8, red_percent / 4)
            severity = "Medium" if confidence > 0.5 else "Low"
        
        return {
            "disease": disease,
            "confidence": round(confidence, 2),
            "severity": severity,
            "symptoms": {
                "yellow_spots": round(yellow_percent, 2),
                "brown_spots": round(brown_percent, 2),
                "white_powder": round(white_percent, 2),
                "red_rust": round(red_percent, 2)
            },
            "treatment": self.treatment_recommendations.get(disease, "Consult agricultural expert"),
            "severity_description": self.severity_levels.get(severity, "Unknown severity")
        }

    def detect_disease_advanced(self, image_data):
        """Advanced disease detection using pre-trained model (placeholder)"""
        # This would use a real trained model in production
        # For now, we'll use the simple method
        return self.detect_disease_simple(image_data)

    def get_disease_history(self):
        """Get disease detection history"""
        try:
            if os.path.exists('disease_history.json'):
                with open('disease_history.json', 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading disease history: {e}")
            return []

    def save_disease_detection(self, detection_result):
        """Save disease detection result to history"""
        try:
            history = self.get_disease_history()
            
            detection_record = {
                "timestamp": datetime.now().isoformat(),
                "disease": detection_result["disease"],
                "confidence": detection_result["confidence"],
                "severity": detection_result["severity"],
                "treatment": detection_result["treatment"]
            }
            
            history.append(detection_record)
            
            # Keep only last 50 records
            if len(history) > 50:
                history = history[-50:]
            
            with open('disease_history.json', 'w') as f:
                json.dump(history, f, indent=2)
                
        except Exception as e:
            print(f"Error saving disease detection: {e}")

# Global detector instance
disease_detector = PlantDiseaseDetector()
