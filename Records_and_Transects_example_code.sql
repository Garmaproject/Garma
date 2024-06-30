-- Create the 'record' table to store archaeological remains points
CREATE TABLE record (
    id SERIAL PRIMARY KEY,               -- Auto-incrementing unique identifier
    geom GEOMETRY(Point, 4326),          -- Geometry column of type Point with SRID 4326
    remains_type VARCHAR(50),            -- Type of archaeological remains, up to 50 characters
    description TEXT,                    -- Description of the record
    date TIMESTAMP DEFAULT NOW()         -- Date and time of the record, default to the current time
);

-- Create the 'Fauna_CAI_Lower_Gallery_La_Garma' table to store fauna polygons
CREATE TABLE Fauna_CAI_Lower_Gallery_La_Garma (
    id SERIAL PRIMARY KEY,               -- Auto-incrementing unique identifier
    geom GEOMETRY(Polygon, 4326),        -- Geometry column of type Polygon with SRID 4326
    description TEXT                     -- Description of the record
);

-- Create a function 'insert_record' that will be executed as a trigger
CREATE OR REPLACE FUNCTION insert_record()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert a new record in the 'record' table with the centroid of the polygon and the description
    INSERT INTO record (geom, remains_type, description)
    VALUES (ST_Centroid(NEW.geom), TG_ARGV[0], NEW.description);
    RETURN NEW;  -- Return the new record
END;
$$ LANGUAGE plpgsql;  -- Define the function language as PL/pgSQL

-- Create a trigger 'trigger_fauna' that will be executed after each insertion in 'Fauna_CAI_Lower_Gallery_La_Garma'
CREATE TRIGGER trigger_fauna
AFTER INSERT ON Fauna_CAI_Lower_Gallery_La_Garma
FOR EACH ROW
EXECUTE FUNCTION insert_record('Fauna CAI Lower Gallery La Garma');

-- Create the 'transects' table to store transect lines
CREATE TABLE transects (
    id SERIAL PRIMARY KEY,               -- Auto-incrementing unique identifier
    geom GEOMETRY(LineString, 4326),     -- Geometry column of type LineString with SRID 4326
    date TIMESTAMP DEFAULT NOW()         -- Date and time of the transect, default to the current time
);

-- Create a function 'generate_transects' that will be executed as a trigger
CREATE OR REPLACE FUNCTION generate_transects()
RETURNS TRIGGER AS $$
BEGIN
    -- Insert a new line in the 'transects' table that connects all points in 'record' in order of date
    INSERT INTO transects (geom)
    SELECT ST_MakeLine(ARRAY(
        SELECT geom
        FROM record
        ORDER BY date
    ));
    RETURN NEW;  -- Return the new record
END;
$$ LANGUAGE plpgsql;  -- Define the function language as PL/pgSQL

-- Create a trigger 'trigger_transects' that will be executed after each insertion in 'record'
CREATE TRIGGER trigger_transects
AFTER INSERT ON record
FOR EACH ROW
EXECUTE FUNCTION generate_transects();
