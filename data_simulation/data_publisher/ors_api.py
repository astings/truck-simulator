"""Openrouteservice API function to perform API calls in the Truck class."""

import requests
from config import ORS_URL, ORS_HEADERS


def get_direction(start: dict, end: dict):
    """Make API call to OpenRouteService API to generate directions.

    Args:
        start (dict): Starting point, contains keys lat and lng with
        matching lattitude and longitude of point.
        end (dict): End point, contains keys lat and lng with
        matching lattitude and longitude of point.

    Returns:
        dict: JSON associated with returned call
    """

    params = {
        "start": ",".join(map(str, [start['lng'], start['lat']])),
        "end": ",".join(map(str, [end['lng'], end['lat']]))
    }
    call = requests.get(ORS_URL,
                        params=params,
                        headers=ORS_HEADERS)

    return call.json()
