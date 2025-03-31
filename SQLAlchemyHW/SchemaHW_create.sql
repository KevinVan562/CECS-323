-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2025-02-17 01:22:42.955

-- tables
-- Table: schema_objects
CREATE TABLE schema_objects (
    schemas_name varchar(64)  NOT NULL,
    name varchar(64)  NOT NULL,
    description varchar(128)  NOT NULL,
    creation_date timestamp  NOT NULL,
    CONSTRAINT schema_objects_pk_01 PRIMARY KEY (schemas_name,name)
);

-- Table: schemas
CREATE TABLE schemas (
    name varchar(64)  NOT NULL,
    description varchar(128)  NOT NULL,
    creation_date timestamp  NOT NULL,
    CONSTRAINT schemas_pk_01 PRIMARY KEY (name)
);

-- foreign keys
-- Reference: schema_objects_schemas (table: schema_objects)
ALTER TABLE schema_objects ADD CONSTRAINT schema_objects_schemas
    FOREIGN KEY (schemas_name)
    REFERENCES schemas (name)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

