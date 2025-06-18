#!/usr/bin/env python3
import os

import telebot
from SilpoCrawler import SilpoCrawler
from DBCursor import DBCursor
import config
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot("")


@bot.message_handler(commands=['menu'])
def start_handler(message):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("Пивас", callback_data="beer"),
        InlineKeyboardButton("Сыр", callback_data="cheese")
    )
    bot.send_message(message.chat.id, "Выберите товары:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "beer":
        bot.answer_callback_query(call.id)

        bot.send_message(call.message.chat.id, "")
    elif call.data == "cheese":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, f"Твой Telegram ID: {call.from_user.id}")

'''
@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Start"), KeyboardButton("Help"))
    bot.send_message(message.chat.id, "Choose:", reply_markup=markup)
'''

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hi")
    bot.send_location(message.chat.id, 46.4108178, 30.7327385)


@bot.message_handler(commands=['beer'])
def send_beer(message):
    items = DBCursor().receive_products("https://shop.silpo.ua/category/kovbasni-vyroby-i-m-iasni-delikatesy-4731"
                                        "?page=1")
    items.sort(key=lambda p: p.profit if p.profit is not None else 0, reverse=True)
    for item in items[:5]:
        bot.send_message(message.chat.id, item)



@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    bot.reply_to(message, message.chat.username)


bot.infinity_polling()
