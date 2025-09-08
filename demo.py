import requests
import time

TECHNICIAN_ID = 1
BASE_URL = "http://127.0.0.1:8000"

LOCATIONS = {
    "off_site_start": {"lat": -37.76300, "lon": 144.94300},
    "on_site": {"lat": -37.76384, "lon": 144.94328},
    "off_site_end": {"lat": -37.76450, "lon": 144.94400},
}

def send_ping(technician_id: int, location_data: dict[str, float]):
    """Sends a POST request to the ping endpoint."""
    url = f"{BASE_URL}/api/technicians/{technician_id}/ping/"
    payload = {
        "latitude": location_data["lat"],
        "longitude": location_data["lon"]
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 204:
            print(f"Server Response ({response.status_code})\n")
        else:
            print(f"Server Response ({response.status_code}): {response.json().get('message', 'No message')}\n")
    except requests.exceptions.RequestException:
        raise

    time.sleep(3)

if __name__ == "__main__":
    send_ping(TECHNICIAN_ID, LOCATIONS["off_site_start"])
    send_ping(TECHNICIAN_ID, LOCATIONS["on_site"])
    send_ping(TECHNICIAN_ID, LOCATIONS["on_site"])
    send_ping(TECHNICIAN_ID, LOCATIONS["off_site_end"])
