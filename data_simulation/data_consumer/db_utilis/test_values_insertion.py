from geoalchemy2 import *
from datetime import datetime
from db_utilis.initiate_db import session, Driver, Itinerary, TruckPosition

driver = Driver(
    firstname='Robin',
    lastname='Ambert'
)
session.add(driver)
session.commit()

depart = 'POINT(-126.4 45.32)'
arrivee = 'POINT(-124.4 42.32)'
itinerary = Itinerary(
    mission="Transport",
    departure=WKTElement(depart, srid=4326),
    arrival=WKTElement(arrivee, srid=4326)
)
session.add(itinerary)
session.commit()

position = 'POINT(-126.4 45.32)'

truck_position = TruckPosition(
    iddriver=2,
    idtruck=1,
    status="test",
    iditinerary=2,
    timestamp=datetime.now(),
    position=WKTElement(position, srid=4269)
)

session.add(truck_position)
session.commit()