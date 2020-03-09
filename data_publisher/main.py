"""Script to run simulations on multiple truck."""
from publisher import Publisher
import sys


def run_trucks(n: int):
    """Runs simulation for n trucks in parallel.

    Args:
        n (int): number of trucks for simulation
    """
    trucks = list()
    for i in range(n):
        trucks.append(Publisher(id_truck=i+1, id_driver=2, id_itinerary=i+2))
        # TODO: id_driver & itinerary generation
    for truck in trucks:
        truck.start()
    for truck in trucks:
        truck.join()


if __name__ == '__main__':
    run_trucks(4)
