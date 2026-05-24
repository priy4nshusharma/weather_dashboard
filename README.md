# 🌦️ SkyLens — Weather Data Dashboard

A real-time weather dashboard built with **Python (Flask)** and **Chart.js**.  
Fetches live data from the **Open-Meteo API** (free, no API key needed).

## Features
- 🌡️ Current temperature, wind speed, humidity
- 📅 7-day forecast with weather icons
- 📊 4 interactive charts (temperature, humidity, wind, precipitation)
- 🔍 Search any city in the world
- 🌐 Fully responsive web UI

## Tech Stack
| Layer    | Tech                        |
|----------|-----------------------------|
| Backend  | Python, Flask               |
| API      | Open-Meteo (free, no key)   |
| Frontend | HTML, CSS, JavaScript       |
| Charts   | Chart.js                    |

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python app.py
```

### 3. Open in browser
```
http://127.0.0.1:5000
```

## Project Structure
```
weather_dashboard/
├── app.py              # Flask backend + API logic
├── requirements.txt    # Dependencies
├── templates/
│   └── index.html      # Frontend dashboard
└── README.md
```

## How It Works
1. User searches a city name
2. Flask backend calls Open-Meteo Geocoding API to get coordinates
3. Coordinates are sent to Open-Meteo Weather API to fetch forecast
4. Data is returned as JSON to the frontend
5. Chart.js renders interactive charts

## Resume Points
- Built a full-stack weather dashboard using Python (Flask) and REST APIs
- Integrated Open-Meteo API for real-time weather data fetching and parsing
- Visualized hourly and 7-day forecast data using Chart.js
- Designed responsive UI with HTML/CSS/JavaScript
