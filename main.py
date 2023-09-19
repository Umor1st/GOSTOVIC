import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# Обращаемся к боту через его api
gostbot = telebot.TeleBot("API_KEY")

# Импортируем два файла для включения функций бота  
import handlers, callbacks

# Запускаем бесконечную работу бота
gostbot.infinity_polling()