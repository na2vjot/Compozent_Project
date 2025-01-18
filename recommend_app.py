from flask import Flask, jsonify, request,render_template
import pickle
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)

# Load the trained Random Forest model
with open(r'D:\My Data\Desktop\project\train_model.pkl', 'rb') as file:
    rf_model = pickle.load(file)
    
@app.route('/')
def home_page():
    return render_template("recommendation.html")

# API Keys (Please replace these with your actual keys)
WAQI_API_KEY = '99e2255e97e295eea3d1d01735b9faf64ed8a4e1'
OPENWEATHER_API_KEY = '9a939355165997c5bc96fe69ce3370cd'

# Rule-based logic for AQI insights
def rule_based_logic(aqi):
    if aqi >= 250:
        return "Hazardous conditions detected! It's recommended to avoid outdoor activities. Also installation of air purifiers is highly Recommended."
    elif aqi >= 200:
        return "Severe conditions detected. Prolonged exposure can cause chronic health issues or organ damage. Caution is advised if you are sensitive to air quality."
    elif aqi >= 150:
        return "Unhealthy conditions outside. Make sure to wear masks!"
    elif aqi >= 100:
        return "Poor conditions, people with respiratory issues may face problems."
    elif aqi >= 50:
        return "Moderate Conditions detected. Outdoor activities might cause mild discomfort in breathing."
    else:
        return "Air quality is good. Enjoy your outdoor activities safely."

# Function to fetch pollution data from WAQI API
def fetch_pollution_data(city):
    url = f'http://api.waqi.info/feed/{city}/?token={WAQI_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        aqi = data['data']['aqi']
        return aqi
    else:
        return None

# Function to fetch weather data from OpenWeather API
def fetch_weather_data(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
        weather_description = data['weather'][0]['description']
        return f"Weather: {weather_description}, Temp: {temperature:.2f}°C"
    else:
        return "Error fetching weather data."
    
geolocator = Nominatim(user_agent="my_geopy_app")

# Function to get latitude and longitude from a place name
def get_coordinates(place_name):
    location = geolocator.geocode(place_name)
    if location:
        return (location.latitude, location.longitude)
    else:
        return None

# Function to fetch traffic data from OpenStreetMap API
def get_traffic_data(start_location, end_location):
    url = f"https://router.project-osrm.org/route/v1/driving/{start_location[1]},{start_location[0]};{end_location[1]},{end_location[0]}?overview=full"
    response = requests.get(url)
    return response.json()

# Function to suggest safer routes
def suggest_safer_routes(start_place, end_place):
    start_coordinates = get_coordinates(start_place)
    end_coordinates = get_coordinates(end_place)

    if not start_coordinates or not end_coordinates:
        return "Could not find coordinates for one of the locations."

    traffic_data = get_traffic_data(start_coordinates, end_coordinates)

    if traffic_data and 'routes' in traffic_data:
        routes = traffic_data['routes']
        recommendations = []
        for route in routes:
            distance = route['distance'] / 1000  # Convert to kilometers
            duration = route['duration'] / 60  # Convert to minutes
            recommendations.append(f"Route: {distance:.2f} km, Estimated time: {duration:.2f} minutes")
        return recommendations
    else:
        return ["No routes found."]

@app.route('/get_aqi_insight', methods=['GET'])
def get_aqi_insight():
    city = request.args.get('city', 'Mumbai')
    aqi = fetch_pollution_data(city)
    
    if aqi is None:
        return jsonify({"error": "Error fetching pollution data."}), 400
    
    insights = rule_based_logic(aqi)
    return jsonify({"city": city, "aqi": aqi, "insight": insights})

@app.route('/get_weather', methods=['GET'])
def get_weather():
    lat = float(request.args.get('lat', 19.0760))  # Default to Mumbai coordinates
    lon = float(request.args.get('lon', 72.8777))
    weather_info = fetch_weather_data(lat, lon)
    return jsonify({"weather_info": weather_info})

@app.route('/get_safer_routes', methods=['GET'])
def get_safer_routes():
    start_place = request.args.get('start_place')
    end_place = request.args.get('end_place')

    if not start_place or not end_place:
        return jsonify({"error": "Please provide both start and end places."}), 400

    safer_routes = suggest_safer_routes(start_place, end_place)
    return jsonify({"start_place": start_place, "end_place": end_place, "routes": safer_routes})

if __name__ == "__main__":
    app.run(debug=True,port=8000)
