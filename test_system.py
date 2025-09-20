#!/usr/bin/env python3
"""
Test script for Smart Soil Monitor system
This script tests the Flask API endpoints and generates demo data
"""

import requests
import json
import time
import random
from datetime import datetime

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Smart Soil Monitor API...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test dashboard data endpoint
    try:
        response = requests.get(f"{base_url}/api/dashboard-data", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard data endpoint working")
            data = response.json()
            print(f"   Sensor data: {data.get('sensor_data')}")
            print(f"   Weather: {data.get('weather')}")
            print(f"   Recommendation: {data.get('recommendation')}")
        else:
            print(f"❌ Dashboard data failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard data error: {e}")
    
    return True

def generate_demo_data():
    """Generate demo sensor data for testing"""
    print("\n📊 Generating demo sensor data...")
    
    base_url = "http://localhost:5000"
    
    # Generate 10 data points
    for i in range(10):
        # Simulate realistic sensor data
        temperature = round(random.uniform(20, 35), 1)
        humidity = round(random.uniform(40, 80), 1)
        soil_moisture = random.randint(30, 70)
        
        data = {
            "temperature": temperature,
            "humidity": humidity,
            "soil_moisture": soil_moisture,
            "timestamp": int(time.time() * 1000)
        }
        
        try:
            response = requests.post(
                f"{base_url}/api/sensor-data",
                json=data,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ Data point {i+1}: Temp={temperature}°C, Humidity={humidity}%, Soil={soil_moisture}%")
            else:
                print(f"❌ Data point {i+1} failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Data point {i+1} error: {e}")
        
        time.sleep(1)  # Wait 1 second between data points

def main():
    """Main test function"""
    print("🌱 Smart Soil Monitor - System Test")
    print("=" * 50)
    
    # Test if server is running
    if not test_api_endpoints():
        print("\n❌ Server not running. Please start with: python app.py")
        return
    
    # Generate demo data
    generate_demo_data()
    
    print("\n🎉 Test completed!")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🔍 Check the dashboard for real-time data visualization")

if __name__ == "__main__":
    main()
