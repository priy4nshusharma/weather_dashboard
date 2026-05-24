from flask import Flask, render_template, jsonify, request
import requests
from datetime import datetime

app = Flask(__name__)

# Free API from Open-Meteo (no API key needed!)
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def get_coordinates(city):
    """Get lat/lon for a city name."""
    resp = requests.get(GEO_URL, params={"name": city, "count": 1, "language": "en", "format": "json"})
    data = resp.json()
    if "results" not in data or len(data["results"]) == 0:
        return None
    result = data["results"][0]
    return {
        "lat": result["latitude"],
        "lon": result["longitude"],
        "name": result["name"],
        "country": result.get("country", ""),
    }

def get_weather(lat, lon):
    """Fetch weather data from Open-Meteo."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation,windspeed_10m,relativehumidity_2m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode",
        "current_weather": True,
        "timezone": "auto",
        "forecast_days": 7,
    }
    resp = requests.get(WEATHER_URL, params=params)
    return resp.json()

WMO_CODES = {
    0: ("Clear Sky", "☀️"),
    1: ("Mainly Clear", "🌤️"),
    2: ("Partly Cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Fog", "🌫️"),
    48: ("Icy Fog", "🌫️"),
    51: ("Light Drizzle", "🌦️"),
    53: ("Drizzle", "🌦️"),
    55: ("Heavy Drizzle", "🌧️"),
    61: ("Light Rain", "🌧️"),
    63: ("Rain", "🌧️"),
    65: ("Heavy Rain", "🌧️"),
    71: ("Light Snow", "🌨️"),
    73: ("Snow", "❄️"),
    75: ("Heavy Snow", "❄️"),
    80: ("Rain Showers", "🌦️"),
    81: ("Rain Showers", "🌧️"),
    82: ("Violent Showers", "⛈️"),
    95: ("Thunderstorm", "⛈️"),
    99: ("Thunderstorm w/ Hail", "⛈️"),
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/weather")
def weather_api():
    city = request.args.get("city", "New Delhi")
    geo = get_coordinates(city)
    if not geo:
        return jsonify({"error": f"City '{city}' not found."}), 404

    data = get_weather(geo["lat"], geo["lon"])
    current = data["current_weather"]

    # Hourly data (next 24 hours)
    hourly = data["hourly"]
    hours = hourly["time"][:24]
    temps = hourly["temperature_2m"][:24]
    humidity = hourly["relativehumidity_2m"][:24]
    wind = hourly["windspeed_10m"][:24]
    precip = hourly["precipitation"][:24]

    hour_labels = [h.split("T")[1] for h in hours]

    # 7-day forecast
    daily = data["daily"]
    forecast = []
    for i in range(7):
        code = daily["weathercode"][i]
        desc, icon = WMO_CODES.get(code, ("Unknown", "🌡️"))
        date_str = daily["time"][i]
        day_name = datetime.strptime(date_str, "%Y-%m-%d").strftime("%a, %b %d")
        forecast.append({
            "day": day_name,
            "max": daily["temperature_2m_max"][i],
            "min": daily["temperature_2m_min"][i],
            "precip": daily["precipitation_sum"][i],
            "desc": desc,
            "icon": icon,
        })

    curr_code = current.get("weathercode", 0)
    curr_desc, curr_icon = WMO_CODES.get(curr_code, ("Unknown", "🌡️"))

    return jsonify({
        "city": geo["name"],
        "country": geo["country"],
        "current": {
            "temp": current["temperature"],
            "windspeed": current["windspeed"],
            "desc": curr_desc,
            "icon": curr_icon,
        },
        "hourly": {
            "labels": hour_labels,
            "temps": temps,
            "humidity": humidity,
            "wind": wind,
            "precip": precip,
        },
        "forecast": forecast,
    })

if __name__ == "__main__":
    app.run(debug=True)
