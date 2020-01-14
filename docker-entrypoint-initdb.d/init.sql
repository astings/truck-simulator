CREATE USER writer;
CREATE DATABASE simulator;
GRANT ALL PRIVILEGES ON DATABASE simulator to writer;
GO ;

USE simulator;
CREATE SCHEMA truck_schema
    AUTHORIZATION writer;
-- Create a new table called 'TableName' in schema 'SchemaName'
-- Drop the table if it already exists
IF OBJECT_ID('truck_schema.truckposition', 'U') IS NOT NULL
DROP TABLE truck_schema.truckposition;
GO;
-- Create the table in the specified schema
CREATE TABLE truck_schema.truckposition
(
    IdEntry INT NOT NULL PRIMARY KEY AUTO INCREMENT, -- primary key column
    lat decimal(9,6) NOT NULL,
    lng decimal(9,6) NOT NULL
    ts timestamp NOT NULL,
    speed decimal(6,3) NOT NULL

);
GO