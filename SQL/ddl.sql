-- ddl.sql

-- Restaurants table with the same structure as csv

CREATE TABLE restaurant (
  id INTEGER PRIMARY KEY,
  position INTEGER,
  name VARCHAR(256),
  score FLOAT,
  ratings INTEGER,
  category varchar(1024),
  price_range varchar(5),
  full_address varchar(1024),
  zip_code varchar(10),
  latitude DOUBLE PRECISION,
  longitude DOUBLE PRECISION
);

CREATE TABLE restaurant_menu_item (
  restaurant_id INTEGER,
  category VARCHAR(256),
  name VARCHAR(256),
  description VARCHAR(1024),
  price FLOAT
);



