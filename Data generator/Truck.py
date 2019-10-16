import math

import numpy as np
import requests
import geopy.distance
from random import uniform


class Truck:
    count_id = 0

    def __init__(self, speed: int = 10):
        self.num_id = Truck.count_id
        Truck.count_id += 1
        self.speed = speed
        self.distances = []
        self.coord = []

    @staticmethod
    def generate_itinerary(start: dict, end: dict):
        key = '5b3ce3597851110001cf6248f022aa2ca82b4338a12afb1b17fbd16f'
        headers = {
            "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
            'Authorization': key
        }

        url = 'https://api.openrouteservice.org/v2/directions/driving-car?api_key=' + key
        url += '&start=' + str(start['lng']) + ',' + str(start['lat'])
        url += '&end=' + str(end['lng']) + ',' + str(end['lat'])
        call = requests.get(url, headers=headers)
        coordinates = call.json()['features'][0]['geometry']['coordinates']
        print(call.json())
        return coordinates

    def get_coordinates(self, time):
        distance = self.speed * time
        dist_segment = 0
        i = 0
        while dist_segment < distance:
            dist_segment += self.distances[i]
            i += 1
        return self.coord[i]

    @staticmethod
    def get_distances(coord):
        distances = []
        for i in range(len(coord) - 1):
            distances.append(geopy.distance.geodesic(coord[i], coord[i + 1]).m)
            # self.compute_distance(coord[i][0], coord[i][1], coord[i + 1][0], coord[i + 1][1]))
        return distances

    @staticmethod
    def compute_distance(lat1, lon1, lat2, lon2):
        return np.arccos(np.sin(math.radians(lat1)) * np.sin(math.radians(lat2)) + np.cos(math.radians(lat1)) * np.cos(
            math.radians(lat2)) * np.cos(math.radians(lon1) - math.radians(lon2))) * 6371

    def drive_truck(self):
        start = {'lng': uniform(2.2632, 2.4083),
                 'lat': uniform(48.8319, 48.9019)}
        end = {'lng': uniform(2.2632, 2.4083),
               'lat': uniform(48.8319, 48.9019)}
        self.coord = self.generate_itinerary(start, end)
        self.distances = self.get_distances(self.coord)
        print(sum(self.distances))
        for i in range (200):
            print(self.get_coordinates(1*i))


if __name__ == "__main__":
    truck = Truck()
    start = {
        'lng': 2.309958,
        'lat': 48.849295
    }
    end = {
        'lng': 2.377816,
        'lat': 48.874886
    }
    truck.drive_truck()
