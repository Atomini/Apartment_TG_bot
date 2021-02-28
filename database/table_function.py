import sqlite3 as sql

conn = sql.connect("database\\database.db")


# conn = sql.connect("..\\..\\..\\database\\database.db")
# conn = sql.connect("database.db")


def delete_data(table):
    """ Удаляет все записаные данные из таблицы
        table: название таблици"""
    with conn:
        cur = conn.cursor()
        cur.execute(f"""DELETE FROM {table}""")
        conn.commit()


# сейчас не актуально замененно на add_new_user_to_bill
# def add_data_to_table_bill(*args):
#     """Добавляет даные в таблицу bill
#     принимает 9 аргуменьов:
#     user_id, dollar, dollar_elect, euro, euro_elect, grivna, grivna_elect, income, goal"""
#     with conn:
#         cur = conn.cursor()
#         data = args
#         cur.execute("INSERT INTO bill (user_id, dollar, dollar_elect, euro, euro_elect, grivna,"
#                     " grivna_elect, income, goal) VALUES (?,?,?,?,?,?,?,?,?)", data)
#         conn.commit()


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


def add_new_user_to_bill(chat_id):
    """Добавляем нового юзера в таблицу bill по chat_id, если уже есть в таблице то не виполняется"""
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO bill (user_id, dollar, dollar_elect, euro, euro_elect, grivna,"
                " grivna_elect, income, goal) VALUES (?,?,?,?,?,?,?,?,?)", (chat_id, 0, 0, 0, 0, 0, 0, 0, 1))
    conn.commit()


def get_from_bill(chat_id, param):
    """Для получения даних из БД для пользованеля по Chat_id"""
    cur = conn.cursor()
    cur.execute(f"SELECT {param} FROM bill WHERE user_id={chat_id}")
    par = cur.fetchall()
    conn.commit()
    return par[0][0]

if __name__ == '__main__':
    # change_value_in_bill("10770", "dollar", 1000)
    # delete_data("bill")
    get_from_bill(785617282, "dollar")
