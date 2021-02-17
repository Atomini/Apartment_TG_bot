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


def change_value_in_bill(chat_id, argument, value):
    """Меняет значение в таблице bill
    принемает argument - название строки
    value - значение"""
    with conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE bill SET {argument}={value} WHERE user_id = {chat_id}")
        conn.commit()