from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json
from datetime import datetime
import sqlite3
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from disease_detection import disease_detector

app = Flask(__name__)
CORS(app)

# Initialize database
def init_db():
    conn = sqlite3.connect('farm_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            soil_moisture INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Crop recommendation model (simplified)
def get_crop_recommendation(temperature, humidity, soil_moisture):
    """AI-powered crop recommendation based on environmental conditions"""
    # Simple rule-based recommendation (can be replaced with ML model)
    if soil_moisture < 30:
        return "🌾 Wheat, Barley - Drought resistant crops recommended for low moisture conditions"
    elif soil_moisture > 70:
        return "🌾 Rice, Sugarcane - Water-loving crops ideal for high moisture soil"
    elif 20 <= temperature <= 30 and 40 <= humidity <= 60:
        return "🍅 Tomatoes, Peppers, Cucumbers - Perfect conditions for vegetable cultivation"
    elif temperature > 35:
        return "🌾 Millet, Sorghum - Heat tolerant crops suitable for high temperature"
    elif temperature < 15:
        return "🥬 Spinach, Lettuce, Cabbage - Cool weather crops for low temperature"
    else:
        return "🥕 Mixed vegetables, Legumes - General crops suitable for current conditions"

# Weather API integration
def get_weather_data():
    """Fetch real-time weather data for Chhattisgarh"""
    # Using OpenWeatherMap API (free tier)
    api_key = "YOUR_API_KEY"  # Get from openweathermap.org
    city = "Raipur"  # Chhattisgarh capital
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
            'pressure': data['main']['pressure']
        }
    except Exception as e:
        print(f"Weather API error: {e}")
        return {
            'temperature': 25.0,
            'humidity': 60.0,
            'description': 'Weather data unavailable',
            'wind_speed': 5.0,
            'pressure': 1013.0
        }

# Get farming advice based on conditions
def get_farming_advice(temperature, humidity, soil_moisture, weather_data):
    """Provide farming advice based on current conditions"""
    advice = []
    
    if soil_moisture < 30:
        advice.append("💧 Soil is dry - Consider irrigation")
    elif soil_moisture > 80:
        advice.append("⚠️ Soil is too wet - Check drainage")
    
    if temperature > 35:
        advice.append("🌡️ High temperature - Water plants in early morning or evening")
    elif temperature < 10:
        advice.append("❄️ Low temperature - Protect sensitive crops")
    
    if humidity > 80:
        advice.append("🌫️ High humidity - Watch for fungal diseases")
    elif humidity < 30:
        advice.append("🏜️ Low humidity - Increase watering frequency")
    
    if weather_data and 'rain' in weather_data.get('description', '').lower():
        advice.append("🌧️ Rain expected - Reduce irrigation")
    
    return advice if advice else ["✅ Conditions are optimal for farming"]

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    """Receive sensor data from ESP32"""
    try:
        data = request.json
        conn = sqlite3.connect('farm_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sensor_data (temperature, humidity, soil_moisture)
            VALUES (?, ?, ?)
        ''', (data['temperature'], data['humidity'], data['soil_moisture']))
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Data received successfully'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/dashboard-data')
def get_dashboard_data():
    """Get all data for dashboard display"""
    conn = sqlite3.connect('farm_data.db')
    cursor = conn.cursor()
    
    # Get latest sensor data
    cursor.execute('''
        SELECT temperature, humidity, soil_moisture, timestamp
        FROM sensor_data
        ORDER BY timestamp DESC LIMIT 1
    ''')
    latest_data = cursor.fetchone()
    
    # Get weather data
    weather = get_weather_data()
    
    # Get crop recommendation and farming advice
    if latest_data:
        recommendation = get_crop_recommendation(
            latest_data[0], latest_data[1], latest_data[2]
        )
        advice = get_farming_advice(
            latest_data[0], latest_data[1], latest_data[2], weather
        )
    else:
        recommendation = "No sensor data available - Connect your ESP32 device"
        advice = ["Connect your ESP32 device to start monitoring"]
    
    # Get historical data for trends (last 24 hours)
    cursor.execute('''
        SELECT temperature, humidity, soil_moisture, timestamp
        FROM sensor_data
        WHERE timestamp > datetime('now', '-1 day')
        ORDER BY timestamp ASC
    ''')
    historical_data = cursor.fetchall()
    
    conn.close()
    
    return jsonify({
        'sensor_data': {
            'temperature': latest_data[0] if latest_data else None,
            'humidity': latest_data[1] if latest_data else None,
            'soil_moisture': latest_data[2] if latest_data else None,
            'timestamp': latest_data[3] if latest_data else None
        },
        'weather': weather,
        'recommendation': recommendation,
        'advice': advice,
        'historical_data': historical_data
    })

@app.route('/api/disease-detection', methods=['POST'])
def detect_plant_disease():
    """Detect plant disease from uploaded image"""
    try:
        data = request.json
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Detect disease
        detection_result = disease_detector.detect_disease_simple(image_data)
        
        if detection_result:
            # Save to history
            disease_detector.save_disease_detection(detection_result)
            
            return jsonify({
                'status': 'success',
                'detection': detection_result,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Failed to process image'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/disease-history')
def get_disease_history():
    """Get disease detection history"""
    try:
        history = disease_detector.get_disease_history()
        return jsonify({
            'status': 'success',
            'history': history,
            'total_detections': len(history)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    print("🌱 Starting Smart Soil Monitor Server...")
    init_db()
    print("📊 Database initialized")
    print("🌐 Server starting on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
