from logging import getLogger
import requests
from requests.exceptions import HTTPError
from django.contrib.gis.geos import Point

logger = getLogger(__name__)

NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org"

def geocode_address(address: str) -> Point | None:
    params = {
        "q": address,
        "format": "json",
        "countrycodes": "au",
    }
    headers = {"User-Agent": "SiteLog/1.0"}

    try:
        response = requests.get(f"{NOMINATIM_BASE_URL}/search", params, headers=headers)
        response.raise_for_status()

        results = response.json()
        if results:
            result = results[0]
            return Point(float(result["lon"]), float(result["lat"]))

        return None
    except HTTPError as e:
        logger.error(f"Failed to geocode address '{address}': {e}")

    return None
