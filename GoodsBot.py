#!/usr/bin/env python3

import telebot
from GoodsParser import GoodsParser
import config

bot = telebot.TeleBot(config.BOT_TOKEN)

parser = GoodsParser()


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hi")
    bot.send_location(message.chat.id, 46.4108178, 30.7327385)


@bot.message_handler(commands=['beer'])
def send_beer(message):
    parser.retrieve("beer_parse.json")
    for good in parser.products_dict.items():
        bot.send_message(message.chat.id, str(good))


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    bot.reply_to(message, message.chat.username)


bot.infinity_polling()