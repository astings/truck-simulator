"""Script to write local csv files from simulations."""
from publisher import Publisher

if __name__ == '__main__':
    trucks = []
    for i in range(4):
        trucks.append(Publisher(1+i, 2, i+2))
    for i in range(4):
        trucks[i].start()
    for i in range(4):
        trucks[i].join()
