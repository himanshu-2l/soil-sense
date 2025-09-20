# 🛠️ Smart Soil Monitor - Setup Guide

## 📋 Prerequisites

### Hardware
- ESP32 Development Board
- DHT22 Temperature & Humidity Sensor
- Soil Moisture Sensor (Analog)
- Jumper Wires
- Breadboard
- USB Cable for ESP32

### Software
- Arduino IDE
- Python 3.8 or higher
- Git (optional)

## 🔧 Step-by-Step Setup

### 1. Hardware Connections

#### ESP32 Pin Connections:
```
DHT22 Sensor:
- VCC → 3.3V
- GND → GND
- Data → GPIO 4

Soil Moisture Sensor:
- VCC → 3.3V
- GND → GND
- A0 → GPIO A0 (ADC)
```

### 2. Arduino IDE Setup

1. **Install ESP32 Board Package**
   - Open Arduino IDE
   - Go to File → Preferences
   - Add this URL to Additional Board Manager URLs:
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Go to Tools → Board → Boards Manager
   - Search for "ESP32" and install "ESP32 by Espressif Systems"

2. **Install Required Libraries**
   - Go to Tools → Manage Libraries
   - Install these libraries:
     - DHT sensor library by Adafruit
     - ArduinoJson by Benoit Blanchon
     - HTTPClient (usually included with ESP32)

3. **Configure and Upload Code**
   - Open `esp32_soil_monitor.ino`
   - Update WiFi credentials:
     ```cpp
     const char* ssid = "YOUR_WIFI_NAME";
     const char* password = "YOUR_WIFI_PASSWORD";
     ```
   - Update server URL (replace with your computer's IP):
     ```cpp
     const char* serverURL = "http://192.168.1.100:5000/api/sensor-data";
     ```
   - Select Board: "ESP32 Dev Module"
   - Select Port: Your ESP32 port
   - Click Upload

### 3. Python Backend Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Weather API Key**
   - Go to [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Get your API key
   - Replace `YOUR_API_KEY` in `app.py`

3. **Find Your Computer's IP Address**
   - Windows: Open Command Prompt, type `ipconfig`
   - Mac/Linux: Open Terminal, type `ifconfig`
   - Look for your local IP (usually 192.168.x.x)

4. **Update ESP32 Code with Your IP**
   - Edit `esp32_soil_monitor.ino`
   - Replace `192.168.1.100` with your actual IP address

### 4. Running the Application

1. **Start Python Server**
   ```bash
   python app.py
   ```
   You should see:
   ```
   🌱 Starting Smart Soil Monitor Server...
   📊 Database initialized
   🌐 Server starting on http://localhost:5000
   ```

2. **Connect ESP32**
   - Power on your ESP32
   - Check Arduino IDE Serial Monitor
   - You should see "Connected to WiFi" and "Data sent successfully"

3. **Access Dashboard**
   - Open browser: `http://localhost:5000`
   - You should see the Smart Soil Monitor dashboard

## 🔍 Troubleshooting

### ESP32 Not Connecting to WiFi
- Check WiFi credentials
- Ensure 2.4GHz network (ESP32 doesn't support 5GHz)
- Check signal strength

### No Data in Dashboard
- Verify ESP32 is connected to WiFi
- Check server IP address in ESP32 code
- Ensure Python server is running
- Check firewall settings

### Weather Data Not Loading
- Verify OpenWeatherMap API key
- Check internet connection
- API key might need activation time

### Sensor Readings Incorrect
- Check wiring connections
- Verify sensor power supply (3.3V)
- Calibrate soil moisture sensor if needed

## 📊 Testing the System

1. **Sensor Test**
   - Breathe on DHT22 sensor (should show humidity increase)
   - Touch soil moisture sensor (should show moisture change)
   - Check temperature readings

2. **Data Flow Test**
   - Monitor Arduino IDE Serial Monitor
   - Check Python server logs
   - Verify data appears in dashboard

3. **Dashboard Test**
   - Refresh browser to see new data
   - Check all cards show correct values
   - Verify chart updates with historical data

## 🚀 Competition Day Tips

1. **Pre-competition Setup**
   - Test everything the day before
   - Have backup ESP32 and sensors
   - Prepare demo data for presentation

2. **During Competition**
   - Start with Python server first
   - Then connect ESP32
   - Have dashboard ready for judges

3. **Presentation Points**
   - Show real-time data updates
   - Demonstrate AI recommendations
   - Explain hardware connections
   - Highlight mobile responsiveness

## 📱 Mobile Testing

- Test on different devices
- Check responsive design
- Verify touch interactions
- Test in different orientations

## 🔧 Advanced Configuration

### Customizing Crop Recommendations
Edit the `get_crop_recommendation()` function in `app.py` to add more crops or modify logic.

### Adding More Sensors
- Add sensor reading in ESP32 code
- Update database schema
- Add new dashboard cards
- Update API endpoints

### Styling Customization
Modify `templates/dashboard.html` CSS for different colors, fonts, or layouts.

---

**Ready to win the competition! 🏆**
