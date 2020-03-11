import unittest
from data_publisher.truck import Truck


class TruckTestCase(unittest.TestCase):
    def setUp(self):
        self.truck = Truck(id=1)
        self.truck.drive()
    
    def test_default_truck_speed(self):
        self.assertEqual(self.truck.speed, 10, 'incorrect default speed')

    def test_speed_change(self):
        self.truck.speed = 20
        self.assertEqual(self.truck.speed, 20,
                         'incorrect speed after change')
    
    def test_owner_setter(self):
        self.truck.owner = 'test'
        self.assertEqual(self.truck.owner, 'test', 'incorrect owner after change')

    def test_change_coord(self): 
        test_coords = [[32.12,33.1],[12,13]]
        result = self.truck._change_coordinate_system(test_coords)
        expected_result = [[6699713.149606992, -1344501.6139290542],
                           [6357934.973254686, -5120165.410501068]]
        self.assertEqual(result, expected_result,
                         '''incorrect result for static method 
                            _change_coordinate_system''')

    def test_drive_completion(self):
        start, end = self.truck.drive()
        self.assertIsNotNone(start, "start should not be None")
        self.assertIsNotNone(end, "end should not be None")
        self.assertIsNotNone(self.truck._saved_call, "no save made")

    def drive_truck(self):
        self.truck.drive()
        print(self.truck._saved_call)

    def test_call_save(self):
        start = {'lng': 2.3093303,'lat': 48.8718765}
        end = {'lng': 2.3051033,'lat': 48.8751925}
        self.truck._generate_itinerary(start, end)
        self.assertIsNotNone(self.truck._saved_call, "saved call is None")
    
    def test_parse_step(self):
        self.assertIsNotNone(self.truck._parse_steps_from_call(self.truck._saved_call))

if __name__ == '__main__':
    unittest.main()