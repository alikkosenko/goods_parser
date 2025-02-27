#!/usr/bin/env python3
import os

import telebot
from SilpoCrawler import SilpoCrawler
from DBCursor import DBCursor
import config

bot = telebot.TeleBot(os.getenv("tgbotapi"))


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hi")
    bot.send_location(message.chat.id, 46.4108178, 30.7327385)


@bot.message_handler(commands=['beer'])
def send_beer(message):
    items = DBCursor().receive_products()
    items.sort(key=lambda p: p.profit if p.profit is not None else 0, reverse=True)
    for item in items[:5]:
        bot.send_message(message.chat.id, item)


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    bot.reply_to(message, message.chat.username)


bot.infinity_polling()
