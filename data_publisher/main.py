"""Script to write local csv files from simulations."""
from publisher import emit_truck_info


if __name__ == '__main__':
    while True:
        emit_truck_info()
