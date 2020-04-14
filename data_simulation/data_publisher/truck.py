"""Contain Truck class with drive method used for simulations."""

import math
from random import uniform, random
from geojsonio import display
import json
import pyproj
from ors_api import get_direction
from time import time, sleep
from numpy.random import normal
import sys
from config import IDF_POLYGON, ISN2004, WGS84


class Truck:
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
        self._statuses = []

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

    def drive(self, debug: bool = False):
        """Simulate truck movement along a random itinerary."""
        start_time = time()
        start = self._generate_random_point()
        end = self._generate_random_point()
        generate_points_time = time()
        self._coord = self._generate_itinerary(start, end)
        generate_itinerary_time = time()
        self._plan_coord = self._change_coordinate_system(self._coord)
        change_coord_sys_time = time()
        self._distances = self._get_distance(self._plan_coord)
        calc_dist_time = time()
        self._statuses = self._generate_statuses()
        generate_statuses_time = time()
        self._speeds = self._generate_speeds(0.5)
        generate_speeds_time = time()

        if debug:
            print('Time to:\n')
            print('Generate points: %f' %
                  (generate_points_time - start_time))
            print('Generate itinerary: %f' %
                  (generate_itinerary_time - generate_points_time))
            print('Change coord: %f' %
                  (change_coord_sys_time - generate_itinerary_time))
            print('Calculate distances: %f' %
                  (calc_dist_time - change_coord_sys_time))
            print('Generate statuses: %f' %
                  (generate_statuses_time - calc_dist_time))
            print('Generate speeds: %f' %
                  (generate_speeds_time - generate_statuses_time))
            print('____________________________')
            print('TOTAL : %f' %
                  (generate_statuses_time - start_time))
            print('Number of coordinates: %i' %
                  (len(self._coord)))

        return start, end

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
                sleep(1)
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
    
    @staticmethod
    def _get_next_status(previous_status):
        rand = random()
        if previous_status is None:
                return 'driving'
        elif previous_status == 'driving':
            if rand <= 0.95:
                return 'driving'
            elif rand <= 0.97:
                return 'slow traffic'
            else :
                return 'full stop'
        elif previous_status == 'slow traffic':
            if rand <= 0.6:
                return 'slow traffic'
            elif rand <= 0.9:
                return 'exiting slow traffic'
            else:
                return 'full stop'
        elif previous_status == 'full stop':
            if rand <= 0.6:
                return 'full stop'
            elif rand <= 0.9:
                return 'slow traffic'
            else:
                return 'exiting slow traffic'
        elif previous_status == 'exiting slow traffic':
            return 'driving'
        else:
            print('Unknown status passed, defaulting to driving')
            return 'driving'
    
    def _generate_statuses(self):
        segments = self._parse_steps_from_call(self._saved_call)
        previous_status = None
        statuses = list()
        for segment in segments:
            previous_status = self._get_next_status(previous_status)
            statuses.append(previous_status)
        return statuses   

    def _generate_speeds(self, base_variation):
        """Simulate speeds along itinerary."""
        if self._saved_call is None:
            raise ValueError("No previous call made.")
        segments = self._parse_steps_from_call(self._saved_call)
        speed = self._speed
        speeds = list()
        for i, segment in enumerate(segments):
            if self._statuses[i] == 'driving':
                speed += base_variation * normal(0, 2, 1)[0]
                if speed < 5:
                    speed = 5
            elif self._statuses[i] == 'exiting slow traffic':
                speed = 10 + base_variation * normal(0, 2, 1)[0]
            elif self._statuses[i] == 'slow traffic':
                if speed > 5:
                    speed += (5 - speed) * abs(normal(0,0.6,1)[0])
                else:
                    speed += base_variation * normal(0, 2, 1)[0]
                if speed < 2:
                    speed = 2
            elif self._statuses[i] == 'full stop':
                speed = 0.5
            else:
                print('Unknown status, defaulting to driving...')
                speed += base_variation * normal(0, 2, 1)[0]
                if speed < 5:
                    speed = 5

            nb_coord_points = (
                segment["way_points"][1] -
                segment["way_points"][0] + 1
            )
            speeds.extend([speed] * nb_coord_points)
            print(f'Status {self._statuses[i]} at speed {speed}')
        return speeds

    @staticmethod
    def _parse_steps_from_call(call):
        return call['features'][0]['properties']['segments'][0]['steps']

    def get_coordinates(self, step: int = 10):
        """Generate coordinates for each second passed."""
        main_distance = 0
        distance = 0
        L = []
        i = 0
        current_timestamp = 0
        current_speed = self._speeds[0]
        while main_distance < sum(self._distances):
            while distance > 0 and i < len(self._distances)-1:
                distance -= self._distances[i]
                i += 1
                current_speed = self._speeds[i]
            if self._distances[i-1] == 0:
                i += 1
            distance += self._distances[i-1]
            advancement = distance / self._distances[i-1]
            current_timestamp += current_speed / step
            current_x = (
                self._coord[i-1][0] +
                advancement * (self._coord[i][0] - self._coord[i-1][0])
            )
            current_y = (
                self._coord[i-1][1] +
                advancement * (self._coord[i][1] - self._coord[i-1][1])
            )
            L.append([current_x,
                      current_y,
                      current_timestamp,
                      current_speed])
            i = 0
            main_distance += step
            distance = main_distance
        return (L)

    def get_position_at_time(self, time: int):
        """Get position at given time in seconds."""
        i = 0
        while time > 0 and i < len(self._distances):
            time -= self._distances[i]/self._speeds[i]
            i += 1

        i -= 1
        time += self._distances[i]/self._speeds[i]
        advancement = time /(self._distances[i]/ self._speeds[i])
        current_x = (
                self._coord[i][0] +
                advancement * (self._coord[i+1][0] - self._coord[i][0])
        )
        current_y = (
                self._coord[i][1] +
                advancement * (self._coord[i+1][1] - self._coord[i][1]))

        if i == (len(self._distances) - 1) and advancement > 1 :
            return self._coord[-1][0],self._coord[-1][1]

        return current_x, current_y
    
    def get_status_at_time(self, time:int):
        i = 0
        while time > 0 and i < len(self._distances):
            time -= self._distances[i]/self._speeds[i]
            i += 1
        return self._statuses[i-1]

if __name__ == '__main__':
    truck = Truck(1)
    start, end = truck.drive()
    print(start)
    print(end)
    truck.get_coordinates()


        
        
