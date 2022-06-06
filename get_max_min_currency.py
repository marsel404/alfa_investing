import sqlite3


def get_max_min_currency(currency_pair):
    try:
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        currency_pair_get_id = cursor.execute(
            "SELECT * FROM api_currencypairs WHERE currency_pair == ?", (currency_pair, )).fetchone()
        id = currency_pair_get_id[0]
        min = cursor.execute(
            "SELECT * FROM api_currencypair WHERE currency_pair_id == ? ORDER BY min", (id, )).fetchone()
        max = cursor.execute(
            "SELECT * FROM api_currencypair WHERE currency_pair_id == ? ORDER BY -max", (id, )).fetchone()
        connection.close()
        print(str(currency_pair.upper()), min[2], max[3])
    except:
        print('Неизвестный параметр. Пожалуйста, укажите корректную валютную пару.')


get_max_min_currency('eurrub')
