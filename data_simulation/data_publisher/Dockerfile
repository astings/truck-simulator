FROM python:3.7

RUN python -m pip install --upgrade pip \
  && python -m pip install numpy shapely pyproj geojsonio cryptography requests pika cython geoalchemy2 sqlalchemy pika psycopg2 names

COPY . .