DROP TABLE IF EXISTS fact_sales;
    DROP TABLE IF EXISTS dim_time;
    DROP TABLE IF EXISTS dim_item;
    DROP TABLE IF EXISTS dim_location;
            
    -- DIMENSIONES — atributos descriptivos y jerarquías
    CREATE TABLE dim_time (
    time_key INTEGER PRIMARY KEY,
    day DATE, month VARCHAR, quarter VARCHAR, year INTEGER );
            
    CREATE TABLE dim_item (
    item_key INTEGER PRIMARY KEY,
    item_name VARCHAR, brand VARCHAR, category VARCHAR );
            
    CREATE TABLE dim_location (
    loc_key INTEGER PRIMARY KEY,
    city VARCHAR, state VARCHAR, country VARCHAR );
    -- HECHOS — claves foraneas + medidas numericas
            
    CREATE TABLE fact_sales (
    time_key INTEGER REFERENCES dim_time(time_key),
    item_key INTEGER REFERENCES dim_item(item_key),
    loc_key INTEGER REFERENCES dim_location(loc_key),
    dollars_sold DECIMAL(12,2),
    units_sold INTEGER );

    INSERT INTO dim_time SELECT * FROM read_csv_auto('data/dim_time.csv');
    INSERT INTO dim_item SELECT * FROM read_csv_auto('data/dim_item.csv');
    INSERT INTO dim_location SELECT * FROM read_csv_auto('data/dim_location.csv');
    INSERT INTO fact_sales SELECT * FROM read_csv_auto('data/fact_sales.csv');

    DROP VIEW IF EXISTS v_sales;
    CREATE VIEW v_sales AS
    SELECT t.year, t.quarter, t.month, i.category, i.item_name, l.country, f.dollars_sold, f.units_sold
    FROM fact_sales f
    JOIN dim_time t USING (time_key)
    JOIN dim_item i USING (item_key)
    JOIN dim_location l USING (loc_key);