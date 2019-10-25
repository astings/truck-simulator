from shapely.geometry import Polygon
from geojsonio import display
from random import uniform
import json
import requests

idf_json = requests.get('https://france-geojson.gregoiredavid.fr/repo/departements/75-paris/departement-75-paris.geojson')
idf_coords = idf_json.json()["geometry"]["coordinates"][0]
idf_polygon = Polygon(idf_coords)
min_x, min_y, max_x, max_y = idf_polygon.bounds[0], idf_polygon.bounds[1], idf_polygon.bounds[2], idf_polygon.bounds[3]
point = [uniform(min_x, max_x), uniform(min_y, max_y)]
geo_obj = {
    "type" : "Feature",
    "geometry": {
    "type":"Point",
    "coordinates": point
    },
    "properties": {
    "name": "Random point in Paris"
    }
}

display(json.dumps(geo_obj))
