# Instructions for your Secret Server (Python code)
import os  # <-- ADDED THIS LINE to help find the file
from flask import Flask, request, send_file
import requests
from datetime import datetime

# --- CONFIGURATION ---
app = Flask(__name__)

# The reliable way to find the decoy image file:
# 1. Get the directory where your script is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 2. Join the directory path with the image file name. 
#    This ensures the script finds 'my_error.png' wherever the script is run from.
IMAGE_NAME = os.path.join(BASE_DIR, 'my_error.png')

LOG_FILE = 'scammer_log.txt' # The file that saves the addresses
GEO_API_URL = 'http://ipinfo.io/' # The online service to check the IP address

# -- THE MAIN SPYING TRICK --
@app.route('/image') 
def spy_on_click():
    # 1. Capture the Address (IP)
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # 2. Get Location Details from the online service
    try:
        location_response = requests.get(f"{GEO_API_URL}{user_ip}/json").json()
    except:
        location_response = {"city": "Unknown", "country": "Unknown"}

    city = location_response.get('city', 'N/A')
    country = location_response.get('country', 'N/A')
    
    # 3. Write the secret log entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] IP: {user_ip} | Location: {city}, {country}\n"
    
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)
    
    print(f"IP LOGGED: {user_ip} - {city}, {country}")
    
    # 4. Show the Decoy Image (fool the scammer)
    # This now uses the full, reliable path to the image file
    return send_file(IMAGE_NAME, mimetype='image/png')

# -- START THE SERVER --
if __name__ == '__main__':
    # The server is actually running on port 8000 based on your terminal output.
    print(f"Running the server. Link to test locally: http://127.0.0.1:8000/image")
    app.run(host='0.0.0.0', port=8000)