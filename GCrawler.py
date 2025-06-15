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
        self.SC = SilpoCrawler()
        self.AC = ATBCrawler()
        #self.TC = TavriaCrawler()
        self.Clist = [self.SC, self.AC]

    def crawl(self):
        for cat in config.categories:
            for crwl in self.Clist:
                crwl.parse_category(cat[crwl.name])

