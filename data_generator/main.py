from flotte import Flotte
from truck import Truck
import pandas as pd


class Main():
    def __init__(self):
        self._writer = Csv_Writer()

    def write(self, n):
        """Write data locally for n simulations."""
        for _ in range(n):
            self._writer.run()


class Csv_Writer():
    def __init__(self):
        self.id = 0
        self.flotte = Flotte()
        self.truck = Truck(self.flotte)

    def run(self):
        """Write generated data into a local csv file."""
        self.truck.drive()
        name = r'data_generator/csv_files/test' + str(self.id) + '.csv'
        self.id += 1
        result = list(map(list, zip(*self.truck.get_coordinates())))
        df = pd.DataFrame({
            'lng': result[0],
            'lat': result[1],
            'ts': result[2],
            'speed': result[3]
        })
        df.to_csv(name, header=True)