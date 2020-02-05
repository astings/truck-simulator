from geoalchemy2 import *
from etl_service.initiate_db import session, Driver, Itinerary, TruckPosition


def truck_position_to_db(data):

    truck_position = TruckPosition(
        iddriver=data['iddriver'],
        idtruck=data['idtruck'],
        status=data['status'],
        iditinerary=data['iditinerary'],
        timestamp=data['timestamp'],
        position=WKTElement(data['position'], srid=4269)
    )

    session.add(truck_position)
    session.commit()

    return 'done'


def driver_to_db(data):

    driver = Driver(
        firstname=data['firstname'],
        lastname=data['lastname']
    )

    session.add(driver)
    session.commit()

    return 'done'


def itinerary_to_db(data):

    itinerary = Itinerary(
        mission=data['mission'],
        departure=WKTElement(data['departure'], srid=4326),
        arrival=WKTElement(data['arrival'], srid=4326)
    )

    session.add(itinerary)
    session.commit()

    return 'done'
