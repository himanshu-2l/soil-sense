#!/usr/bin/env python3
"""
Test script for Plant Disease Detection feature
"""

import requests
import base64
import json
from PIL import Image
import io
import numpy as np

def create_test_image():
    """Create a test image with simulated disease symptoms"""
    # Create a simple test image with colored spots
    img = Image.new('RGB', (224, 224), color='green')
    
    # Add some yellow/brown spots to simulate disease
    pixels = np.array(img)
    
    # Add yellow spots (simulating fungal infection)
    for i in range(50, 100):
        for j in range(50, 100):
            if (i-75)**2 + (j-75)**2 < 25**2:  # Circle
                pixels[i, j] = [255, 255, 0]  # Yellow
    
    # Add brown spots
    for i in range(120, 170):
        for j in range(120, 170):
            if (i-145)**2 + (j-145)**2 < 20**2:  # Circle
                pixels[i, j] = [139, 69, 19]  # Brown
    
    # Convert back to PIL Image
    test_img = Image.fromarray(pixels)
    
    # Convert to base64
    buffer = io.BytesIO()
    test_img.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/jpeg;base64,{img_str}"

def test_disease_detection():
    """Test the disease detection API"""
    print("🌱 Testing Plant Disease Detection...")
    
    # Create test image
    test_image = create_test_image()
    
    # Test API endpoint
    try:
        response = requests.post(
            'http://localhost:5000/api/disease-detection',
            json={'image': test_image},
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Disease detection successful!")
            print(f"   Disease: {result['detection']['disease']}")
            print(f"   Confidence: {result['detection']['confidence']:.2f}")
            print(f"   Severity: {result['detection']['severity']}")
            print(f"   Treatment: {result['detection']['treatment']}")
            print(f"   Symptoms: {result['detection']['symptoms']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing disease detection: {e}")

def test_disease_history():
    """Test disease history endpoint"""
    print("\n📊 Testing Disease History...")
    
    try:
        response = requests.get('http://localhost:5000/api/disease-history')
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Disease history retrieved!")
            print(f"   Total detections: {result['total_detections']}")
            if result['history']:
                print("   Recent detections:")
                for detection in result['history'][-3:]:  # Show last 3
                    print(f"     - {detection['disease']} ({detection['confidence']:.2f}) - {detection['timestamp']}")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing disease history: {e}")

def main():
    """Main test function"""
    print("🌱 Plant Disease Detection - Test Suite")
    print("=" * 50)
    
    # Test disease detection
    test_disease_detection()
    
    # Test disease history
    test_disease_history()
    
    print("\n🎉 Disease detection tests completed!")
    print("📱 Open browser: http://localhost:5000")
    print("📷 Try the camera feature in the dashboard!")

if __name__ == "__main__":
    main()
