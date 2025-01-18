import requests
import osmnx as ox

# Function to fetch data from OpenWeather API
def fetch_weather_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        data['main']['temp'] = data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
        return data
    else:
        print(f"Error fetching weather data: {response.status_code}")
        return None

# Function to fetch data from WAQI API
def fetch_aqi_data(city, api_key):
    url = f"http://api.waqi.info/feed/{city}/?token={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") == "ok":
            return data["data"]
        else:
            print(f"AQI API error: {data.get('data')}")
    else:
        print(f"Error fetching AQI data: {response.status_code}")
    return None

# Function to fetch route data from OpenStreetMap
def fetch_osm_route_data(origin_coords, destination_coords):
    """
    Fetch route data between two locations using OpenStreetMap.
    
    Args:
        origin_coords (tuple): Latitude and longitude of the starting point.
        destination_coords (tuple): Latitude and longitude of the ending point.
        
    Returns:
        route (list): List of latitude-longitude pairs for the route.
    """
    try:
        # Download the graph of the area
        G = ox.graph_from_point(origin_coords, dist=20000, network_type='drive')

        # Find the nearest nodes
        origin_node = ox.distance.nearest_nodes(G, origin_coords[1], origin_coords[0])
        destination_node = ox.distance.nearest_nodes(G, destination_coords[1], destination_coords[0])

        # Find the shortest path
        route = ox.shortest_path(G, origin_node, destination_node, weight='length')

        # Get route geometry
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        return route_coords
    except Exception as e:
        print(f"Error fetching OSM data: {e}")
        return None

# Example API keys (Replace with your own)
weather_api_key = "9a939355165997c5bc96fe69ce3370cd"
aqi_api_key = "99e2255e97e295eea3d1d01735b9faf64ed8a4e1"

# Example usage
city = "Mumbai"
origin_coords = (19.0760, 72.8777)  # Mumbai
destination_coords = (19.1076, 72.8376)  # Andheri

# Fetch data
weather_data = fetch_weather_data(city, weather_api_key)
aqi_data = fetch_aqi_data(city, aqi_api_key)
osm_route_data = fetch_osm_route_data(origin_coords, destination_coords)

# Print fetched data
if weather_data:
    print("Weather Data:", weather_data)
if aqi_data:
    print("AQI Data:", aqi_data)
if osm_route_data:
    print("OSM Route Data (Coordinates):", osm_route_data)
