import sqlite3 as sql


conn = sql.connect("..\\..\\..\\database\\database.db")


def delete_data(table):
    """ Удаляет все записаные данные из таблицы
        table: название таблици"""
    with conn:
        cur = conn.cursor()
        cur.execute(f"""DELETE FROM {table}""")
        conn.commit()


def add_data_to_table_bill(*args):
    """Добавляет даные в таблицу bill
    принимает 7 аргуменьов:
    user_id, dollar, dollar_elect, euro, euro_elect, grivna, grivna_elect"""
    with conn:
        cur = conn.cursor()
        data = args
        cur.execute("INSERT INTO bill (user_id, dollar, dollar_elect, euro, euro_elect, grivna, grivna_elect) "
                    "VALUES (?,?,?,?,?,?,?)", data)
        conn.commit()


def add_data_to_table_novobud(*args):
    """Добовляет данные в таблицу novobud
    принимает 10 аргументов:
    status, district, address, description, construction_end, link,image, price, map_d, map_w"""
    with conn:
        cur = conn.cursor()
        data = args
        cur.execute("INSERT INTO novobud (status, district, address, description, construction_end, link, "
                    "image, price, map_d, map_w) VALUES (?,?,?,?,?,?,?,?,?,?)", data)
        conn.commit()

#---------------test--------------
# delete_data("bill")
#add_data_to_table_bill("100" ,"2000" ,"0" ,"40" ,"4000" ,"0" , "100")