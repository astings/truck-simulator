import math
import numpy as np
import requests
import geopy.distance
from random import uniform
from geojsonio import display
import json
import pyproj
# from flotte import Flotte

class Truck:
    count_id = 0

    def __init__(self,
                 # flotte,
                 speed: int = 10):
        self.num_id = Truck.count_id
        Truck.count_id += 1
        self.speed = speed
        self.distances = []
        self.coord = []
        self.plan_coord = []
        # self.owner = flotte
        # flotte.truck_list.append(self)


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
        call_json = call.json()
        print(json.dumps(call_json, indent=4, sort_keys=True))
        return coordinates

    def get_coordinates(self):
        main_distance = 0
        distance = 0
        L = []
        i=0
        while main_distance < sum(self.distances):
            while distance > 0 and i < len(self.distances)-1:
                distance -= self.distances[i]
                i += 1
            distance += self.distances[i-1]
            advancement = distance / self.distances[i-1]
            L.append([self.coord[i-1][0] + advancement * (self.coord[i][0] - self.coord[i-1][0]) ,self.coord[i-1][1] + advancement * (self.coord[i][1] - self.coord[i-1][1])])
            i=0
            main_distance += 10
            distance = main_distance

        return (L)


    @staticmethod
    def change_coordinate_system(coord):
        new_coordinate = []
        isn2004 = pyproj.Proj(
            "+proj=lcc +lat_1=64.25 +lat_2=65.75 +lat_0=65 +lon_0=-19 +x_0=1700000 +y_0=300000 +no_defs +a=6378137 +rf=298.257222101 +to_meter=1")
        wgs84 = pyproj.Proj("+init=EPSG:4326")
        for coordonnee in coord:
            new_coordinate.append([pyproj.transform(wgs84, isn2004, coordonnee[0], coordonnee[1])[0],pyproj.transform(wgs84, isn2004, coordonnee[0], coordonnee[1])[1]])
        return new_coordinate

    @staticmethod
    def get_distance(coord):
        distance = []
        for i in range(len(coord)-1):
            distance.append(math.sqrt(math.pow(coord[i+1][0]-coord[i][0],2)+math.pow(coord[i+1][1]-coord[i][1],2)))
        return distance

    def drive(self):
        start = {'lng': uniform(2.2632, 2.4083),
                 'lat': uniform(48.8319, 48.9019)}
        end = {'lng': uniform(2.2632, 2.4083),
               'lat': uniform(48.8319, 48.9019)}
        self.coord = self.generate_itinerary(start, end)
        self.plan_coord = self.change_coordinate_system(self.coord)
        self.distances = self.get_distance(self.plan_coord)
        print(sum(self.distances))

    def display_geojson(self):
        geo_object2 = {
            "type": "MultiPoint",
            "coordinates": truck.get_coordinates()
        }
        display(json.dumps(geo_object2))





if __name__ == "__main__":
    L = []
    truck = Truck()
    truck2 = Truck()

    truck.drive()
    truck2.drive()

    #print(truck.coord[0])
    #print(truck.coord[-1])


    print(truck.get_coordinates()[-1])

    truck.display_geojson()
