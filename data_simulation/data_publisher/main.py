"""Script to run simulations on multiple truck."""
from publisher import Publisher
import sys
from os import environ

def run_trucks(n: int):
    """Runs simulation for n trucks in parallel.

    Args:
        n (int): number of trucks for simulation
    """
    trucks = list()
    for i in range(n):
        trucks.append(Publisher(id_truck=i+1, id_driver=2, id_itinerary=i))
        # TODO: id_driver & itinerary generation
    for truck in trucks:
        truck.start()
    for truck in trucks:
        truck.join()


if __name__ == '__main__':
    if environ.get('NB_TRUCK') is not None:
        n = int(environ.get('NB_TRUCK'))
        print(f'Environement variable fetched, n = {n}')
    else:
        n = 4
        print(f'Environement variable not fetched, n = {n}')
    run_trucks(n)

