from flask import Flask, jsonify
from flask_cors import CORS
from geoalchemy2.shape import to_shape
from back.initiate_db import session, Driver, TruckPosition, Itinerary


app = Flask(__name__)

CORS(app)


@app.route('/')
def get_itinerate():
    truck_pos = session.query(TruckPosition).order_by(TruckPosition.identry.desc()).first()
    truck_pos = [to_shape(truck_pos.position).x, to_shape(truck_pos.position).y]
    return jsonify(truck_pos)
