import math
import requests
from random import uniform
from geojsonio import display
import json
import pyproj
from flotte import Flotte
from ors_api import ApiOrs
from shapely.geometry import Polygon
from time import time
from numpy.random import normal


class Truck:
    count_id = 0
    api_ors = ApiOrs()

    def __init__(self,
                 flotte,
                 speed: int = 10):
        self.num_id = Truck.count_id
        Truck.count_id += 1
        self.speed = speed
        self.saved_call = None
        self.distances = []
        self.coord = []
        self.plan_coord = []
        self.owner = flotte
        self.speeds = []
        flotte.truck_list.append(self)

    def generate_itinerary(self, start: dict, end: dict):
        call_json = Truck.api_ors.get_direction(start, end)
        self.saved_call = call_json
        coordinates = call_json['features'][0]['geometry']['coordinates']
        return coordinates

    def get_coordinates(self):
        main_distance = 0
        distance = 0
        L = []
        i = 0
        while main_distance < sum(self.distances):
            while distance > 0 and i < len(self.distances)-1:
                distance -= self.distances[i]
                i += 1
            distance += self.distances[i-1]
            advancement = distance / self.distances[i-1]
            L.append([self.coord[i-1][0] + advancement * (self.coord[i][0] - self.coord[i-1][0]) ,self.coord[i-1][1] + advancement * (self.coord[i][1] - self.coord[i-1][1])])
            i = 0
            main_distance += 10
            distance = main_distance

        return (L)

    @staticmethod
    def change_coordinate_system(coord):
        new_coordinate = []
        isn2004 = pyproj.Proj(
            "+proj=lcc +lat_1=64.25 +lat_2=65.75 +lat_0=65 +lon_0=-19 +x_0=1700000 +y_0=300000 +no_defs +a=6378137 +rf=298.257222101 +to_meter=1")
        wgs84 = pyproj.Proj("+init=EPSG:4326")
        transformer = pyproj.Transformer.from_proj(wgs84, isn2004)
        new_coordinate = list(map(list, zip(*coord)))
        result = transformer.transform(new_coordinate[0], new_coordinate[1])
        return list(map(list, zip(*result)))

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
            "lng": uniform(min_x, max_x),
            "lat": uniform(min_y, max_y)
        }
        return point
    
    def generate_speeds(self, base_variation):
        if self.saved_call is None:
            raise ValueError("No previous call made.")
        segments = self.saved_call["features"][0]["properties"]["segments"][0]["steps"]
        speed = self.speed
        speeds = list()
        for segment in segments:
            speed += base_variation * normal(0, 0.5, 1)[0]
            nb_coord_points = segment["way_points"][1] - segment["way_points"][0] + 1
            speeds.extend([speed] * nb_coord_points)
        return speeds

    def drive(self, debug: bool = False):
        start_time = time()
        start = self.generate_random_point()
        end = self.generate_random_point()
        generate_points_time = time()
        self.coord = self.generate_itinerary(start, end)
        generate_itinerary_time = time()
        self.plan_coord = self.change_coordinate_system(self.coord)
        change_coord_sys_time = time()
        self.distances = self.get_distance(self.plan_coord)
        calc_dist_time = time()
        self.speeds = self.generate_speeds(1.5)
        generate_speeds_time = time()
        if debug:
            print('Time to:\n')
            print('Generate points: %f' % (generate_points_time - start_time))
            print('Generate itinerary: %f' % (generate_itinerary_time - generate_points_time))
            print('Change coord: %f' % (change_coord_sys_time - generate_itinerary_time))
            print('Calculate distances: %f' % (calc_dist_time - change_coord_sys_time))
            print('Generate speeds: %f' % (generate_speeds_time - calc_dist_time))
            print('____________________________')
            print('TOTAL : %f' % (generate_speeds_time - start_time))
            print('Number of coordinates:\n')
            print(len(self.coord))
        return(sum(self.distances))

    def display_geojson(self):
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


if __name__ == "__main__":
    L = []

    f1 = Flotte()
    t1 = Truck(flotte=f1)
    for _ in range(15):
        dist = t1.drive(debug = False)
        print("Relative error:")
        print((t1.saved_call['features'][0]['properties']['segments'][0]['distance']- dist)/dist)
        print('\n Abs error:')
        print(t1.saved_call['features'][0]['properties']['segments'][0]['distance']- dist)
