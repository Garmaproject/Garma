-- Create a schema
CREATE SCHEMA example_schema;

-- Create the PostGIS extension
CREATE EXTENSION postgis;

-- Create a sequence called 'user_seq' in the 'example_schema' schema
CREATE SEQUENCE example_schema.user_seq
    START WITH 1          -- Start at 1
    INCREMENT BY 1        -- Increment by 1
    NO MINVALUE           -- No minimum value
    NO MAXVALUE           -- No maximum value
    CACHE 1;              -- Cache of 1

-- Create a table 'users' in the 'example_schema' schema
-- with a geometry column and using the sequence for the id column
CREATE TABLE example_schema.users (
    id INTEGER DEFAULT nextval('example_schema.user_seq') PRIMARY KEY, -- Unique identifier using the sequence
    geom GEOMETRY(Point, 4326),          -- Geometry column of type Point with SRID 4326
    element VARCHAR(100) NOT NULL,       -- Element name, not null
    physical_conservation VARCHAR(100) UNIQUE NOT NULL, -- Unique and not null physical conservation
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Registration date, default to the current time
);  --and so on

-- Create a spatial index on the geom column
CREATE INDEX users_geom_idx ON example_schema.users USING GIST (geom);
