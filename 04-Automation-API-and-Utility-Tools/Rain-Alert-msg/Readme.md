# 🌧️ Rain Alert App

Get SMS alerts when it's going to rain in your area using OpenWeather API and Twilio.

## 🚀 Features
- Fetches weather data for your city.
- Sends SMS alerts using Twilio.
- Can run daily via Task Scheduler or Cron.

## 🔧 Technologies
- Python
- OpenWeatherMap API
- Twilio API

## 📦 Setup
1. Get API keys from:
   - [OpenWeather](https://openweathermap.org/)
   - [Twilio](https://www.twilio.com/)
2. Install dependencies:
   ```bash
   pip install requests twilio
   ```
3. Run
   ```bash
   python rain_alert.py
