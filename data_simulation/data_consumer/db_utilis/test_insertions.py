"""[A reprendre] Tests for database insertions"""
from geoalchemy2 import WKTElement
from datetime import datetime
from db_utilis.initiate_db import session, Driver, Itinerary, TruckPosition
import unittest

class DbTestCase(unittest.TestCase):
    driver = Driver(
            firstname='Robin',
            lastname='Ambert'
        )
    depart = 'POINT(-126.4 45.32)'
    arrivee = 'POINT(-124.4 42.32)'
    itinerary = Itinerary(
            mission="Transport",
            departure=WKTElement(depart, srid=4326),
            arrival=WKTElement(arrivee, srid=4326)
        )
    position = 'POINT(-126.4 45.32)'
    truck_position = TruckPosition(
            iddriver=2,
            idtruck=1,
            status="test",
            iditinerary=2,
            timestamp=datetime.now(),
            position=WKTElement(position, srid=4269)
        )

    def setUp(self):
        session.add(DbTestCase.driver)
        session.commit()
        session.add(DbTestCase.itinerary)
        session.commit()
        session.add(DbTestCase.truck_position)
        session.commit()

    def tearDown(self):
        session.delete(DbTestCase.driver)
        session.commit()
        session.delete(DbTestCase.itinerary)
        session.commit()
        session.delete(DbTestCase.truck_position)
        session.commit()

    def test_insertions(self):
        q_driver =  session.query(Driver).filter_by(
            firstname = 'Robin',
            lastname = 'Ambert')
        self.assertIsNotNone(q_driver.first())
        q_itinerary = session.query(Itinerary).filter_by(
            mission = 'Transport')
        self.assertIsNotNone(q_itinerary.first())
        q_truckposition = session.query(TruckPosition).filter_by(
            status = 'test')
        self.assertIsNotNone(q_truckposition.first())
        

if __name__ == '__main__':
    unittest.main()