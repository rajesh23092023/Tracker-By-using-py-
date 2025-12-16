import os
import requests
from flask import Flask, request, send_file
from datetime import datetime

# --- Configuration ---
tracker_app = Flask(__name__)

# Define file paths dynamically to ensure reliable asset location.
PROJECT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DECOY_IMAGE_PATH = os.path.join(PROJECT_BASE_DIR, 'my_error.png')

IP_LOG_FILENAME = 'scammer_log.txt'
GEO_SERVICE_URL = 'http://ipinfo.io/'

# --- Tracking Route ---
@tracker_app.route('/image') 
def process_visitor_click():
    
    # Capture the real visitor IP address, accounting for proxy headers (like Ngrok).
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Lookup location details via external GeoIP service.
    try:
        location_data = requests.get(f"{GEO_SERVICE_URL}{visitor_ip}/json").json()
    except Exception:
        location_data = {"city": "Unknown", "country": "Unknown"}

    city_name = location_data.get('city', 'N/A')
    country_code = location_data.get('country', 'N/A')
    
    # Create and write the log entry.
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_record = (
        f"[{current_time}] IP: {visitor_ip} | "
        f"Location: {city_name}, {country_code}\n"
    )
    
    with open(IP_LOG_FILENAME, 'a') as log_file:
        log_file.write(log_record)
    
    # Provide immediate feedback to the local console.
    print(f"--- IP SUCCESSFULLY LOGGED ---: {visitor_ip} - {city_name}, {country_code}")
    
    # Serve the decoy image to the visitor.
    return send_file(DECOY_IMAGE_PATH, mimetype='image/png')

# --- Server Execution ---
if __name__ == '__main__':
    # Start the server on port 8000.
    print(f"Starting server... Test locally at: http://127.0.0.1:8000/image")
    tracker_app.run(host='0.0.0.0', port=8000)
