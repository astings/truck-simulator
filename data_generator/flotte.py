from geojsonio import display
import json


class Flotte():
    def __init__(self):
        self.truck_list = []

    def display_geojson(self):
        coord = []
        for truck in self.truck_list:
            for coordonnee in truck.get_coordinates():
                coord.append(coordonnee)
        geo_object2 = {
            "type": "MultiPoint",
            "coordinates": coord
        }
        display(json.dumps(geo_object2))