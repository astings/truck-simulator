"""Flotte class, each Truck must belong to a Flotte. 

Methods:
    display_geojson
    add_truck
"""

from geojsonio import display
import json
from truck import Truck


class Flotte():
    def __init__(self):
        self._truck_list = []

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

    def add_truck(self, truck):
        """Add Truck object to Flotte."""
        if not isinstance(Truck, truck):
            raise ValueError("Can only add trucks to a flotte")
        self._truck_list.append(truck)
        truck.owner = self
