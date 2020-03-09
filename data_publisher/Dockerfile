FROM python:3.7

RUN python -m pip install --upgrade pip \
  && python -m pip install numpy shapely pyproj geojsonio cryptography requests pika cython

COPY . .