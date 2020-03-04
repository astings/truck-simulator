"""Contain Truck class with drive method used for simulations."""

import math
from random import uniform
from geojsonio import display
import json
import time
import datetime
import random
import pyproj
from ors_api import get_direction
from numpy.random import normal
import sys
from config import IDF_POLYGON, ISN2004, WGS84

class Truck():
    def __init__(self,
                 id,
                 speed: int = 10):

        self._num_id = id
        self._speed = speed
        self._owner = None
        self._saved_call = None
        self._distances = []
        self._coord = []
        self._plan_coord = []
        self._speeds = []
        self.departure_time = 0
        self.current_pos = {'lng': 2.410232, 'lat': 48.900129}
        self.status = 0

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        self._owner = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if not 0 <= value <= 30:
            raise ValueError('Speed must be between 0 and 30 meters/second')
        self._speed = value

    def drive(self):
        """Simulate truck movement along a random itinerary."""
        if self.current_pos != {'lng': 2.410232, 'lat': 48.900129}:
            end = {'lng': 2.410232, 'lat': 48.900129}
        else :
            end = self._generate_random_point()

        self._coord = self._generate_itinerary(self.current_pos, end)

        self.status = "waiting for departure"

        self._plan_coord = self._change_coordinate_system(self._coord)

        self._distances = self._get_distance(self._plan_coord)

        self.departure_time = datetime.datetime.now() + datetime.timedelta(seconds= random.randint(10,30))

        self._speeds = self._generate_speeds(0.5)


    @staticmethod
    def _generate_random_point():
        """Generate random coordinate point in Ile-de-France."""
        min_x, min_y = IDF_POLYGON.bounds[0], IDF_POLYGON.bounds[1]
        max_x, max_y = IDF_POLYGON.bounds[2], IDF_POLYGON.bounds[3]
        return {
            "lng": uniform(min_x, max_x),
            "lat": uniform(min_y, max_y)
        }

    def _generate_itinerary(self, start: dict, end: dict):
        """ Call API to retrieve itinerary coordinates between two points."""
        self._saved_call = get_direction(start, end)
        if 'error' in self._saved_call.keys():
            sys.stdout.write('WAITING...')
            for i in range(10, 0, -1):
                sys.stdout.write(str(i)+'s ')
                sys.stdout.flush()
                time.sleep(1)
            start = self._generate_random_point()
            end = self._generate_random_point()
            return self._generate_itinerary(start, end)
        else:
            return self._parse_coordinates_from_call(
                self._saved_call)

    @staticmethod
    def _parse_coordinates_from_call(call):
        return call['features'][0]['geometry']['coordinates']

    @staticmethod
    def _change_coordinate_system(coord):
        """Transform WGS into Lambert 2004 coordinates."""
        temp_coordinate = []
        transformer = pyproj.Transformer.from_proj(WGS84, ISN2004)
        # transform coordinates to comply with transformer format
        temp_coordinate = list(map(list, zip(*coord)))
        result = transformer.transform(temp_coordinate[0], temp_coordinate[1])
        return list(map(list, zip(*result)))

    @staticmethod
    def _get_distance(coord):
        """Compute distance between two coordinates."""
        distance = []
        for i in range(len(coord)-1):
            distance.append(math.sqrt(math.pow(coord[i+1][0]-coord[i][0], 2) +
                                      math.pow(coord[i+1][1]-coord[i][1], 2)))
        return distance

    def _generate_speeds(self, base_variation):
        """Simulate speeds along itinerary."""
        if self._saved_call is None:
            raise ValueError("No previous call made.")
        segments = self._parse_steps_from_call(self._saved_call)
        speed = self._speed
        speeds = list()
        for segment in segments:
            speed += base_variation * normal(0, 2, 1)[0]
            if speed < 0:
                speed = 0
            nb_coord_points = (
                segment["way_points"][1] -
                segment["way_points"][0] + 1
            )
            speeds.extend([speed] * nb_coord_points)
        return speeds

    @staticmethod
    def _parse_steps_from_call(call):
        return call['features'][0]['properties']['segments'][0]['steps']

    def get_position_at_time(self, t: datetime):
        """Get position at given time in seconds."""
        main_distance = 0
        i = 0
        t = (t - self.departure_time).total_seconds()
        if t < 0:
            self.status = 'waiting for departure'
            return [self._coord[0][0], self._coord[0][1]]

        while t > 0 and i < len(self._distances):
            t -= self._distances[i]/self._speeds[i]
            i += 1

        i -= 1
        t += self._distances[i]/self._speeds[i]
        advancement = t /(self._distances[i]/ self._speeds[i])
        current_x = (
                self._coord[i][0] +
                advancement * (self._coord[i+1][0] - self._coord[i][0])
        )
        current_y = (
                self._coord[i][1] +
                advancement * (self._coord[i+1][1] - self._coord[i][1]))
        self.status = 'driving'

        if i == (len(self._distances) - 1) and advancement > 1 :
            return [self._coord[-1][0],self._coord[-1][1]]
            self.status = "arrived"

        return [current_x, current_y]


    def display_geojson(self):
        """Display itinerary on map."""
        geo_object2 = {
            "type": "Feature",
            "geometry": {
                "type": "MultiPoint",
                "coordinates": self.coord
            },
            "properties": {
                "name": "Truck %i" % self.num_id
            }
        }
        display(json.dumps(geo_object2))


if __name__ == '__main__':
    truck = Truck(1)
    truck.drive()
    for i in range(1000):
        print(truck.get_position_at_time(datetime.datetime.now()))
        time.sleep(1)





