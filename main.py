#!/usr/bin/python3

import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from os.path import exists
from os import _exit
file_exists = exists('api_key.txt')
if not file_exists:
    print("Error: api_key.txt file does not exist. Create it and put your telegram bot api there")
    _exit(1)
api_key_file = open('api_key.txt', 'r')
api_key = api_key_file.readline().rstrip()
if api_key=="":
    print("Error: could not read api key from api_key.txt")
    _exit(1)

# Обращаемся к боту через его api
gostbot = telebot.TeleBot(api_key)

# Импортируем два файла для включения функций бота  
import handlers, callbacks

# Запускаем бесконечную работу бота
gostbot.infinity_polling()
