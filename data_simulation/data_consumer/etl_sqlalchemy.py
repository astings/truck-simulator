from geoalchemy2 import *
from initiate_db import session, Driver, Itinerary, TruckPosition
import names


def pos_to_string(position):
    template = 'POINT(%f %f)'
    return template % (position[0], position[1])


def truck_position_to_db(data):
    truck_position = TruckPosition(
        iddriver=data['iddriver'],
        idtruck=data['idtruck'],
        status=data['status'],
        iditinerary=data['iditinerary'],
        timestamp=data['timestamp'],
        position=WKTElement(pos_to_string(data['position']), srid=4269)
    )
    session.add(truck_position)
    session.commit()
    return f'Truck position {truck_position.position} written successfully'


    # new_driver = driver_to_db(data) 
    # new_itinerary = itinerary_to_db(data)
    # if new_driver == 1 and new_itinerary == 1:
    #     print('Unknown error occured (both driver and itinerary already existed.')
    # elif new_driver == 1 and new_itinerary == 0:
    #     print("Driver already existed in DB, itinerary added")
    # elif new_driver == 0 and new_itinerary == 1:
    #     print("Itinerary already existed in DB, driver added")
    # elif new_driver == 0 and new_itinerary == 0:
    #     print("Itinerary and driver added")
    # else:
    #     print('Unknown error, printing debugging info')
    #     print(f"Driver exists? {driver_exists(data['idriver'])}")
    #     print(f"Itinerary exists? {driver_exists(data['iditinerary'])}")

def truck_position_to_db_missing_foreign(data):
    session.rollback()
    truck_position = TruckPosition(
        iddriver=data['iddriver'],
        idtruck=data['idtruck'],
        status=data['status'],
        iditinerary=data['iditinerary'],
        timestamp=data['timestamp'],
        position=WKTElement(pos_to_string(data['position']), srid=4269)
    )
    if not driver_exists(data['iddriver']):
        session.add(generate_driver(data['iddriver']))
    if not itinerary_exists(data['iditinerary']):
        itinerary = Itinerary(
            mission=data['mission'],
            departure=WKTElement(pos_to_string(data['departure']), srid=4326),
            arrival=WKTElement(pos_to_string(data['arrival']), srid=4326)
        )
        session.add(itinerary) 
    session.commit()
    session.add(truck_position)
    session.commit()
    return f'Truck position {truck_position.position} written successfully'

def generate_driver(iddriver):
    firstname = names.get_first_name()
    lastname = names.get_last_name()
    return Driver(iddriver, firstname, lastname)

def driver_to_db(data):
    if driver_exists(data['iddriver']):
        return 1
    else :
        driver = generate_driver(data['iddriver'])
        session.add(driver)
        session.commit()
        return 0

def itinerary_to_db(data):
    if itinerary_exists(data['iditinerary']):
        return 1
    else:
        itinerary = Itinerary(
            iditinerary=data['iditinerary'],
            mission=data['mission'],
            departure=WKTElement(pos_to_string(data['departure']), srid=4326),
            arrival=WKTElement(pos_to_string(data['arrival']), srid=4326)
        )
        session.add(itinerary)
        session.commit()
        return 0

def driver_exists(iddriver):
    q = session.query(Driver).filter_by(iddriver=iddriver).exists()
    return session.query(q).scalar()

def itinerary_exists(iditinerary):
    q = session.query(Itinerary).filter_by(iditinerary=iditinerary).exists()
    return session.query(q).scalar()
