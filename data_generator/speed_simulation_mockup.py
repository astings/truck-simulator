import requests
from numpy.random import normal


class main:
    def __init__(self):
        self.key = key = "5b3ce3597851110001cf6248f022aa2ca82b4338a12afb1b17fbd16f"
        self.base_url = (
            "https://api.openrouteservice.org/v2/directions/driving-car?api_key"
        )
        self.base_url += "=" + self.key
        self.headers = {
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
            "Authorization": key,
        }
        self.saved_coordinates = list()
        self.saved_segments = list()
        self.saved_last_call = None
        self.speeds = list()

    def make_call(self, save=False):
        params = {
            "start": ",".join(map(str, [8.681495, 49.41461])),
            "end": ",".join(map(str, [8.687872, 49.420318])),
        }
        call = requests.get(self.base_url, params=params, headers=self.headers)
        call_json = call.json()
        if save:
            self.saved_last_call = call_json
            return
        else:
            return call_json

    def get_coord(self, save: bool = False, from_save: bool = False):
        if from_save:
            call_json = self.saved_last_call
        else:
            call_json = self.make_call()

        coordinates = call_json["features"][0]["geometry"]["coordinates"]

        if save:
            self.saved_coordinates = coordinates
            return
        else:
            return coordinates

    def get_segments(self, save: bool = False, from_save: bool = False):
        if from_save:
            call_json = self.saved_last_call
        else:
            call_json = self.make_call()

        segments = call_json["features"][0]["properties"]["segments"][0]["steps"]

        if save:
            self.saved_segments = segments
            return
        else:
            return segments


if __name__ == "__main__":
    speed = 12.5  # 45 km/h
    base_variation = 1.5  # 5.4 km/h
    m = main()
    m.make_call(save=True)
    m.get_coord(save=True, from_save=True)
    m.get_segments(save=True, from_save=True)

    for segment in m.saved_segments:
        speed += base_variation * normal(0, 0.5, 1)[0]
        nb_coord_points = segment["way_points"][1] - segment["way_points"][0] + 1
        m.speeds.extend([speed] * nb_coord_points)

    print(m.speeds)