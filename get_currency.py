from selenium import webdriver
from bs4 import BeautifulSoup
import json
from datetime import datetime
from threading import Timer
import sqlite3

"""Этот скрипт получает доступ к странице https://ru.investing.com/charts/forex-charts, 
собирает данные по всем валютам с периодичностью 10 секунд и заносит данныев БД: {дата}, {мин цена},
{макс цена}"""


def get_data():

    currency_list = [
        ('usdrub', 0),
        ('eurrub', 1),
        ('eurusd', 2),
        ('gbpusd', 3),
        ('usdjpy', 4),
        ('eurjpy', 5),
        ('audusd', 6),
        ('btcusd', 7),
        ('usdchf', 8),
        ('usdcad', 9),
        ('nzdusd', 10),
        ('eurgbp', 11),
        ('eurchf', 12),
        ('jpyrub', 13),
        ('euraud', 14),
    ]

    """Сбор минимальной и максимальной цен валют"""
    # Выдёргиваю данные из json-файла, можно было ограничиться библиотекой requests,
    # но решил перестраховаться с помощью Selenium, чтобы свести к нулю вероятность бана моего ip
    # сервером донора
    driver = webdriver.Chrome(
        executable_path='chromedriver.exe')

    url = 'https://tvc4.investing.com/18e1e7f7bf41694738d6d94343607b30/1654182182/7/7/18/quotes?symbols=MCX%3AUSD%2FRUB%2CMCX%3AEUR%2FRUB%2CEUR%2FUSD%2CGBP%2FUSD%2CUSD%2FJPY%2CEUR%2FJPY%2CAUD%2FUSD%2CBitfinex%3ABTC%2FUSD%2CICE%3ADX%2CUSD%2FCHF%2CUSD%2FCAD%2CNZD%2FUSD%2CEUR%2FGBP%2CEUR%2FCHF%2CJPY%2FRUB%2CEUR%2FAUD'

    # Открываем Investing.com и получаем код json-файла
    driver.get(url)
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')

    # Создаём переменную с датой в виде dd.mm.yyyy
    date = datetime.now().date()

    # Работаем с данными и заливаем в БД
    for currency in currency_list:
        get_currency_pair(date, soup, currency[1], currency[1])

    driver.close()


def get_currency_pair(date, soup, cur_pair, n):
    """Работаем с данными и выдёргиваем необходимые значения"""
    # В этом блоке работаем с json-файлом и выдёргиваем из вложенных списков/словарей
    # мин и макс цену валютной пары
    slovar = json.loads(soup.body.text).get('d')
    list = slovar[n]
    slovar_inside_list = list.get('v')
    min = slovar_inside_list.get('bid')
    max = slovar_inside_list.get('ask')
    print(date, min, max)

    # Заливаем данные в БД
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO api_currencypair(date, min, max, currency_pair_id) VALUES (?, ?, ?, ?)', (date, min, max, cur_pair))
    connection.commit()
    connection.close()


def parsing(func, nth_sec):
    """Функция срабатывает каждые несколько секунд и запускает процесс парсинга из функции выше
    Цикл бесконечный, прерывается принудительно"""
    now_sec = datetime.now().second
    wait = (60 + nth_sec - now_sec) % 60
    Timer(wait, func).start()
    Timer(wait + 3, lambda: parsing(func, nth_sec)).start()


parsing(get_data, 5)
