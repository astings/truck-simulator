import math
import numpy as np
import requests
import geopy.distance
from random import uniform
from geojsonio import display
import json
import pyproj
from flotte import Flotte
from ors_api import ApiOrs
from shapely.geometry import Polygon

class Truck:
    count_id = 0
    api_ors = ApiOrs()

    def __init__(self,
                 flotte,
                 speed: int = 10):
        self.num_id = Truck.count_id
        Truck.count_id += 1
        self.speed = speed
        self.distances = []
        self.coord = []
        self.plan_coord = []
        self.owner = flotte
        flotte.truck_list.append(self)


    @staticmethod
    def generate_itinerary(start: dict, end: dict):
        call_json = Truck.api_ors.get_direction(start, end)
        coordinates = call_json['features'][0]['geometry']['coordinates']
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

    @staticmethod
    def generate_random_point():
        idf_json = requests.get('https://france-geojson.gregoiredavid.fr/repo/departements/75-paris/departement-75-paris.geojson')
        idf_coords = idf_json.json()["geometry"]["coordinates"][0]
        idf_polygon = Polygon(idf_coords)
        min_x, min_y, max_x, max_y = idf_polygon.bounds[0], idf_polygon.bounds[1], idf_polygon.bounds[2], idf_polygon.bounds[3]
        point = {
            "lng" : uniform(min_x, max_x),
            "lat" : uniform(min_y, max_y)
        }
        return point

    def drive(self):
        start = self.generate_random_point()
        end = self.generate_random_point()
        self.coord = self.generate_itinerary(start, end)
        self.plan_coord = self.change_coordinate_system(self.coord)
        self.distances = self.get_distance(self.plan_coord)
        print(sum(self.distances))

    def display_geojson(self):
        geo_object2 = {
            "type": "Feature",
            "geometry": {
                "type": "MultiPoint",
                "coordinates": self.get_coordinates()
            },
            "properties":{
                "name": "Truck %i"% self.num_id
            }

        }

        display(json.dumps(geo_object2))





if __name__ == "__main__":
    L = []
    # flotte = Flotte()
    # for i in range(2):
    #     truck = Truck(flotte)
    #     truck.drive()
    #
    # flotte.display_geojson()
    f1 = Flotte()
    t1 = Truck(flotte=f1)
    t1.drive()
    t1.display_geojson()
