#!/usr/bin/env python3
"""
Demo data generator for Smart Soil Monitor
Generates realistic sensor data for demonstration purposes
"""

import sqlite3
import random
from datetime import datetime, timedelta
import time

def create_demo_database():
    """Create database with demo data"""
    print("📊 Creating demo database with sample data...")
    
    conn = sqlite3.connect('farm_data.db')
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute('DELETE FROM sensor_data')
    
    # Generate 24 hours of data (every 30 minutes)
    base_time = datetime.now() - timedelta(hours=24)
    
    for i in range(48):  # 48 data points (24 hours * 2 per hour)
        # Simulate realistic farming conditions
        hour = i // 2
        
        # Temperature varies throughout the day
        if 6 <= hour <= 18:  # Daytime
            temperature = random.uniform(25, 35)
        else:  # Nighttime
            temperature = random.uniform(18, 25)
        
        # Humidity varies inversely with temperature
        humidity = random.uniform(40, 80)
        
        # Soil moisture decreases during day, increases at night
        if 6 <= hour <= 18:
            soil_moisture = random.randint(30, 50)
        else:
            soil_moisture = random.randint(50, 70)
        
        # Add some realistic variation
        temperature += random.uniform(-2, 2)
        humidity += random.uniform(-10, 10)
        soil_moisture += random.randint(-5, 5)
        
        # Ensure values are within reasonable bounds
        temperature = max(15, min(40, temperature))
        humidity = max(20, min(95, humidity))
        soil_moisture = max(10, min(90, soil_moisture))
        
        # Insert data
        cursor.execute('''
            INSERT INTO sensor_data (temperature, humidity, soil_moisture, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (round(temperature, 1), round(humidity, 1), soil_moisture, 
              base_time + timedelta(minutes=30*i)))
    
    conn.commit()
    conn.close()
    
    print("✅ Demo database created with 24 hours of sample data")
    print("📈 Data includes realistic temperature, humidity, and soil moisture patterns")

def add_recent_data():
    """Add recent data points for live demonstration"""
    print("\n🔄 Adding recent data points...")
    
    conn = sqlite3.connect('farm_data.db')
    cursor = conn.cursor()
    
    # Add 5 recent data points (last 2.5 hours)
    for i in range(5):
        temperature = round(random.uniform(22, 28), 1)
        humidity = round(random.uniform(50, 70), 1)
        soil_moisture = random.randint(40, 60)
        
        cursor.execute('''
            INSERT INTO sensor_data (temperature, humidity, soil_moisture, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (temperature, humidity, soil_moisture, 
              datetime.now() - timedelta(minutes=30*i)))
    
    conn.commit()
    conn.close()
    
    print("✅ Recent data points added")

def main():
    """Main function"""
    print("🌱 Smart Soil Monitor - Demo Data Generator")
    print("=" * 50)
    
    create_demo_database()
    add_recent_data()
    
    print("\n🎉 Demo data generation completed!")
    print("📱 Start the server with: python app.py")
    print("🌐 Open browser: http://localhost:5000")
    print("📊 You should now see historical data in the charts")

if __name__ == "__main__":
    main()
