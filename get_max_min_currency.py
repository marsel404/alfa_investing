import sqlite3


def get_max_min_currency(currency_pair):
    try:
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        min = cursor.execute(
            "SELECT * FROM " + currency_pair + " ORDER BY min ").fetchone()
        max = cursor.execute(
            "SELECT * FROM " + currency_pair + " ORDER BY -max ").fetchone()
        connection.close()
        print(str(currency_pair.upper()), min[1], max[2])
    except:
        print('Неизвестный параметр. Пожалуйста, укажите корректную валютную пару.')


get_max_min_currency('eurrub')
