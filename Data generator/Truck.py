import requests


class Truck:
    count_id = 0

    def __init__(self, speed: int = 80):
        self.num_id = Truck.count_id
        Truck.count_id += 1
        self.speed = speed

    def generate_itinerary(self, direction):
        key = '5b3ce3597851110001cf6248f022aa2ca82b4338a12afb1b17fbd16f'
        headers = {
                "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
                'Authorization' : key
                }

        url = 'https://api.openrouteservice.org/v2/directions/driving-car?api_key=' + key
        url += '&start=' + str(start['lng']) + ',' + str(start['lat'])
        url += '&end=' + str(end['lng']) + ',' + str(end['lat'])
        call = requests.get(url, headers=headers)
        coordinates = call.json()['features'][0]['geometry']['coordinates']
        #print (call.json())
        return coordinates

    def get_coordinates(self, start:dict, end:dict):

    def drive_truck(self):
        pass



if __name__ == "__main__":
    truck = Truck()
    start = {
                'lng': 2.309958,
                'lat': 48.849295
                }
    end = {
                'lng':2.377816,
                'lat':48.874886
                }
    print(truck.generate_itinerary(start, end))

