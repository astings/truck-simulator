CREATE DATABASE trucks;
\c trucks;

CREATE ROLE writer INHERIT;
GRANT CONNECT ON DATABASE trucks TO writer;
GRANT USAGE ON SCHEMA public TO writer;
GRANT INSERT ON ALL TABLES IN SCHEMA public TO writer;

CREATE ROLE reader INHERIT;
GRANT CONNECT ON DATABASE trucks TO reader;
GRANT USAGE ON SCHEMA public TO reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;

CREATE USER etl_server;
GRANT writer TO etl_server;

CREATE USER rest_api;
GRANT reader TO rest_api;

CREATE EXTENSION postgis;

CREATE TABLE driver
(
    iddriver  varchar
        constraint driver_pk
            primary key,
    firstname varchar,
    lastname  varchar
);

CREATE TABLE itinerary
(
    iditinerary varchar
        constraint itinerary_pk
            primary key,
    mission varchar,
    departure geography(Point, 4326),
    arrival geography(Point, 4326)
);

CREATE TABLE truck_position
(
    identry varchar not null
        constraint truck_position_pk
            primary key,
    iddriver varchar
        constraint truck_position_driver_iddriver_fk
            references driver,
    idtruck varchar,
    status varchar,
    iditinerary varchar
        constraint truck_position_itinerary_iditinerary_fk
            references itinerary,
    timestamp timestamp,
    position geography(Point, 4269)
);

