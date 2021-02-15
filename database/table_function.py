import sqlite3 as sql

conn = sql.connect("database.db")


def delete_data(table):
    with conn:
        cur = conn.cursor()
        cur.execute(f"""DELETE FROM {table}""")
        conn.commit()


def add_data_to_table_bill(*args):
    with conn:
        cur = conn.cursor()
        data = args
        cur.execute("INSERT INTO bill (user_id, dollar, dollar_elect, euro, euro_elect, grivna, grivna_elect) "
                    "VALUES (?,?,?,?,?,?,?)", data)
        conn.commit()


#---------------test--------------
# delete_data("bill")
add_data_to_table_bill("100" ,"2000" ,"0" ,"40" ,"4000" ,"0" , "100")