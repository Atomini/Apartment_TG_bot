import sqlite3 as sql

conn = sql.connect("database.db")

with conn:
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS novobud(
       id                   INT PRIMARY KEY,
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
    cur.execute("""CREATE TABLE IF NOT EXISTS bill(
    id                      INT PRIMARY KEY,
    user_id                 INT ,
    dollar                  INT ,
    dollar_elect            INT ,
    euro                    INT, 
    euro_elect              INT,
    grivna                  INT, 
    grivna_elect            INT 
                )""")

    conn.commit()