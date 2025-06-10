-- filepath: c:\PostGress_Database\bdd_schema.sql
-- Create database (optional if you already created it)

-- Connect to the database (psql will not execute this inside the file, see note below)
-- \c bbd

-- You can omit the CREATE DATABASE line if you’ll connect first, then run the rest.

-- Table: Product
CREATE TABLE Product (
    id SERIAL PRIMARY KEY,
    nom TEXT NOT NULL,
    description TEXT,
    ingrédients TEXT,
    prix NUMERIC(10, 2) NOT NULL
);

-- Table: Store
CREATE TABLE Store (
    id SERIAL PRIMARY KEY,
    nom TEXT NOT NULL,
    adresse TEXT NOT NULL
);

-- Table: Store_Products
CREATE TABLE Store_Products (
    id_store INTEGER REFERENCES Store(id) ON DELETE CASCADE,
    id_product INTEGER REFERENCES Product(id) ON DELETE CASCADE,
    stock_unit INTEGER NOT NULL,
    PRIMARY KEY (id_store, id_product)
);