"""Script to write local csv files from simulations."""

from truck import Truck
import pandas as pd
import sys

id = 0


def write(n):
    """Write data locally for n simulations.

    Args:
        n (int): number of simulations ran
    """
    for _ in range(n):
        run()


def run():
    """"Write generated data into a local csv file."""
    global id
    truck = Truck(id=0)
    truck.drive()
    name = r'csv_files/test' + str(id) + '.csv'
    id += 1
    result = list(map(list, zip(*truck.get_coordinates())))
    df = pd.DataFrame({
        'lng': result[0],
        'lat': result[1],
        'ts': result[2],
        'speed': result[3]
    })
    df.to_csv(name, header=True)


if __name__ == '__main__':
    n = int(sys.argv[1])
    write(n)
