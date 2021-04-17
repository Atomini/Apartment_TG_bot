"""создание БД"""
import sqlite3 as sql


conn = sql.connect("database.db")

with conn:
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS novobud(
       _id                  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
       status               TEXT,
       district             TEXT,
       address              TEXT, 
       description          TEXT,
       construction_end     TEXT,
       link                 TEXT, 
       image                TEXT,
       price                INT,
       map_d                TEXT,
       map_w                TEXT
                )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS domria(
        _id                 INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        link                TEXT,
        description         TEXT,
        latitude            TEXT,
        longitude           TEXT,
        price_USD           TEXT,
        price_EUR           TEXT,
        price_UAH           TEXT,
        street_name         TEXT,
        building_number     TEXT,
        publishing_date     TEXT,
        photo_link          TEXT
                )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS bill(
        _id                     INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        user_id                 TEXT UNIQUE ,
        dollar                  INT ,
        dollar_elect            INT ,
        euro                    INT, 
        euro_elect              INT,
        grivna                  INT, 
        grivna_elect            INT,
        income                  INT,
        goal                    INT 
                )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS course(
        id                     INT,
        euro_sales             FLOAT,
        dollar_sales           FLOAT,
        euro_dollar_sales      FLOAT 
                )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS olx(
        _id                    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        title                  TEXT UNIQUE,
        price                  TEXT,
        link                   TEXT UNIQUE,
        image                  TEXT,
        add_date               TEXT
                )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS flafy(
        _id                    INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        title                  TEXT,
        price                  TEXT,
        link                   TEXT UNIQUE,
        district               TEXT
                )""")
