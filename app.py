
from flask import request
import math
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import random
import threading
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Exact sector names to match your frontend
noida_sectors_list = [
    "Sector 62 (Industrial)", "Sector 18 (Commercial)", "Sector 50 (Residential)",
    "Sector 137 (Eco City)", "Pari Chowk", "Botanical Garden", "Sector 15 Metro",
    "Sector 128 (Wish Town)", "Sector 93A", "Sector 10 (Ind. Area)", 
    "Sector 21 Stadium", "Sector 37 (City Center)", "Sector 76", 
    "Sector 125 (Amity)", "Sector 44", "Sector 1 (Film City)", 
    "Sector 110 (Market)", "Sector 52", "Sector 12 (Residential)", "Sector 104 (Hub)"
]
def distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)
mock_data = {
    str(i+1): {
        "name": noida_sectors_list[i], 
        "aqi": random.randint(40, 250), 
        "last_updated": "Initializing..."
    } for i in range(len(noida_sectors_list))
}

def simulate_sensor_fluctuation():
    """Background task to simulate real-time data drift every 5 seconds"""
    while True:
        time.sleep(5) # The 5-second backend update trigger
        current_time = datetime.now().strftime("%H:%M:%S")
        for node_id in mock_data:
            # Generate a random drift (+/- 15 points)
            change = random.randint(-15, 15)
            mock_data[node_id]["aqi"] = max(10, min(450, mock_data[node_id]["aqi"] + change))
            mock_data[node_id]["last_updated"] = current_time
        print(f"[{current_time}] High-Frequency Sync: All Nodes Updated.")

# Start the simulation thread independently of the web server
threading.Thread(target=simulate_sensor_fluctuation, daemon=True).start()

@app.route('/')
def index():
    """This serves your dashboard from the /templates folder"""
    return render_template('index.html')

@app.route('/api/aqi')
def get_aqi():
    """API endpoint providing the latest mobile node data"""
    return jsonify(mock_data)
@app.route('/api/safest-route', methods=['POST'])
def safest_route():

    data = request.json
    start_id = data['start']
    end_id = data['end']

    # Coordinates dictionary (must match frontend)
    coords = {
        "1": (28.6289, 77.3769),
        "2": (28.5708, 77.3261),
        "3": (28.5677, 77.3661),
        "4": (28.5028, 77.4082),
        "5": (28.4671, 77.5134),
        "6": (28.5645, 77.3340),
        "7": (28.5833, 77.3111),
        "8": (28.5134, 77.3611),
        "9": (28.5280, 77.3880),
        "10": (28.5912, 77.3190),
        "11": (28.5950, 77.3390),
        "12": (28.5650, 77.3490),
        "13": (28.5630, 77.3850),
        "14": (28.5450, 77.3330),
        "15": (28.5520, 77.3420),
        "16": (28.5780, 77.3150),
        "17": (28.5350, 77.3950),
        "18": (28.5820, 77.3550),
        "19": (28.5920, 77.3250),
        "20": (28.5420, 77.3650)
    }

    start_coord = coords[start_id]
    end_coord = coords[end_id]

    start_aqi = mock_data[start_id]["aqi"]
    end_aqi = mock_data[end_id]["aqi"]

    dist = distance(start_coord[0], start_coord[1], end_coord[0], end_coord[1])

    exposure = dist * ((start_aqi + end_aqi) / 2)

    return jsonify({
        "route_coords": [
            start_coord,
            end_coord
        ],
        "total_exposure": round(exposure, 2)
    })

if __name__ == '__main__':
    # use_reloader=False prevents the background thread from running twice
    app.run(debug=True, port=5001, use_reloader=False)