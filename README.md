# 🌱 Smart Soil Monitor - Agricultural Automation

A comprehensive IoT solution for farmers in Chhattisgarh, featuring real-time soil monitoring, AI-powered crop recommendations, and weather integration.

## 🏆 Competition Features

- **Real-time Sensor Monitoring**: ESP32 + DHT22 + Soil Moisture Sensor
- **AI-Powered Crop Recommendations**: Smart suggestions based on environmental conditions
- **Weather Integration**: Real-time weather data from OpenWeatherMap API
- **Modern Web Dashboard**: Mobile-responsive interface with live data visualization
- **Historical Data Tracking**: 24-hour trend analysis with interactive charts

## 🚀 Quick Start

### Hardware Requirements
- ESP32 Development Board
- DHT22 Temperature & Humidity Sensor
- Soil Moisture Sensor (Analog)
- Jumper Wires
- Breadboard

### Software Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure ESP32**
   - Open `esp32_soil_monitor.ino` in Arduino IDE
   - Install ESP32 board package and required libraries
   - Update WiFi credentials and server URL
   - Upload to ESP32

3. **Get Weather API Key**
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Replace `YOUR_API_KEY` in `app.py`

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access Dashboard**
   - Open browser: `http://localhost:5000`
   - Connect ESP32 to same WiFi network

## 📊 Features

### Real-time Monitoring
- Temperature, Humidity, Soil Moisture sensors
- Live data updates every 30 seconds
- Visual status indicators (Optimal/Warning/Danger)

### AI Crop Recommendations
- Smart crop suggestions based on:
  - Soil moisture levels
  - Temperature conditions
  - Humidity readings
  - Weather patterns

### Plant Disease Detection 🆕
- **Camera Integration**: Use device camera to capture plant images
- **AI-Powered Analysis**: Computer vision algorithms detect diseases
- **Real-time Detection**: Instant analysis of captured images
- **Disease Classification**: Identifies 10+ common plant diseases
- **Treatment Recommendations**: Provides specific treatment advice
- **Severity Assessment**: Low/Medium/High severity levels
- **Detection History**: Tracks all previous detections

### Weather Integration
- Real-time weather data for Raipur, Chhattisgarh
- Temperature, humidity, wind speed, pressure
- Weather-based farming advice

### Historical Analytics
- 24-hour data trends
- Interactive charts
- Data persistence in SQLite database

## 🛠️ Technical Stack

- **Hardware**: ESP32, DHT22, Soil Moisture Sensor
- **Backend**: Python Flask, SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **APIs**: OpenWeatherMap
- **AI/ML**: Computer Vision, OpenCV, scikit-learn
- **Libraries**: numpy, requests, Pillow, opencv-python

## 📱 Mobile Responsive

The dashboard is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes

## 🔧 Configuration

### ESP32 Settings
```cpp
const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";
const char* serverURL = "http://YOUR_IP:5000/api/sensor-data";
```

### Weather API
```python
api_key = "YOUR_API_KEY"  # Get from openweathermap.org
city = "Raipur"  # Chhattisgarh capital
```

## 🏅 Competition Advantages

1. **Complete End-to-End Solution**: Hardware + Software + AI
2. **Real-world Impact**: Directly helps Chhattisgarh farmers
3. **Modern Technology Stack**: Latest IoT and web technologies
4. **Professional UI/UX**: Clean, intuitive interface
5. **Scalable Architecture**: Easy to extend with more features
6. **Live Demonstration**: Real-time data visualization

## 🚀 Future Enhancements

- SMS alerts for critical conditions
- Multiple farm locations support
- Mobile app (PWA)
- Machine learning model training
- Integration with government agricultural databases

## 📞 Support

For technical support or questions about this project, please refer to the code comments or create an issue.

---

**Built for Chhattisgarh State Silver Jubilee Coding Competition 2025** 🏆
