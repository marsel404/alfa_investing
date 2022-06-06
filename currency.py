import sqlite3
import click
from datetime import datetime

"""Консольное приложение с двумя командами minmax и list"""

# Вводим переменную date, показывает текущую дату в формате yyyy-mm-dd.
# Потребуется для работы функций minmax и list: переменная задаёт значения по умолчанинию
# для day_yesterday и day_tommorrow
date = datetime.now().date()


@click.group(invoke_without_command=True)
def main():
    pass


@main.command()
@click.argument('currency_pair')
@click.argument('day_yesterday', default=date)
@click.argument('day_tommorow', default=date)
def minmax(currency_pair, day_yesterday, day_tommorow):
    """Функция показывает мин/макс значения валют за выбранный период времени"""
    try:
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        currency_pair_get_id = cursor.execute(
            "SELECT * FROM api_currencypairs WHERE currency_pair == ?", (currency_pair, )).fetchone()
        id = currency_pair_get_id[0]
        min = cursor.execute(
            "SELECT * FROM api_currencypair WHERE currency_pair_id == ? AND date BETWEEN ? AND ? ORDER BY min", (id, day_yesterday, day_tommorow)).fetchone()
        max = cursor.execute(
            "SELECT * FROM api_currencypair WHERE currency_pair_id == ? AND date BETWEEN ? AND ? ORDER BY -max", (id, day_yesterday, day_tommorow)).fetchone()
        print(f'MIN = {min[2]}\nMAX = {max[3]}')
    except:
        print(
            'Ошибка. Пожалуйста, введите команду в следующем формате: currency.py minmax (валютная пара) (дата начала) (дата окончания)\n'
            'Список доступных валютных пар: usdrub, eurrub, eurusd, gbpusd, usdjpy, eurjpy, audusd, btcusd, usdchf, usdcad, nzdusd, '
            'eurgbp, eurchf, jpyrub, euraud.\nФормат записи дат: yyyy-mm-dd')


@main.command()
@click.argument('currency_pair')
@click.argument('day_yesterday', default=date)
@click.argument('day_tommorow', default=date)
@click.option('--limit', default=3, help='Количиество строк')
def list(currency_pair, day_yesterday, day_tommorow, limit):
    """Вывод списка данных по определённой валютной паре за указанный период"""
    try:
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        currency_pair_get_id = cursor.execute(
            "SELECT * FROM api_currencypairs WHERE currency_pair == ?", (currency_pair, )).fetchone()
        id = currency_pair_get_id[0]
        data = cursor.execute("SELECT * FROM api_currencypair WHERE currency_pair_id == ? AND date BETWEEN ? AND ?",
                              (id, day_yesterday, day_tommorow)).fetchmany(limit)
        print(f'Count = {limit}')
        count = 0
        for item in data:
            count += 1
            print(f'{count}. {item[2]} {item[3]}')
    except:
        print(
            'Ошибка. Пожалуйста, введите команду в следующем формате: currency.py list (валютная пара)'
            ' (дата начала) (дата окончания) --limit (количество строк)\n'
            'Список доступных валютных пар: usdrub, eurrub, eurusd, gbpusd, usdjpy, eurjpy, audusd, btcusd, usdchf, usdcad, nzdusd, '
            'eurgbp, eurchf, jpyrub, euraud.\nФормат записи дат: yyyy-mm-dd')


if __name__ == '__main__':
    main()
