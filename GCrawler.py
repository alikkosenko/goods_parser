#!/usr/bin/env python3

from SilpoCrawler import SilpoCrawler
from ATBCrawler import ATBCrawler
from TavriaCrawler import TavriaCrawler

import config

"""
Логика: Раз в сутки парситься вся база с 3-4 сайтов торговых сетей и сохраняется в БД в разные таблицы.
Данный модуль управляет данным процессом, в случае ошибки отправляет ALERT-сообщения в Телеграм-бота.
"""


class GCrawler:
    def __init__(self):
        pass

