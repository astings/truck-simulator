FROM python:3.7

RUN python -m pip install --upgrade pip \
  && python -m pip install geoalchemy2 sqlalchemy flask flask_cors shapely psycopg2

COPY . .

EXPOSE 5000
