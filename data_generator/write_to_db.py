import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import String
from truck import Truck
import pandas as pd

HOST = ""
PORT = ""
DBNAME = ""
USERNAME = ""
PASSWORD = ""
TEMPLATE_CONNECTION = "postgresql+psycopg2://%s:%s@%s:%s/%s"

engine = create_engine(TEMPLATE_CONNECTION % (
    USERNAME,
    PASSWORD,
    HOST,
    PORT,
    DBNAME
))

def write_truck_itinerary():
    truck = Truck(id=0)
    truck.drive()
    result = list(map(list, zip(*truck.get_coordinates())))
    df = pd.DataFrame({
        'lng': result[0],
        'lat': result[1],
        'ts': result[2],
        'speed': result[3]
    })
    df.to_sql(name='sqltableTODO', con=engine, if_exists='append',index=False) #Maybe add dtype arg
    

