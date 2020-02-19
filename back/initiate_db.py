from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/trucks")
metadata = MetaData()
metadata.reflect(engine, only=['driver', 'truck_position', 'itinerary'])
Base = automap_base(metadata=metadata)

Base.prepare()

Driver, TruckPosition, Itinerary = Base.classes.driver, Base.classes.truck_position, \
                                   Base.classes.itinerary

session = Session(engine)
