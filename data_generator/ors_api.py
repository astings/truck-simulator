import requests

"""
Openrouteservice API class to perform API calls in the Truck class
"""

class ApiOrs():
    """
    Openrouteservice Api object, used to fetch direction between two points

    Args:

    Attributes:
        _key (str): API key
        _base_url (str): URL used to make requests
        _headers (dict): Header passed in the request
    """
    def __init__(self):
        self._key = "5b3ce3597851110001cf6248f022aa2ca82b4338a12afb1b17fbd16f"  # Need change to secure key
        self._base_url = (
            "https://api.openrouteservice.org/v2/directions/driving-car?api_key",
            "=",
            self.key
            )
        self._headers = {
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
            "Authorization": key,
        }

    def get_direction(self, start:dict, end:dict):
        """
        Method invoked to make a direction GET request to the API

        Args:
            start (dict): Starting point, with keys 'lng' and 'lat'
            end (dict): Ending point, with keys 'lng' and 'lat'

        Returns:
            call (dict): JSON formatted object returned by the call
        """
        params = {
            "start": ",".join(map(str, [start['lng'], start['lat']]),
            "end": ",".join(map(str, [end['lng'], end['lat']]),
        }
        call = requests.get(self._base_url, params=params, headers=self._headers)
        return call.json()
