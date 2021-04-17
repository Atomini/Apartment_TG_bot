import sqlite3 as sql
from pathlib import Path

#  ддя подключения к локальной базе данных
way = Path(__file__).parent / 'database.db'
print(way)
conn = sql.connect(way)


def delete_data(table):
    """ Удаляет все записаные данные из таблицы
        table: название таблици"""
    with conn:
        cur = conn.cursor()
        cur.execute(f"""DELETE FROM {table}""")
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


def add_to_course(dollar, euro, euro_dollar):
    """Обновляет данные в БД - таблица course"""
    cur = conn.cursor()
    cur.execute(f"UPDATE course SET euro_sales={euro}, dollar_sales={dollar}, "
                f"euro_dollar_sales={euro_dollar} WHERE id=1")
    conn.commit()


def get_from_course(param):
    """Для получение данних из БД - таблица course"""
    cur = conn.cursor()
    cur.execute(f"SELECT {param} FROM course WHERE id=1")
    par = cur.fetchall()
    conn.commit()
    return par[0][0]


def get_from_novobud():
    """Возвращает данные из БД в таблицу novobud"""
    try:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM novobud""")
        records = cur.fetchall()
        cur.close()
        return records
    except sql.Error as error:
        print("Ошибка", error)
    finally:
        if cur:
            cur.close()


def add_data_to_table_domria(*args):
    """Добовляет данные в таблицу domria
    принимает 11 аргументов:
    status, district, address, description, construction_end, link,image, price, map_d, map_w"""

    with conn:
        cur = conn.cursor()
        data = args
        cur.execute("INSERT INTO domria (link, description, latitude, longitude, price_USD, price_EUR, price_UAH,"
                    " street_name, building_number, publishing_date, photo_link) VALUES (?,?,?,?,?,?,?,?,?,?,?)", data)
        conn.commit()


def get_from_domria():
    """Возвращает данные из БД в таблицу dimria"""
    try:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM domria""")
        records = cur.fetchall()
        cur.close()
        return records
    except sql.Error as error:
        print("Ошибка", error)
    finally:
        if cur:
            cur.close()


def add_data_to_table_olx(*args):
    """Добовляет данные в таблицу olx
    принимает 5 аргументов:
    title, price, link, image, add_date"""
    with conn:
        cur = conn.cursor()
        data = args
        cur.execute("INSERT OR IGNORE INTO olx (title, price, link, image, add_date ) VALUES (?,?,?,?,?)", data)
        conn.commit()


def get_from_olx():
    """Возвращает данные из БД в таблицу olx"""
    try:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM olx""")
        records = cur.fetchall()
        cur.close()
        return records
    except sql.Error as error:
        print("Ошибка", error)
    finally:
        if cur:
            cur.close()


def add_data_to_table_flafy(*args):
    """Добовляет данные в таблицу flafy
    принимает 4 аргументов:
    title, price, link, district"""
    with conn:
        cur = conn.cursor()
        data = args
        cur.execute("INSERT OR IGNORE INTO flafy(title, price, link, district) VALUES (?,?,?,?)", data)
        conn.commit()


def get_from_flafy():
    """Возвращает данные из БД в таблицу flafy"""
    try:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM flafy""")
        records = cur.fetchall()
        cur.close()
        return records
    except sql.Error as error:
        print("Ошибка", error)
    finally:
        if cur:
            cur.close()

# для проверки работоспособности
if __name__ == '__main__':
    # change_value_in_bill("10770", "dollar", 1000)
    # delete_data
    get_from_novobud()
