import math
import requests
from random import uniform
from geojsonio import display
import json
import pyproj
from flotte import Flotte
from ors_api import ApiOrs
from shapely.geometry import Polygon
from time import time, sleep
from numpy.random import normal
import sys


class Truck:
    count_id = 0
    api_ors = ApiOrs()
    idf_json = requests.get(
        'https://france-geojson.gregoiredavid.fr/' +
        'repo/departements/75-paris/departement-75-paris.geojson'
        )

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
        """ Call API to retrieve itinerary coordinates between two points."""
        self.saved_call = Truck.api_ors.get_direction(start, end)
        # If calls returns error, remakes call
        if 'error' in self.saved_call.keys():
            sys.stdout.write('WAITING...')
            for i in range(10, 0, -1):
                sys.stdout.write(str(i)+'s ')
                sys.stdout.flush()
                sleep(1)
            start = self.generate_random_point()
            end = self.generate_random_point()
            coordinates = self.generate_itinerary(start, end)
            return coordinates
        else:
            coordinates = (self.saved_call
                           ['features']
                           [0]
                           ['geometry']
                           ['coordinates'])
            return coordinates

    def get_coordinates(self):
        """Generate equally distanced coordinates."""
        main_distance = 0
        distance = 0
        L = []
        i = 0
        current_timestamp = 0
        current_speed = self.speeds[0]
        while main_distance < sum(self.distances):
            while distance > 0 and i < len(self.distances)-1:
                distance -= self.distances[i]
                i += 1
                current_speed = self.speeds[i]
            if self.distances[i-1] == 0:
                i += 1
            distance += self.distances[i-1]
            advancement = distance / self.distances[i-1]
            current_timestamp += current_speed / 10
            current_x = (
                self.coord[i-1][0] +
                advancement * (self.coord[i][0] - self.coord[i-1][0])
            )
            current_y = (
                self.coord[i-1][1] +
                advancement * (self.coord[i][1] - self.coord[i-1][1])
            )
            L.append([current_x,
                      current_y,
                      current_timestamp,
                      current_speed])
            i = 0
            main_distance += 10
            distance = main_distance
        return (L)

    @staticmethod
    def change_coordinate_system(coord):
        """Transform WGS into Lambert 2004 coordinates."""
        temp_coordinate = []
        isn2004 = pyproj.Proj(
            "+proj=lcc +lat_1=64.25 +lat_2=65.75 +lat_0=65 +lon_0=-19 +" +
            "x_0=1700000 +y_0=300000 +no_defs +a=6378137 +rf=298.257222101" +
            "+to_meter=1")
        wgs84 = pyproj.Proj("+init=EPSG:4326")

        transformer = pyproj.Transformer.from_proj(wgs84, isn2004)
        # transform coordinates to comply with transformer
        temp_coordinate = list(map(list, zip(*coord)))
        result = transformer.transform(temp_coordinate[0], temp_coordinate[1])
        return list(map(list, zip(*result)))

    @staticmethod
    def get_distance(coord):
        """Compute distance between two coordinates."""
        distance = []
        for i in range(len(coord)-1):
            distance.append(math.sqrt(math.pow(coord[i+1][0]-coord[i][0], 2) +
                                      math.pow(coord[i+1][1]-coord[i][1], 2)))
        return distance

    @staticmethod
    def generate_random_point():
        """Generate random coordinate point in Ile-de-France."""
        idf_coords = Truck.idf_json.json()["geometry"]["coordinates"][0]
        idf_polygon = Polygon(idf_coords)
        min_x, min_y = idf_polygon.bounds[0], idf_polygon.bounds[1]
        max_x, max_y = idf_polygon.bounds[2], idf_polygon.bounds[3]
        point = {
            "lng": uniform(min_x, max_x),
            "lat": uniform(min_y, max_y)
        }
        return point

    def generate_speeds(self, base_variation):
        """Simulate speeds along itinerary."""
        if self.saved_call is None:
            raise ValueError("No previous call made.")
        segments = (
            self.saved_call
            ['features'][0]
            ['properties']
            ['segments'][0]
            ['steps'])
        speed = self.speed
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

    def drive(self, debug: bool = False):
        """Simulate truck movement along a random itinerary."""
        start_time = time()
        # Generate random points in IDF
        start = self.generate_random_point()
        end = self.generate_random_point()
        generate_points_time = time()
        # Generate itinerary
        self.coord = self.generate_itinerary(start, end)
        generate_itinerary_time = time()
        # Change to Lambert 2004 coord system
        self.plan_coord = self.change_coordinate_system(self.coord)
        change_coord_sys_time = time()
        # Compute distances
        self.distances = self.get_distance(self.plan_coord)
        calc_dist_time = time()
        # Compute varied speeds
        self.speeds = self.generate_speeds(0.5)
        generate_speeds_time = time()
        # If debug True prints time for each step
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
            print('Generate speeds: %f' %
                  (generate_speeds_time - calc_dist_time))
            print('____________________________')
            print('TOTAL : %f' %
                  (generate_speeds_time - start_time))
            print('Number of coordinates: %i' %
                  (len(self.coord)))
        return(sum(self.distances))

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


if __name__ == "__main__":
    L = []
    f1 = Flotte()
    t1 = Truck(flotte=f1)
    t1.drive()
    coord = t1.get_coordinates()

    distances = [i*10 for i in range(len(coord))]
    print(distances)
    timestamps = [elt[2] for elt in coord]
    speed = [elt[3] * 3.6 for elt in coord]

    # Plotting graphs for viz purposes
    import matplotlib.pyplot as plt
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.plot(distances, timestamps, color=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.plot(distances, speed, color=color)
    fig.tight_layout()
    plt.savefig('graph.png')

    # Display geojson
    t1.display_geojson()
