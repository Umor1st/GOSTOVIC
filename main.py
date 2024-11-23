#!/usr/bin/python3

import telebot
import sys
sys.stdout.reconfigure(encoding='utf-8')
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from os.path import exists
from os import _exit

file_exists = exists('api_key.txt')

if not file_exists:
    print("Error: api_key.txt file does not exist. Create it and put your telegram bot api there")
    _exit(1)

api_key_file = open('api_key.txt', 'r')
api_key = api_key_file.readline().rstrip()

if api_key == "":
    print("Error: could not read api key from api_key.txt")
    _exit(1)

# Обращаемся к боту через его api

gostbot = telebot.TeleBot(api_key)

# Импортируем callbacks и buttons

from buttons import *
from callbacks import *

# Словарь для добавления списков пользователей для состовляющих ГОСТ-ов (Например: имя книги, год издания и тд.)

gost_dict = dict()

#Итак здесь будут списки городов исключений(чтобы не писать по нескольку раз)

SPB = ["Санкт-Петербург", "Санкт Петербург", "cанкт-петербург","Питер", "питер", "СПБ", "CПб", "спб"]
MSC = ["Москва", "Москоу", "москва"]

# Функция для добавления списка для пользователя в "базу данных"

def add_user_in_db(id_chat, gost_dict):
    if id_chat not in gost_dict:
        gost_dict[id_chat] = []

# Handler - штука, которая исполняет по команде определённые действия
# В фильтрах можно указать определенную команду после которой будут выполняться действия


# Handler для вывода главного меню
@gostbot.message_handler(commands=["start"])
def main(message):
    id_chat = message.chat.id
    print(id_chat)
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    print(username)
    gostbot.send_message(id_chat, f"Привет, {username.first_name}, я продвинутый инструмент для гостов - GOSTOVIC")
    # Бот может отсылать сообщения с встроенной клавиатурой reply_markup 
    # Которая может быть как inline, так и обычной
    # Здесь сообщению передается значение функции markup_main, которая возращает inline клавиатуру
    gostbot.send_message(id_chat, "Выберите одну из категорий:", reply_markup=markup_main())

# УЧЕНИКИ

# 2003 год 
# Handler для работы с журналом ГОСТ-а 2003 года
@gostbot.message_handler(commands=["Journal2003"])
def jour_avtors_2003(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите авторов\nОбразец: Иванов А.А., Петров А.А.")
    gostbot.register_next_step_handler(send, jour_tema_2003)

def jour_tema_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите тему")
    gostbot.register_next_step_handler(send, jour_name_2003)

def jour_name_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название журнала")
    gostbot.register_next_step_handler(send, jour_year_2003)

def jour_year_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год издания (только цифра)")
    gostbot.register_next_step_handler(send, jour_nomer_2003)

def jour_nomer_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите номер журнала (только цифра)")
    gostbot.register_next_step_handler(send, jour_pages_2003)

def jour_pages_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите страницы журнала (через тире)\nОбразец: 65-70")
    gostbot.register_next_step_handler(send, journal_result_2003)

def journal_result_2003(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    jour_avtors = [""]*3
    counter = 0
    try:
        print(gost_dict[id_chat][0].split(",")[:3])
        for i in gost_dict[id_chat][0].split(",")[:3]:
            jour_avtors[counter] = i
            counter += 1
        print(jour_avtors)
        tema = (gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]).replace("\n"," ")
        journal_name = gost_dict[id_chat][2][0].capitalize() + gost_dict[id_chat][2][1:]
        year = gost_dict[id_chat][3].capitalize()
        nomer = gost_dict[id_chat][4]
        pages = gost_dict[id_chat][5]
        a1_f = jour_avtors[0].strip()[:jour_avtors[0].strip().find(" ")].capitalize()
        a1_name = jour_avtors[0].strip()[jour_avtors[0].strip().find(" ")+1:]
        a1_name = a1_name[0].capitalize() + a1_name[1] + a1_name[2].capitalize() + a1_name[3]
        if jour_avtors.count('') == 0:
            result = f"""{a1_f}, {a1_name} {tema} [Текст] / {a1_name} {a1_f} и др. // {journal_name}. — {year}. — № {nomer}. — C. {pages}."""
        elif jour_avtors.count('') == 1:
            a2 = jour_avtors[1].strip()[jour_avtors[1].strip().index(" ")+1:] + " " + jour_avtors[1].strip()[:jour_avtors[1].strip().index(" ")]
            result = f"""{a1_f}, {a1_name} {tema} [Текст] / {a1_name} {a1_f}, {a2} // {journal_name}. — {year}. — № {nomer}. — C. {pages}."""
        else:
            result = f"""{a1_f}, {a1_name} {tema} [Текст] / {a1_name} {a1_f} // {journal_name}. — {year}. — № {nomer}. — C. {pages}."""

        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Journal2003", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)
        

@gostbot.message_handler(commands=["BookNormal2003"])
def book_normal_avtors_2003(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите авторов\nОбразец: Иванов А.А., Петров А.А.")
    gostbot.register_next_step_handler(send, book_normal_name_2003)

def book_normal_name_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название")
    gostbot.register_next_step_handler(send, book_normal_add_inf_2003)

def book_normal_add_inf_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. сведения, относящиеся к названию (заглавию) если они есть\nЕсли их нет введите: . \nОбразец: учебник")
    gostbot.register_next_step_handler(send, book_normal_responsibility_2003)

def book_normal_responsibility_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. сведения об ответственности если они есть\nЕсли их нет введите: . \nОбразец: отв. ред. П. П. Петров ; пер. с англ. С. С. Сидорова")
    gostbot.register_next_step_handler(send, book_normal_reissues_2003)

def book_normal_reissues_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. информацию о издании, исправлениях и дополнениях\nЕсли ничего такого нет напишите: . \nОбразец: 6-е изд., испр. и доп.")
    gostbot.register_next_step_handler(send, book_normal_city_2003)

def book_normal_city_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, book_normal_publish_2003)

def book_normal_publish_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название издательства")
    gostbot.register_next_step_handler(send, book_normal_year_2003)

def book_normal_year_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name} введите год издания (только цифра)")
    gostbot.register_next_step_handler(send, book_normal_pages_2003)

def book_normal_pages_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество страниц\nОбразец: 65")
    gostbot.register_next_step_handler(send, book_normal_result_2003)

def book_normal_result_2003(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    book_avtors = [""]*5
    counter = 0
    try:
        print(gost_dict[id_chat][0].split(",")[:5])
        for i in gost_dict[id_chat][0].split(",")[:5]:
            book_avtors[counter] = i
            counter += 1
        print(book_avtors)
        name = gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]
        if gost_dict[id_chat][2] != ".":
            add_inf = " : " + gost_dict[id_chat][2]
        else:
            add_inf = ""
        if gost_dict[id_chat][3] != ".":
            responsibility = " / " + gost_dict[id_chat][3]
        else:
            responsibility = ""
        if gost_dict[id_chat][4] != ".":
            reissues = " " + gost_dict[id_chat][4] + " — "
        else:
            reissues = ""
        if gost_dict[id_chat][5].lower() in SPB:
            city = "СПб."
        elif gost_dict[id_chat][5].lower() in MSC:
            city = "М."
        else:
            city = gost_dict[id_chat][5][0].capitalize() + gost_dict[id_chat][5][1:]
        publish = gost_dict[id_chat][6][0].capitalize() + gost_dict[id_chat][6][1:]
        year = gost_dict[id_chat][7]
        pages = gost_dict[id_chat][8]
        a1_f = book_avtors[0].strip()[:book_avtors[0].strip().find(" ")]
        a1_name = book_avtors[0].strip()[book_avtors[0].strip().find(" ")+1:]
        if book_avtors.count('') == 0:
            a2 = book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:] + " " + book_avtors[1].strip()[:book_avtors[1].strip().index(" ")]
            a3 = book_avtors[2].strip()[book_avtors[2].strip().index(" ")+1:] + " " + book_avtors[2].strip()[:book_avtors[1].strip().index(" ")]
            result = f"""{name} [Текст]{add_inf} / {a1_name} {a1_f}, {a2}, {a3} и др.{responsibility} —{reissues} {city} : {publish}, {year}. — {pages} c."""
        elif book_avtors.count('') == 1:
            a2 = book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:] + " " + book_avtors[1].strip()[:book_avtors[1].strip().index(" ")]
            a3 = book_avtors[2].strip()[book_avtors[2].strip().index(" ")+1:] + " " + book_avtors[2].strip()[:book_avtors[1].strip().index(" ")]
            a4 = book_avtors[3].strip()[book_avtors[3].strip().index(" ")+1:] + " " + book_avtors[3].strip()[:book_avtors[1].strip().index(" ")]
            result = f"""{name} [Текст]{add_inf} / {a1_name} {a1_f}, {a2}, {a3}, {a4}{responsibility} —{reissues} {city} : {publish}, {year}. — {pages} c."""
        elif book_avtors.count('') == 2:
            a2 = book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:] + " " + book_avtors[1].strip()[:book_avtors[1].strip().index(" ")]
            a3 = book_avtors[2].strip()[book_avtors[2].strip().index(" ")+1:] + " " + book_avtors[2].strip()[:book_avtors[1].strip().index(" ")]
            result = f"""{a1_f}, {a1_name} {name} [Текст]{add_inf} / {a1_name} {a1_f}, {a2}, {a3}{responsibility} —{reissues} {city} : {publish}, {year}. — {pages} c."""
        elif book_avtors.count('') == 3:
            a2 = book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:] + " " + book_avtors[1].strip()[:book_avtors[1].strip().index(" ")]
            result = f"""{a1_f}, {a1_name} {name} [Текст]{add_inf} / {a1_name} {a1_f}, {a2}{responsibility} —{reissues} {city} : {publish}, {year}. — {pages} c."""
        else:
            result = f"""{a1_f}, {a1_name} {name} [Текст]{add_inf} / {a1_name} {a1_f}{responsibility} —{reissues} {city} : {publish}, {year}. — {pages} c."""


        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/BookNormal2003", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["Ethernet2003"])
def name_of_eth_2003(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название ресурса")
    gostbot.register_next_step_handler(send, url_2003)

def url_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите URL")
    gostbot.register_next_step_handler(send, date_2003)

def date_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите время обращения\nОбразец: 22.01.2023")
    gostbot.register_next_step_handler(send, result_eth_2003)

def result_eth_2003(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    try:
        name = gost_dict[id_chat][0][0].upper() + gost_dict[id_chat][0][1:]
        result = f"""{name} [Электронный ресурс]. — URL: {gost_dict[id_chat][1]} (Дата обращения: {gost_dict[id_chat][2]})."""
        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Ethernet2003", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["Dissertation2003"])
def dissert_avtor_2003(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите автора диссертации\nОбразец: Иванов Александр Александорович")
    gostbot.register_next_step_handler(send, dissert_name_2003)

def dissert_name_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название диссертации")
    gostbot.register_next_step_handler(send, dissert_rang_2003)

def dissert_rang_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите ученую степень автора диссертации Образец: канд. ист. наук")
    gostbot.register_next_step_handler(send, dissert_shifr_vac_2003)

def dissert_shifr_vac_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите шифр ВАК если он есть, в противном случае вводите: . \nОбразец: 13.00.05")
    gostbot.register_next_step_handler(send, dissert_city_2003)

def dissert_city_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, dissert_year_2003)

def dissert_year_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год защиты (Просто цифра)")
    gostbot.register_next_step_handler(send, dissert_pages_2003)

def dissert_pages_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество страниц\nОбразец: 65")
    gostbot.register_next_step_handler(send, dissert_result_2003)

def dissert_result_2003(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    try:
        dissert_avtor = gost_dict[id_chat][0].split()
        print(dissert_avtor)
        dissert_name = (gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]).replace("\n"," ")
        dissert_rang = gost_dict[id_chat][2]
        if gost_dict[id_chat][3] != ".":
            dissert_shifr_vac = " : " + gost_dict[id_chat][3]
        else:
            dissert_shifr_vac = ""
        if gost_dict[id_chat][4].lower() in SPB:
            dissert_city = "СПб."
        elif gost_dict[id_chat][4].lower() in MSC:
            dissert_city = "М."
        else:
            dissert_city = gost_dict[id_chat][4][0].capitalize() + gost_dict[id_chat][4][1:]
        dissert_year = gost_dict[id_chat][5]
        dissert_pages = gost_dict[id_chat][6] 
        result = f"""{dissert_avtor[0]}, {dissert_avtor[1][0]}.{dissert_avtor[2][0]}. {dissert_name} [Текст] : дис. ... {dissert_rang}{dissert_shifr_vac} / {dissert_avtor[0]} {dissert_avtor[1]} {dissert_avtor[2]}. — {dissert_city}, {dissert_year}. — {dissert_pages} с."""

        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Dissertation2003", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["Aftoreferat2003"])
def aftoref_avtor_2003(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите автора автореферата\nОбразец: Иванов Александр Александорович")
    gostbot.register_next_step_handler(send, aftoref_name_2003)

def aftoref_name_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название автореферата")
    gostbot.register_next_step_handler(send, aftoref_rang_2003)

def aftoref_rang_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите ученую степень автора автореферата Образец: канд. ист. наук")
    gostbot.register_next_step_handler(send, aftoref_shifr_vac_2003)

def aftoref_shifr_vac_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите шифр ВАК если он есть, в противном случае вводите: . \nОбразец: 13.00.05")
    gostbot.register_next_step_handler(send, aftoref_city_2003)

def aftoref_city_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, aftoref_year_2003)

def aftoref_year_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год защиты (Просто цифра)")
    gostbot.register_next_step_handler(send, aftoref_pages_2003)

def aftoref_pages_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество страниц\nОбразец: 65")
    gostbot.register_next_step_handler(send, aftoref_result_2003)

def aftoref_result_2003(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    try:
        aftoref_avtor = gost_dict[id_chat][0].split()
        aftoref_name = (gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]).replace("\n"," ")
        aftoref_rang = gost_dict[id_chat][2]
        if gost_dict[id_chat][3] != ".":
            aftoref_shifr_vac = " : " + gost_dict[id_chat][3]
        else:
            aftoref_shifr_vac = ""
        if gost_dict[id_chat][4].lower() in SPB:
            aftoref_city = "СПб."
        elif gost_dict[id_chat][4].lower() in MSC:
            aftoref_city = "М."
        else:
            aftoref_city = gost_dict[id_chat][4][0].capitalize() + gost_dict[id_chat][4][1:]
        aftoref_year = gost_dict[id_chat][5]
        aftoref_pages = gost_dict[id_chat][6] 
        result = f"""{aftoref_avtor[0]}, {aftoref_avtor[1][0]}.{aftoref_avtor[2][0]}. {aftoref_name} [Текст] : афтореф. дис. ... {aftoref_rang}{aftoref_shifr_vac} / {aftoref_avtor[0]} {aftoref_avtor[1]} {aftoref_avtor[2]}. — {aftoref_city}, {aftoref_year}. — {aftoref_pages} c."""

        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Aftoreferat2003", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)


@gostbot.message_handler(commands=["Zakon2003Document"])
def zakon_document_name_2003(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите полное название документа\nОбразец: Конституция РФ")
    gostbot.register_next_step_handler(send, zakon_document_izd_date_2003)

def zakon_document_izd_date_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите дату от которой был издан закон\nОбразец: 18.04.2007")
    gostbot.register_next_step_handler(send, zakon_document_num_fz_2003)

def zakon_document_num_fz_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите номер ФЗ (только цифра)")
    gostbot.register_next_step_handler(send, zakon_document_redact_date_2003)

def zakon_document_redact_date_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите дату редактирования\nОбразец: 27.12.2018")
    gostbot.register_next_step_handler(send, zakon_document_who_accept_2003)

def zakon_document_who_accept_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название гос. органа, принявшего/учредившего закон\nОбразец: СЗ РФ")
    gostbot.register_next_step_handler(send, zakon_document_pechat_date_2003)

def zakon_document_pechat_date_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите дату печати Образец: 09.05.2011")
    gostbot.register_next_step_handler(send, zakon_document_num_2003)

def zakon_document_num_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите номер издания")
    gostbot.register_next_step_handler(send, zakon_document_statya_2003)

def zakon_document_statya_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите статью")
    gostbot.register_next_step_handler(send, zakon_document_result_2003)

def zakon_document_result_2003(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    try:
        name = (gost_dict[id_chat][0][0].capitalize() + gost_dict[id_chat][0][1:]).replace("\n"," ")
        izd_date = gost_dict[id_chat][1] 
        num_fz = gost_dict[id_chat][2] 
        redact_date = gost_dict[id_chat][3] 
        who_accept = gost_dict[id_chat][4][0].capitalize() + gost_dict[id_chat][4][1:]
        pechat_date = gost_dict[id_chat][5]
        num = gost_dict[id_chat][6]
        statya = gost_dict[id_chat][7]
        result = f"{name} от {izd_date} № {num_fz}-ФЗ (ред. от {redact_date}) // {who_accept}. — {pechat_date} — № {num} — Ст. {statya}."
        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Zakon2003Document", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["Zakon2003Federation"])
def zakon_federation_name_2003(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите полное название закона (без кавычек!)\nОбразец: О лицензировании отдельных видов деятельности")
    gostbot.register_next_step_handler(send, zakon_federation_izd_date_2003)

def zakon_federation_izd_date_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите дату от которой был издан закон\nОбразец: 18.04.2007")
    gostbot.register_next_step_handler(send, zakon_federation_num_fz_2003)

def zakon_federation_num_fz_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите номер ФЗ (только цифра)")
    gostbot.register_next_step_handler(send, zakon_federation_redact_date_2003)

def zakon_federation_redact_date_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите дату редактирования\nОбразец: 27.12.2018")
    gostbot.register_next_step_handler(send, zakon_federation_who_accept_2003)

def zakon_federation_who_accept_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название гос. органа, принявшего/учредившего закон\n Образуц: СЗ РФ")
    gostbot.register_next_step_handler(send, zakon_federation_pechat_date_2003)

def zakon_federation_pechat_date_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите дату печати Образец: 09.05.2011")
    gostbot.register_next_step_handler(send, zakon_federation_num_2003)

def zakon_federation_num_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите номер издания")
    gostbot.register_next_step_handler(send, zakon_federation_statya_2003)

def zakon_federation_statya_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите статью")
    gostbot.register_next_step_handler(send, zakon_federation_result_2003)

def zakon_federation_result_2003(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    try:
        name = (gost_dict[id_chat][0][0].capitalize() + gost_dict[id_chat][0][1:]).replace("\n"," ")
        izd_date = gost_dict[id_chat][1] 
        num_fz = gost_dict[id_chat][2] 
        redact_date = gost_dict[id_chat][3] 
        who_accept = gost_dict[id_chat][4][0].capitalize() + gost_dict[id_chat][4][1:]
        pechat_date = gost_dict[id_chat][5]
        num = gost_dict[id_chat][6]
        statya = gost_dict[id_chat][7]
        result = f"Федеральный закон от {izd_date} № {num_fz}-ФЗ (ред. от {redact_date}) «{name}» // {who_accept}. — {pechat_date} — № {num} — Ст. {statya}."
        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Zakon2003Federation", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["Zakon2003FederationInternet"])
def zakon_federation_internet_name_2003(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите полное название закона (без кавычек)\nОбразец: О лицензировании отдельных видов деятельности")
    gostbot.register_next_step_handler(send, zakon_federation_internet_izd_date_2003)

def zakon_federation_internet_izd_date_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите дату от которой был издан закон\nОбразец: 18.04.2007")
    gostbot.register_next_step_handler(send, zakon_federation_internet_num_fz_2003)

def zakon_federation_internet_num_fz_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите номер ФЗ (Просто цифра)")
    gostbot.register_next_step_handler(send, zakon_federation_internet_redact_date_2003)

def zakon_federation_internet_redact_date_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите дату редактирования\nОбразец: 27.12.2018")
    gostbot.register_next_step_handler(send, zakon_federation_internet_url_2003)

def zakon_federation_internet_url_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите URL сайта на котором расположен закон")
    gostbot.register_next_step_handler(send, zakon_federation_internet_result_2003)

def zakon_federation_internet_result_2003(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    name = (gost_dict[id_chat][0][0].capitalize() + gost_dict[id_chat][0][1:]).replace("\n"," ")
    izd_date = gost_dict[id_chat][1] 
    num_fz = gost_dict[id_chat][2] 
    redact_date = gost_dict[id_chat][3] 
    url = gost_dict[id_chat][4]
    result = f"Федеральный закон от {izd_date} № {num_fz}-ФЗ (ред. от {redact_date}) «{name}» [Электронный ресурс]. — URL: {url}"
    gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
    gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Zakon2003FederationInternet", parse_mode="MarkdownV2", reply_markup=back())
    print(result)
    gost_dict[id_chat].clear()


@gostbot.message_handler(commands=["Zakon2003Postanovlenie"])
def zakon_postan_name_2003(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите полное название постановления (без кавычек)")
    gostbot.register_next_step_handler(send, zakon_postan_who_postan_2003)

def zakon_postan_who_postan_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите чьё именно постановиление\nОбразец: Правительства РФ")
    gostbot.register_next_step_handler(send, zakon_postan_izd_date_2003)

def zakon_postan_izd_date_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите дату от которой был издан закон\nОбразец: 18.04.2007")
    gostbot.register_next_step_handler(send, zakon_postan_num_postan_2003)

def zakon_postan_num_postan_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите номер постановления (только цифра)")
    gostbot.register_next_step_handler(send, zakon_postan_redact_date_2003)

def zakon_postan_redact_date_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите дату редактирования\nОбразец: 27.12.2018")
    gostbot.register_next_step_handler(send, zakon_postan_who_accept_2003)

def zakon_postan_who_accept_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название Гос. органа, принявшего/учредившего закон\nОбразец: ФЗ РФ")
    gostbot.register_next_step_handler(send, zakon_postan_pechat_date_2003)

def zakon_postan_pechat_date_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите дату печати Образец: 09.05.2011")
    gostbot.register_next_step_handler(send, zakon_postan_num_2003)

def zakon_postan_num_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите номер издания")
    gostbot.register_next_step_handler(send, zakon_postan_statya_2003)

def zakon_postan_statya_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите статью")
    gostbot.register_next_step_handler(send, zakon_postan_result_2003)

def zakon_postan_result_2003(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    try:
        name = (gost_dict[id_chat][0][0].capitalize() + gost_dict[id_chat][0][1:]).replace("\n"," ")
        who_postan = gost_dict[id_chat][1] 
        izd_date = gost_dict[id_chat][2] 
        num_postan = gost_dict[id_chat][3] 
        redact_date = gost_dict[id_chat][4] 
        who_accept = gost_dict[id_chat][5][0].capitalize() + gost_dict[id_chat][5][1:]
        pechat_date = gost_dict[id_chat][6]
        num = gost_dict[id_chat][7]
        statya = gost_dict[id_chat][8]
        result = f"Постановление {who_postan} от {izd_date} № {num_postan} (ред. от {redact_date}) «{name}» // {who_accept}. — {pechat_date} — № {num} — Ст. {statya}."
        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Zakon2003Postanovlenie", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)



@gostbot.message_handler(commands=["Mnogotomnik2003toms"])
def book_mnogotomnic_toms_avtors_2003(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите авторов\nОбразец: Иванов А.А., Петров А.А.")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_name_2003)

def book_mnogotomnic_toms_name_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название моготомного издания")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_count_toms_2003)

def book_mnogotomnic_toms_count_toms_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество томов всего (укажите только цифру)")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_add_inf_tom_2003)

def book_mnogotomnic_toms_add_inf_tom_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите информацию о номере вашего тома (укажите только цифру)")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_city_2003)

def book_mnogotomnic_toms_city_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_publish_2003)

def book_mnogotomnic_toms_publish_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название издательства")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_year_2003)

def book_mnogotomnic_toms_year_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год издания (только цифра)")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_result_2003)

def book_mnogotomnic_toms_result_2003(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    book_mnogotomnic_avtors = [""]*5
    counter = 0
    try:
        print(gost_dict[id_chat][0].split(",")[:5])
        for i in gost_dict[id_chat][0].split(",")[:5]:
            book_mnogotomnic_avtors[counter] = i
            counter += 1
        print(book_mnogotomnic_avtors)
        name = gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]
        count_toms = gost_dict[id_chat][2]
        tom_num = gost_dict[id_chat][3] 
        if gost_dict[id_chat][4].lower() in SPB:
            city = "СПб."
        elif gost_dict[id_chat][4].lower() in MSC:
            city = "М."
        else:
            city = gost_dict[id_chat][4][0].capitalize() + gost_dict[id_chat][4][1:]
        publish = gost_dict[id_chat][5][0].capitalize() + gost_dict[id_chat][5][1:]
        year = gost_dict[id_chat][6]
        a1_f = book_mnogotomnic_avtors[0].strip()[:book_mnogotomnic_avtors[0].strip().find(" ")]
        a1_name = book_mnogotomnic_avtors[0].strip()[book_mnogotomnic_avtors[0].strip().find(" ")+1:]
        if book_mnogotomnic_avtors.count('') == 0:
            a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            a3 = book_mnogotomnic_avtors[2].strip()[book_mnogotomnic_avtors[2].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[2].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            result = f"""{name} [Текст] : в {count_toms} / {a1_name} {a1_f}, {a2}, {a3} и др. — {city} : {publish}, {year}. — {tom_num} т."""
        elif book_mnogotomnic_avtors.count('') == 1:
            a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            a3 = book_mnogotomnic_avtors[2].strip()[book_mnogotomnic_avtors[2].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[2].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            a4 = book_mnogotomnic_avtors[3].strip()[book_mnogotomnic_avtors[3].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[3].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            result = f"""{name} [Текст] : в {count_toms} т. / {a1_name} {a1_f}, {a2}, {a3}, {a4}. — {city} : {publish}, {year}. — {tom_num} т."""
        elif book_mnogotomnic_avtors.count('') == 2:
            a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            a3 = book_mnogotomnic_avtors[2].strip()[book_mnogotomnic_avtors[2].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[2].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            result = f"""{a1_f}, {a1_name} {name} [Текст] : в {count_toms} т. / {a1_name} {a1_f}, {a2}, {a3}. — {city} : {publish}, {year}. — {tom_num} т."""
        elif book_mnogotomnic_avtors.count('') == 3:
            a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            result = f"""{a1_f}, {a1_name} {name} [Текст] : в {count_toms} т. / {a1_name} {a1_f}, {a2}. — {city} : {publish}, {year}. — {tom_num} т."""
        else:
            result = f"""{a1_f}, {a1_name} {name} [Текст] : в {count_toms} т. / {a1_name} {a1_f}. — {city} : {publish}, {year}. — {tom_num} т."""


        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Mnogotomnik2003toms", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["Mnogotomnik2003chapters"])
def book_mnogotomnic_chapters_avtors_2003(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите авторов\nОбразец: Иванов А.А., Петров А.А.")
    gostbot.register_next_step_handler(send, book_mnogotomnic_chapters_name_2003)

def book_mnogotomnic_chapters_name_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название")
    gostbot.register_next_step_handler(send, book_mnogotomnic_chapters_count_chapters_2003)

def book_mnogotomnic_chapters_count_chapters_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество частей всего (укажите только цифру)")
    gostbot.register_next_step_handler(send, book_mnogotomnic_chapters_inf_chapter_2003)

def book_mnogotomnic_chapters_inf_chapter_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите номер вашей части (укажите только цифру)")
    gostbot.register_next_step_handler(send, book_mnogotomnic_chapters_inf_chapter_name_2003)

def book_mnogotomnic_chapters_inf_chapter_name_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название части")
    gostbot.register_next_step_handler(send, book_mnogotomnic_chapters_city_2003)

def book_mnogotomnic_chapters_city_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, book_mnogotomnic_chapters_publish_2003)

def book_mnogotomnic_chapters_publish_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название издательства")
    gostbot.register_next_step_handler(send, book_mnogotomnic_chapters_year_2003)

def book_mnogotomnic_chapters_year_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год издания (только цифра)")
    gostbot.register_next_step_handler(send, book_mnogotomnic_chapters_pages_2003)

def book_mnogotomnic_chapters_pages_2003(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество страниц (только цифра)")
    gostbot.register_next_step_handler(send, book_mnogotomnic_chapters_result_2003)

def book_mnogotomnic_chapters_result_2003(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    book_mnogotomnic_avtors = [""]*5
    counter = 0
    print(gost_dict[id_chat][0].split(",")[:5])
    for i in gost_dict[id_chat][0].split(",")[:5]:
        book_mnogotomnic_avtors[counter] = i
        counter += 1
    print(book_mnogotomnic_avtors)
    name = gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]
    count_chapters = gost_dict[id_chat][2]
    chapter_num = gost_dict[id_chat][3]
    chapter_name = gost_dict[id_chat][4][0].capitalize() + gost_dict[id_chat][4][1:]
    if gost_dict[id_chat][5].lower() in SPB:
        city = "СПб."
    elif gost_dict[id_chat][5].lower() in MSC:
        city = "М."
    else:
        city = gost_dict[id_chat][5][0].capitalize() + gost_dict[id_chat][5][1:]
    publish = gost_dict[id_chat][6][0].capitalize() + gost_dict[id_chat][6][1:]
    year = gost_dict[id_chat][7]
    mnogotomnic_pages = gost_dict[id_chat][8]
    a1_f = book_mnogotomnic_avtors[0].strip()[:book_mnogotomnic_avtors[0].strip().find(" ")]
    a1_name = book_mnogotomnic_avtors[0].strip()[book_mnogotomnic_avtors[0].strip().find(" ")+1:]
    if book_mnogotomnic_avtors.count('') == 0:
        a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
        a3 = book_mnogotomnic_avtors[2].strip()[book_mnogotomnic_avtors[2].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[2].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
        result = f"""{name} [Текст] : В {count_chapters} ч. Ч. {chapter_num} {chapter_name} / {a1_name} {a1_f}, {a2}, {a3} и др. — {city} : {publish}, {year}. — {mnogotomnic_pages} c."""
    elif book_mnogotomnic_avtors.count('') == 1:
        a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
        a3 = book_mnogotomnic_avtors[2].strip()[book_mnogotomnic_avtors[2].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[2].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
        a4 = book_mnogotomnic_avtors[3].strip()[book_mnogotomnic_avtors[3].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[3].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
        result = f"""{name} [Текст] : В {count_chapters} ч. Ч. {chapter_num} {chapter_name} / {a1_name} {a1_f}, {a2}, {a3}, {a4}. — {city} : {publish}, {year}. — {mnogotomnic_pages} c."""
    elif book_mnogotomnic_avtors.count('') == 2:
        a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
        a3 = book_mnogotomnic_avtors[2].strip()[book_mnogotomnic_avtors[2].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[2].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
        result = f"""{a1_f}, {a1_name} {name} [Текст] : В {count_chapters} ч. Ч. {chapter_num} {chapter_name} / {a1_name} {a1_f}, {a2}, {a3}. — {city} : {publish}, {year}. — {mnogotomnic_pages} c."""
    elif book_mnogotomnic_avtors.count('') == 3:
        a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
        result = f"""{a1_f}, {a1_name} {name} [Текст] : В {count_chapters} ч. Ч. {chapter_num} {chapter_name} / {a1_name} {a1_f}, {a2}. — {city} : {publish}, {year}. — {mnogotomnic_pages} c."""
    else:
        result = f"""{a1_f}, {a1_name} {name} [Текст] : В {count_chapters} ч. Ч. {chapter_num} {chapter_name} / {a1_name} {a1_f}. — {city} : {publish}, {year}. — {mnogotomnic_pages} c."""


    gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
    gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Mnogotomnik2003chapters", parse_mode="MarkdownV2", reply_markup=back())
    print(result)
    gost_dict[id_chat].clear()

# 2008 год 
# Handler для работы с журналом ГОСТ-а 2008 года
@gostbot.message_handler(commands=["Journal2008"])
def jour_avtors_2008(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите авторов\nОбразец: Иванов А.А., Петров А.А.")
    gostbot.register_next_step_handler(send, jour_tema_2008)

def jour_tema_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите тему")
    gostbot.register_next_step_handler(send, jour_name_2008)

def jour_name_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название журнала")
    gostbot.register_next_step_handler(send, jour_year_2008)

def jour_year_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год издания (только цифра)")
    gostbot.register_next_step_handler(send, jour_nomer_2008)

def jour_nomer_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите номер журнала (только цифра)")
    gostbot.register_next_step_handler(send, jour_pages_2008)

def jour_pages_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите страницы журнала (через тире)\nОбразец: 65-70")
    gostbot.register_next_step_handler(send, journal_result_2008)

def journal_result_2008(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    jour_avtors = [""]*4
    counter = 0
    try:
        print(gost_dict[id_chat][0].split(",")[:4])
        for i in gost_dict[id_chat][0].split(",")[:4]:
            jour_avtors[counter] = i
            counter += 1
        print(jour_avtors)
        tema = (gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]).replace("\n"," ")
        journal_name = gost_dict[id_chat][2][0].capitalize() + gost_dict[id_chat][2][1:]
        year = gost_dict[id_chat][3]
        nomer = gost_dict[id_chat][4]
        pages = gost_dict[id_chat][5]
        a1_f = jour_avtors[0].strip()[:jour_avtors[0].strip().find(" ")]
        a1_name = jour_avtors[0].strip()[jour_avtors[0].strip().find(" ")+1:]
        if jour_avtors.count('') == 0:
            result = f"""{tema} / {a1_name} {a1_f} и [др.] // {journal_name}. {year}. № {nomer}. C. {pages}."""
        elif jour_avtors.count('') == 1:
            a2 = jour_avtors[1].strip()[:jour_avtors[1].strip().index(" ")] + " " + jour_avtors[1].strip()[jour_avtors[1].strip().index(" ")+1:]
            a3 = jour_avtors[2].strip()[:jour_avtors[2].strip().index(" ")] + " " + jour_avtors[2].strip()[jour_avtors[2].strip().index(" ")+1:]
            result = f"""{a1_f} {a1_name}, {a2}, {a3} {tema} // {journal_name}. {year}. № {nomer}. C. {pages}."""    
        elif jour_avtors.count('') == 2:
            a2 = jour_avtors[1].strip()[:jour_avtors[1].strip().index(" ")] + " " + jour_avtors[1].strip()[jour_avtors[1].strip().index(" ")+1:]
            result = f"""{a1_f} {a1_name}, {a2} {tema} // {journal_name}. {year}. № {nomer}. C. {pages}."""
        else:
            result = f"""{a1_f} {a1_name} {tema} // {journal_name}. {year}. № {nomer}. C. {pages}."""

        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Journal2008", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["BookNormal2008"])
def book_normal_avtors_2008(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите автора(ов), если их нет введите: . \nОбразец: Иванов А.А., Петров А.А.")
    gostbot.register_next_step_handler(send, book_normal_name_2008)

def book_normal_name_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название")
    gostbot.register_next_step_handler(send, book_normal_add_inf_2008)

def book_normal_add_inf_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. сведения, относящиеся к названию (заглавию) если они есть\nЕсли их нет введите: . \nОбразец: учебник")
    gostbot.register_next_step_handler(send, book_normal_responsibility_2008)

def book_normal_responsibility_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. сведения об ответственности если они есть\nЕсли их нет введите: . \nОбразец: отв. ред. П. П. Петров ; пер. с англ. С. С. Сидорова")
    gostbot.register_next_step_handler(send, book_normal_reissues_2008)

def book_normal_reissues_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. информацию о издании, исправлениях и дополнениях\nЕсли ничего такого нет напишите: . \nОбразец: 6-е изд., испр. и доп.")
    gostbot.register_next_step_handler(send, book_normal_city_2008)

def book_normal_city_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, book_normal_publish_2008)

def book_normal_publish_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название издательства")
    gostbot.register_next_step_handler(send, book_normal_year_2008)

def book_normal_year_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год издания (укажите только цифру)")
    gostbot.register_next_step_handler(send, book_normal_pages_2008)

def book_normal_pages_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество страниц\nОбразец: 65")
    gostbot.register_next_step_handler(send, book_normal_result_2008)

def book_normal_result_2008(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    book_avtors = [""]*5
    counter = 0
    try:
        print(gost_dict[id_chat][0].split(",")[:5])
        for i in gost_dict[id_chat][0].split(",")[:5]:
            book_avtors[counter] = i
            counter += 1
        if book_avtors[0] == ".":
            book_avtors[0] == ""
        print(book_avtors)
        name = gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]
        if gost_dict[id_chat][2] != ".":
            add_inf = " : " + gost_dict[id_chat][2] + "."
        else:
            add_inf = ""
        if gost_dict[id_chat][3] != ".":
            responsibility = " / " + gost_dict[id_chat][3] + "."
        else:
            responsibility = ""
        if gost_dict[id_chat][4] != ".":
            reissues = " " + gost_dict[id_chat][4] + " — "
        else:
            reissues = ""
        if gost_dict[id_chat][5].lower() in SPB:
            city = "СПб."
        elif gost_dict[id_chat][5].lower() in MSC:
            city = "М."
        else:
            city = gost_dict[id_chat][5][0].capitalize() + gost_dict[id_chat][5][1:]
        publish = gost_dict[id_chat][6][0].capitalize() + gost_dict[id_chat][6][1:]
        year = gost_dict[id_chat][7]
        pages = gost_dict[id_chat][8]
        a1_f = book_avtors[0].strip()[:book_avtors[0].strip().find(" ")]
        a1_name = book_avtors[0].strip()[book_avtors[0].strip().find(" ")+1:]
        if book_avtors.count('') == 0:
            a2 = book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:] + " " + book_avtors[1].strip()[:book_avtors[1].strip().index(" ")]
            a3 = book_avtors[2].strip()[book_avtors[2].strip().index(" ")+1:] + " " + book_avtors[2].strip()[:book_avtors[2].strip().index(" ")]
            result = f"""{name}{add_inf}{responsibility} / {a1_name} {a1_f} и [др.]. {reissues} {city} : {publish}, {year}. {pages} c."""
        elif book_avtors.count('') == 1:
            a2 = book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:] + " " + book_avtors[1].strip()[:book_avtors[1].strip().index(" ")]
            a3 = book_avtors[2].strip()[book_avtors[2].strip().index(" ")+1:] + " " + book_avtors[2].strip()[:book_avtors[2].strip().index(" ")]
            a4 = book_avtors[3].strip()[book_avtors[3].strip().index(" ")+1:] + " " + book_avtors[3].strip()[:book_avtors[3].strip().index(" ")]
            result = f"""{name}{add_inf}{responsibility} / {a1_name} {a1_f}, {a2}, {a3}, {a4}.{reissues} {city} : {publish}, {year}. {pages} c."""
        elif book_avtors.count('') == 2:
            a2 = book_avtors[1].strip()[:book_avtors[1].strip().index(" ")] + " " + book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:]
            a3 = book_avtors[2].strip()[:book_avtors[2].strip().index(" ")] + " " + book_avtors[2].strip()[book_avtors[2].strip().index(" ")+1:]
            result = f"""{a1_f} {a1_name}, {a2}, {a3} {name}{add_inf}{responsibility}{reissues} {city} : {publish}, {year}. {pages} c."""
        elif book_avtors.count('') == 3:
            a2 = book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:] + " " + book_avtors[1].strip()[:book_avtors[1].strip().index(" ")]
            result = f"""{a1_f} {a1_name}, {a2} {name}{add_inf}{responsibility}{reissues} {city} : {publish}, {year}. {pages} c."""
        elif book_avtors.count('') == 4:
            result = f"""{a1_f} {a1_name} {name}{add_inf}{responsibility}{reissues} {city} : {publish}, {year}. {pages} c."""
        else:
            result = f"""{name}{add_inf}{responsibility}{reissues} {city} : {publish}, {year}. {pages} c."""
    

        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/BookNormal2008", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["BookEBC2008"])
def book_EBC_avtors_2008(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите автора(ов), если их нет введите: . \nОбразец: Иванов А.А., Петров А.А.")
    gostbot.register_next_step_handler(send, book_EBC_name_2008)

def book_EBC_name_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название")
    gostbot.register_next_step_handler(send, book_EBC_add_inf_2008)

def book_EBC_add_inf_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. сведения, относящиеся к названию (заглавию) если они есть\nЕсли их нет введите: . \nОбразец: учебник")
    gostbot.register_next_step_handler(send, book_EBC_responsibility_2008)

def book_EBC_responsibility_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. сведения об ответственности если они есть\nЕсли их нет введите: . \nОбразец: отв. ред. П. П. Петров ; пер. с англ. С. С. Сидорова")
    gostbot.register_next_step_handler(send, book_EBC_reissues_2008)

def book_EBC_reissues_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. информацию о издании, исправлениях и дополнениях\nЕсли ничего такого нет напишите: . \nОбразец: 6-е изд., испр. и доп.")
    gostbot.register_next_step_handler(send, book_EBC_city_2008)

def book_EBC_city_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, book_EBC_publish_2008)

def book_EBC_publish_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название издательства")
    gostbot.register_next_step_handler(send, book_EBC_year_2008)

def book_EBC_year_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год издания (укажите только цифру)")
    gostbot.register_next_step_handler(send, book_EBC_pages_2008)

def book_EBC_pages_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество страниц\nОбразец: 65")
    gostbot.register_next_step_handler(send, book_EBC_URL_2008)

def book_EBC_URL_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите URL")
    gostbot.register_next_step_handler(send, book_EBC_name_of_EBC_2008)

def book_EBC_name_of_EBC_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название EBC, если его нет введите '.' Образец: ЭБС «IPRbooks»")
    gostbot.register_next_step_handler(send, book_EBC_result_2008)

def book_EBC_result_2008(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    book_avtors = [""]*4
    counter = 0
    try:
        print(gost_dict[id_chat][0].split(",")[:4])
        for i in gost_dict[id_chat][0].split(",")[:4]:
            book_avtors[counter] = i
            counter += 1
        if book_avtors[0] == ".":
            book_avtors[0] == ""
        print(book_avtors)
        name = gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]
        if gost_dict[id_chat][2] != ".":
            add_inf = " : " + gost_dict[id_chat][2] + "."
        else:
            add_inf = ""
        if gost_dict[id_chat][3] != ".":
            responsibility = " ; " + gost_dict[id_chat][3] + "."
        else:
            responsibility = ""
        if gost_dict[id_chat][4] != ".":
            reissues = " " + gost_dict[id_chat][4] + " — "
        else:
            reissues = ""
        if gost_dict[id_chat][5].lower() in SPB:
            city = "СПб."
        elif gost_dict[id_chat][5].lower() in MSC:
            city = "М."
        else:
            city = gost_dict[id_chat][5][0].capitalize() + gost_dict[id_chat][5][1:]
        publish = gost_dict[id_chat][6][0].capitalize() + gost_dict[id_chat][6][1:]
        year = gost_dict[id_chat][7]
        if gost_dict[id_chat][8] != ".":
            pages = " " + gost_dict[id_chat][8] + " с."
        else:
            pages = ""
        url = gost_dict[id_chat][9]
        if gost_dict[id_chat][10] != '.':
            name_of_EBC = " " + gost_dict[id_chat][10]
        else:
            name_of_EBC = ""
        a1_f = book_avtors[0].strip()[:book_avtors[0].strip().find(" ")]
        a1_name = book_avtors[0].strip()[book_avtors[0].strip().find(" ")+1:]
        if book_avtors.count('') == 0:
            a2 = book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:] + " " + book_avtors[1].strip()[:book_avtors[1].strip().index(" ")]
            a3 = book_avtors[2].strip()[book_avtors[2].strip().index(" ")+1:] + " " + book_avtors[2].strip()[:book_avtors[2].strip().index(" ")]
            result = f"""{name} [Электронный ресурс]{add_inf} / {a1_name} {a1_f} и [др.]{responsibility} Электрон. текстовые дан.{reissues} {city}: {publish}, {year}.{pages} URL: {url}{name_of_EBC}"""
        elif book_avtors.count('') == 1:
            a2 = book_avtors[1].strip()[:book_avtors[1].strip().index(" ")] + " " + book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:]
            a3 = book_avtors[2].strip()[:book_avtors[2].strip().index(" ")] + " " + book_avtors[2].strip()[book_avtors[2].strip().index(" ")+1:]
            result = f"""{a1_f} {a1_name}, {a2}, {a3} {name} [Электронный ресурс]{add_inf}{responsibility} Электрон. текстовые дан.{reissues} {city}: {publish}, {year}.{pages} URL: {url}{name_of_EBC}"""
        elif book_avtors.count('') == 2:
            a2 = book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:] + " " + book_avtors[1].strip()[:book_avtors[1].strip().index(" ")]
            result = f"""{a1_f} {a1_name}, {a2} {name} [Электронный ресурс]{add_inf}{responsibility} Электрон. текстовые дан.{reissues} {city}: {publish}, {year}.{pages} URL: {url}{name_of_EBC}"""
        elif book_avtors.count('') == 3:
            result = f"""{a1_f} {a1_name} {name} [Электронный ресурс]{add_inf}{responsibility} Электрон. текстовые дан.{reissues} {city}: {publish}, {year}.{pages} URL: {url}{name_of_EBC}"""
    

        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/BookEBC2008", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["Ethernet2008"])
def name_of_eth_2008(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название ресурса")
    gostbot.register_next_step_handler(send, add_inf_2008)
 
def add_inf_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. сведения, относящиеся к названию (заглавию) если они есть\nЕсли их нет введите: . \nОбразец: научный журнал")
    gostbot.register_next_step_handler(send, responsibility_2008)

def responsibility_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. сведения об ответственности\nОбразец: центр информ. технологий РГБ ; ред. Т. В. Власенко ; Web-мастер Н. В. Козлова")
    gostbot.register_next_step_handler(send, city_2008)

def city_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, publish_2008)

def publish_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите имя (наименование) издателя или распространителя\nОбразец: Моск. физ.- техн. ин-т.")
    gostbot.register_next_step_handler(send, year_2008)

def year_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год (укажите только цифру)")
    gostbot.register_next_step_handler(send, url_2008)

def url_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите URL")
    gostbot.register_next_step_handler(send, date_2008)

def date_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите дату обращения\nОбразец: 22.01.23")
    gostbot.register_next_step_handler(send, result_eth_2008)

def result_eth_2008(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    try:
        name = (gost_dict[id_chat][0][0].capitalize() + gost_dict[id_chat][0][1:]).replace("\n"," ")
        if gost_dict[id_chat][1] != ".":
            reissues = " : " + gost_dict[id_chat][1].capitalize()
        else:
            reissues = ""
        responsibility = gost_dict[id_chat][2][0].capitalize() + gost_dict[id_chat][2][1:]
        if gost_dict[id_chat][3].lower() in SPB:
            city = "СПб."
        elif gost_dict[id_chat][3].lower() in MSC:
            city = "М."
        else:
            city = gost_dict[id_chat][3][0].capitalize() + gost_dict[id_chat][3][1:]
        publish = gost_dict[id_chat][4][0].capitalize() + gost_dict[id_chat][4][1:]
        year = gost_dict[id_chat][5]
        url = gost_dict[id_chat][6]
        date = gost_dict[id_chat][7]
        result = f"""{name} [Электронный ресурс]{reissues} / {responsibility} {city}: {publish}, {year}. URL: {url}. (дата обращения: {date})"""
        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Ethernet2008", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["Dissertation2008"])
def dissert_avtor_2008(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите автора диссертации\nОбразец: Иванов А.А.")
    gostbot.register_next_step_handler(send, dissert_name_2008)

def dissert_name_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название диссертации")
    gostbot.register_next_step_handler(send, dissert_rang_2008)

def dissert_rang_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите ученую степень автора диссертации\nОбразец: канд. ист. наук")
    gostbot.register_next_step_handler(send, dissert_shifr_vac_2008)

def dissert_shifr_vac_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите шифр ВАК\nОбразец: 13.00.05")
    gostbot.register_next_step_handler(send, dissert_vac_name_2008)

def dissert_vac_name_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название ВАК (без кавычек) \nОбразец: Инжинерная геометрия и компьютерная графика")
    gostbot.register_next_step_handler(send, dissert_city_2008)

def dissert_city_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, dissert_year_2008)

def dissert_year_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год защиты (только цифра)")
    gostbot.register_next_step_handler(send, dissert_pages_2008)

def dissert_pages_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество страниц\nОбразец: 65")
    gostbot.register_next_step_handler(send, dissert_result_2008)

def dissert_result_2008(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    try:
        dissert_avtor = gost_dict[id_chat][0].split()
        print(dissert_avtor)
        dissert_name = (gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]).replace("\n"," ")
        dissert_rang = gost_dict[id_chat][2]
        dissert_shifr_vac = gost_dict[id_chat][3]
        dissert_vac_name = gost_dict[id_chat][4][0].capitalize() + gost_dict[id_chat][4][1:]
        if gost_dict[id_chat][5].lower() in SPB:
            dissert_city = "СПб."
        elif gost_dict[id_chat][5].lower() in MSC:
            dissert_city = "М."
        else:
            dissert_city = gost_dict[id_chat][5][0].capitalize() + gost_dict[id_chat][5][1:]
        dissert_year = gost_dict[id_chat][6]
        dissert_pages = gost_dict[id_chat][7] 
        result = f"""{dissert_avtor[0]} {dissert_avtor[1][0]}.{dissert_avtor[2][0]}. {dissert_name}: спец. {dissert_shifr_vac} «{dissert_vac_name}»: дис. ... {dissert_rang} {dissert_city}, {dissert_year}. {dissert_pages} с."""

        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Dissertation2008", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["Aftoreferat2008"])
def aftoref_avtor_2008(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите автора диссертации\nОбразец: Иванов А.А.")
    gostbot.register_next_step_handler(send, aftoref_name_2008)

def aftoref_name_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название диссертации")
    gostbot.register_next_step_handler(send, aftoref_rang_2008)

def aftoref_rang_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите ученую степень автора диссертации\nОбразец: канд. ист. наук")
    gostbot.register_next_step_handler(send, aftoref_shifr_vac_2008)

def aftoref_shifr_vac_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите шифр ВАК\nОбразец: 13.00.05")
    gostbot.register_next_step_handler(send, aftoref_vac_name_2008)

def aftoref_vac_name_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название ВАК (без кавычек) \nОбразец: Инжинерная геометрия и компьютерная графика")
    gostbot.register_next_step_handler(send, aftoref_city_2008)

def aftoref_city_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, aftoref_year_2008)

def aftoref_year_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год защиты (только цифра)")
    gostbot.register_next_step_handler(send, aftoref_pages_2008)

def aftoref_pages_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество страниц\nОбразец: 65")
    gostbot.register_next_step_handler(send, aftoref_result_2008)

def aftoref_result_2008(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    try:
        aftoref_avtor = gost_dict[id_chat][0]
        print(aftoref_avtor)
        aftoref_name = (gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]).replace("\n"," ")
        aftoref_rang = gost_dict[id_chat][2]
        aftoref_shifr_vac = gost_dict[id_chat][3]
        aftoref_vac_name = gost_dict[id_chat][4][0].capitalize() + gost_dict[id_chat][4][1:]
        if gost_dict[id_chat][5].lower() in SPB:
            aftoref_city = "СПб."
        elif gost_dict[id_chat][5].lower() in MSC:
            aftoref_city = "М."
        else:
            aftoref_city = gost_dict[id_chat][5][0].capitalize() + gost_dict[id_chat][5][1:]
        aftoref_year = gost_dict[id_chat][6]
        aftoref_pages = gost_dict[id_chat][7] 
        result = f"""{aftoref_avtor.split()[0]} {aftoref_avtor.split()[1][0]}.{aftoref_avtor.split()[2][0]}. {aftoref_name}: спец. {aftoref_shifr_vac} «{aftoref_vac_name}»: автореф. дис. ... {aftoref_rang} {aftoref_city}, {aftoref_year}. {aftoref_pages} с."""

        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Aftoreferat2008", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["Mnogotomnik2008"])
def book_mnogotomnic_toms_avtors_2008(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите авторов\nОбразец: Иванов А.А., Петров А.А.")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_name_2008)

def book_mnogotomnic_toms_name_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название моготомного издания")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_add_inf_2008)

def book_mnogotomnic_toms_add_inf_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. сведения, относящиеся к названию (заглавию) если они есть\nЕсли их нет введите: . \nОбразец: учеб. для академ. бакалавриат.")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_count_toms_2008)

def book_mnogotomnic_toms_count_toms_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество томов всего (укажите только цифру)")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_tom_2008)

def book_mnogotomnic_toms_tom_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите информацию о номере вашего тома (укажите только цифру)")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_reissues_2008)

def book_mnogotomnic_toms_reissues_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. информацию о издании, исправлениях и дополнениях\nЕсли ничего такого нет напишите: . \nОбразец: 5-е изд., перераб. и доп")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_city_2008)

def book_mnogotomnic_toms_city_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_publish_2008)

def book_mnogotomnic_toms_publish_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название издательства")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_year_2008)

def book_mnogotomnic_toms_year_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год издания (только цифра)")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_pages_2008)

def book_mnogotomnic_toms_pages_2008(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество страниц\nОбразец: 65")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_result_2008)

def book_mnogotomnic_toms_result_2008(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    book_mnogotomnic_avtors = [""]*5
    counter = 0
    try:
        print(gost_dict[id_chat][0].split(",")[:5])
        for i in gost_dict[id_chat][0].split(",")[:5]:
            book_mnogotomnic_avtors[counter] = i
            counter += 1
        print(book_mnogotomnic_avtors)
        name = gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]
        if gost_dict[id_chat][2] != ".":
            reissues = " " + gost_dict[id_chat][2].capitalize()
        else:
            reissues = ""
        count_toms = gost_dict[id_chat][3]
        tom_num = gost_dict[id_chat][4]
        if gost_dict[id_chat][5] != ".":
            responsibility = " " + gost_dict[id_chat][5]
        else:
            responsibility = "" 
        if gost_dict[id_chat][6].lower() in SPB:
            city = "СПб."
        elif gost_dict[id_chat][6].lower() in MSC:
            city = "М."
        else:
            city = gost_dict[id_chat][4][0].capitalize() + gost_dict[id_chat][4][1:]
        publish = gost_dict[id_chat][7][0].capitalize() + gost_dict[id_chat][7][1:]
        year = gost_dict[id_chat][8]
        pages = gost_dict[id_chat][9]
        a1_f = book_mnogotomnic_avtors[0].strip()[:book_mnogotomnic_avtors[0].strip().find(" ")]
        a1_name = book_mnogotomnic_avtors[0].strip()[book_mnogotomnic_avtors[0].strip().find(" ")+1:]
        if book_mnogotomnic_avtors.count('') == 0:
            a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            a3 = book_mnogotomnic_avtors[2].strip()[book_mnogotomnic_avtors[2].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[2].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            result = f"""{a1_f} {a1_name}, {a2}, {a3} {name}.{reissues} В {count_toms} т. Т. {tom_num}{responsibility} {city}: {publish}, {year}. {pages} с."""
        elif book_mnogotomnic_avtors.count('') == 1:
            a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            a3 = book_mnogotomnic_avtors[2].strip()[book_mnogotomnic_avtors[2].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[2].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            a4 = book_mnogotomnic_avtors[3].strip()[book_mnogotomnic_avtors[3].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[3].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            result = f"""{a1_f} {a1_name}, {a2}, {a3}, {a4} {name}.{reissues} В {count_toms} т. Т. {tom_num}{responsibility} {city}: {publish}, {year}. {pages} с."""
        elif book_mnogotomnic_avtors.count('') == 2:
            a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            a3 = book_mnogotomnic_avtors[2].strip()[book_mnogotomnic_avtors[2].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[2].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            result = f"""{a1_f} {a1_name}, {a2}, {a3} {name}.{reissues} В {count_toms} т. Т. {tom_num}{responsibility} {city}: {publish}, {year}. {pages} с."""
        elif book_mnogotomnic_avtors.count('') == 3:
            a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            result = f"""{a1_f} {a1_name}, {a2} {name}.{reissues} В {count_toms} т. Т. {tom_num}{responsibility} {city}: {publish}, {year}. {pages} с."""
        else:
            result = f"""{a1_f} {a1_name} {name}.{reissues} В {count_toms} т. Т. {tom_num}{responsibility} {city}: {publish}, {year}. {pages} с."""


        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Mnogotomnik2008", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

# 2018 год 
# Handler для работы с журналом ГОСТ-а 2018 года
@gostbot.message_handler(commands=["Journal2018"])
def jour_avtors_2018(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите авторов\nОбразец: Иванов А.А., Петров А.А.")
    gostbot.register_next_step_handler(send, jour_tema_2018)

def jour_tema_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите тему")
    gostbot.register_next_step_handler(send, jour_name_2018)

def jour_name_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название журнала")
    gostbot.register_next_step_handler(send, jour_year_2018)

def jour_year_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год издания (только цифра)")
    gostbot.register_next_step_handler(send, jour_nomer_2018)

def jour_nomer_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите номер журнала (только цифра)")
    gostbot.register_next_step_handler(send, jour_pages_2018)

def jour_pages_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите страницы журнала (через тире)\nОбразец: 65-70")
    gostbot.register_next_step_handler(send, journal_result_2018)

def journal_result_2018(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    jour_avtors = [""]*5
    counter = 0
    try:
        print(gost_dict[id_chat][0].split(",")[:5])
        for i in gost_dict[id_chat][0].split(",")[:5]:
            jour_avtors[counter] = i
            counter += 1
        print(jour_avtors)
        tema = (gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]).replace("\n"," ")
        journal_name = gost_dict[id_chat][2][0].capitalize() + gost_dict[id_chat][2][1:]
        year = gost_dict[id_chat][3]
        nomer = gost_dict[id_chat][4]
        pages = gost_dict[id_chat][5]
        a1_f = jour_avtors[0].strip()[:jour_avtors[0].strip().find(" ")]
        a1_name = jour_avtors[0].strip()[jour_avtors[0].strip().find(" ")+1:]
        if jour_avtors.count('') == 0:
            a2 = jour_avtors[1].strip()[jour_avtors[1].strip().index(" ")+1:] + " " + jour_avtors[1].strip()[:jour_avtors[1].strip().index(" ")]
            a3 = jour_avtors[2].strip()[jour_avtors[2].strip().index(" ")+1:] + " " + jour_avtors[2].strip()[:jour_avtors[2].strip().index(" ")]
            result = f"""{tema} / {a1_name} {a1_f}, {a2}, {a3} [и др.] // {journal_name}. — {year}. — № {nomer}. — C. {pages}."""
        elif jour_avtors.count('') == 1:
            a2 = jour_avtors[1].strip()[jour_avtors[1].strip().index(" ")+1:] + " " + jour_avtors[1].strip()[:jour_avtors[1].strip().index(" ")]
            a3 = jour_avtors[2].strip()[jour_avtors[2].strip().index(" ")+1:] + " " + jour_avtors[2].strip()[:jour_avtors[2].strip().index(" ")]
            a4 = jour_avtors[3].strip()[jour_avtors[3].strip().index(" ")+1:] + " " + jour_avtors[3].strip()[:jour_avtors[3].strip().index(" ")]
            result = f"""{tema} / {a1_name} {a1_f}, {a2}, {a3}, {a4} // {journal_name}. — {year}. — № {nomer}. — C. {pages}."""
        elif jour_avtors.count('') == 2:
            a2 = jour_avtors[1].strip()[jour_avtors[1].strip().index(" ")+1:] + " " + jour_avtors[1].strip()[:jour_avtors[1].strip().index(" ")]
            a3 = jour_avtors[2].strip()[jour_avtors[2].strip().index(" ")+1:] + " " + jour_avtors[2].strip()[:jour_avtors[2].strip().index(" ")]
            result = f"""{a1_f}, {a1_name} {tema} / {a1_name} {a1_f}, {a2}, {a3} // {journal_name}. — {year}. — № {nomer}. — C. {pages}."""
        elif jour_avtors.count('') == 3:
            a2 = jour_avtors[1].strip()[jour_avtors[1].strip().index(" ")+1:] + " " + jour_avtors[1].strip()[:jour_avtors[1].strip().index(" ")]
            result = f"""{a1_f}, {a1_name} {tema} / {a1_name} {a1_f}, {a2} // {journal_name}. — {year}. — № {nomer}. — C. {pages}."""
        else:
            result = f"""{a1_f}, {a1_name} {tema} / {a1_name} {a1_f} // {journal_name}. — {year}. — № {nomer}. — C. {pages}."""

        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Journal2018", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["BookNormal2018"])
def book_normal_avtors_2018(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите автора(ов)\nОбразец: Иванов А.А., Петров А.А.")
    gostbot.register_next_step_handler(send, book_normal_name_2018)

def book_normal_name_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название")
    gostbot.register_next_step_handler(send, book_normal_add_inf_2018)

def book_normal_add_inf_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. сведения, относящиеся к названию (заглавию) если они есть\nЕсли их нет введите: . \nОбразец: учебник")
    gostbot.register_next_step_handler(send, book_normal_responsibility_2018)

def book_normal_responsibility_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. сведения об ответственности если они есть\nЕсли их нет введите: . \nОбразец: отв. ред. П. П. Петров ; пер. с англ. С. С. Сидорова")
    gostbot.register_next_step_handler(send, book_normal_reissues_2018)

def book_normal_reissues_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. информацию о издании, исправлениях и дополнениях\nЕсли ничего такого нет напишите: . \nОбразец: 6-е изд., испр. и доп.")
    gostbot.register_next_step_handler(send, book_normal_city_2018)

def book_normal_city_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, book_normal_publish_2018)

def book_normal_publish_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название издательства")
    gostbot.register_next_step_handler(send, book_normal_year_2018)

def book_normal_year_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год издания (укажите только цифру)")
    gostbot.register_next_step_handler(send, book_normal_pages_2018)

def book_normal_pages_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество страниц\nОбразец: 65")
    gostbot.register_next_step_handler(send, book_normal_result_2018)

def book_normal_result_2018(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    book_avtors = [""]*5
    counter = 0
    try:
        print(gost_dict[id_chat][0].split(",")[:5])
        for i in gost_dict[id_chat][0].split(",")[:5]:
            book_avtors[counter] = i
            counter += 1
        if book_avtors[0] == ".":
            book_avtors[0] == ""
        print(book_avtors)
        name = (gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]).replace("\n"," ")
        if gost_dict[id_chat][2] != ".":
            add_inf = " : " + gost_dict[id_chat][2]
        else:
            add_inf = ""
        if gost_dict[id_chat][3] != ".":
            responsibility = "; " + gost_dict[id_chat][3] + "."
        else:
            responsibility = ""
        if gost_dict[id_chat][4] != ".":
            reissues = " — " + gost_dict[id_chat][4] + " — "
        else:
            reissues = ""
        if gost_dict[id_chat][5].lower() in SPB:
            city = "СПб."
        elif gost_dict[id_chat][5].lower() in MSC:
            city = "М."
        else:
            city = gost_dict[id_chat][5][0].capitalize() + gost_dict[id_chat][5][1:]
        publish = gost_dict[id_chat][6][0].capitalize() + gost_dict[id_chat][6][1:]
        year = gost_dict[id_chat][7]
        pages = gost_dict[id_chat][8]
        a1_f = book_avtors[0].strip()[:book_avtors[0].strip().find(" ")]
        a1_name = book_avtors[0].strip()[book_avtors[0].strip().find(" ")+1:]
        if book_avtors.count('') == 0:
            a2 = book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:] + " " + book_avtors[1].strip()[:book_avtors[1].strip().index(" ")]
            a3 = book_avtors[2].strip()[book_avtors[2].strip().index(" ")+1:] + " " + book_avtors[2].strip()[:book_avtors[2].strip().index(" ")]
            result = f"""{name}{add_inf} / {a1_name} {a1_f}, {a2}, {a3} [и др.]. {responsibility}{reissues}{city} : {publish}, {year}. — {pages} c."""
        elif book_avtors.count('') == 1:
            a2 = book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:] + " " + book_avtors[1].strip()[:book_avtors[1].strip().index(" ")]
            a3 = book_avtors[2].strip()[book_avtors[2].strip().index(" ")+1:] + " " + book_avtors[2].strip()[:book_avtors[2].strip().index(" ")]
            a4 = book_avtors[3].strip()[book_avtors[3].strip().index(" ")+1:] + " " + book_avtors[3].strip()[:book_avtors[3].strip().index(" ")]
            result = f"""{name}{add_inf} / {a1_name} {a1_f}, {a2}, {a3}, {a4}. {responsibility}{reissues}{city} : {publish}, {year}. — {pages} c."""
        elif book_avtors.count('') == 2:
            a2 = book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:] + " " + book_avtors[1].strip()[:book_avtors[1].strip().index(" ")]
            a3 = book_avtors[2].strip()[book_avtors[2].strip().index(" ")+1:] + " " + book_avtors[2].strip()[:book_avtors[2].strip().index(" ")]
            result = f"""{a1_f}, {a1_name} {name}{add_inf} / {a1_name} {a1_f}, {a2}, {a3}. {responsibility}{reissues}{city} : {publish}, {year}. — {pages} c."""
        elif book_avtors.count('') == 3:
            a2 = book_avtors[1].strip()[book_avtors[1].strip().index(" ")+1:] + " " + book_avtors[1].strip()[:book_avtors[1].strip().index(" ")]
            result = f"""{a1_f}, {a1_name} {name}{add_inf} / {a1_name} {a1_f}, {a2}. {responsibility}{reissues}{city} : {publish}, {year}. — {pages} c."""
        elif book_avtors.count('') == 4:
            result = f"""{a1_f}, {a1_name} {name}{add_inf} / {a1_name} {a1_f}. {responsibility}{reissues}{city} : {publish}, {year}. — {pages} c."""

        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/BookNormal2018", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["Ethernet2018"])
def name_of_eth_2018(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название ресурса")
    gostbot.register_next_step_handler(send, add_inf_2018)
 
def add_inf_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. сведения, относящиеся к названию (заглавию) если они есть\nЕсли их нет введите: . \nОбразец: сайт")
    gostbot.register_next_step_handler(send, city_2018)

def city_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, year_2018)

def year_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год (укажите только цифру)")
    gostbot.register_next_step_handler(send, url_2018)

def url_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите URL")
    gostbot.register_next_step_handler(send, date_2018)

def date_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите дату обращения\nОбразец: 22.01.23")
    gostbot.register_next_step_handler(send, result_eth_2018)

def result_eth_2018(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    try:
        name = (gost_dict[id_chat][0][0].capitalize() + gost_dict[id_chat][0][1:]).replace("\n"," ")
        if gost_dict[id_chat][1] != ".":
            reissues = " : " + gost_dict[id_chat][1]
        else:
            reissues = ""
        if gost_dict[id_chat][2].lower() in SPB:
            city = "СПб."
        elif gost_dict[id_chat][2].lower() in MSC:
            city = "М."
        else:
            city = gost_dict[id_chat][2][0].capitalize() + gost_dict[id_chat][2][1:]
        year = gost_dict[id_chat][3]
        url = gost_dict[id_chat][4]
        date = gost_dict[id_chat][5]
        result = f"""{name}{reissues} {city}, {year}. URL: {url} (дата обращения: {date})."""
        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Ethernet2018", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["Dissertation2018"])
def dissert_avtor_2018(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите автора диссертации\nОбразец: Иванов Александр Александорович")
    gostbot.register_next_step_handler(send, dissert_name_2018)

def dissert_name_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название диссертации")
    gostbot.register_next_step_handler(send, dissert_rang_2018)

def dissert_rang_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите ученую степень автора диссертации\nОбразец: канд. ист. наук")
    gostbot.register_next_step_handler(send, dissert_shifr_vac_2018)

def dissert_shifr_vac_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите шифр ВАК\nОбразец: 13.00.05")
    gostbot.register_next_step_handler(send, dissert_vac_name_2018)

def dissert_vac_name_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название ВАК (без кавычек) \nОбразец: Инжинерная геометрия и компьютерная графика")
    gostbot.register_next_step_handler(send, dissert_city_2018)

def dissert_city_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, dissert_year_2018)

def dissert_year_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год защиты (только цифра)")
    gostbot.register_next_step_handler(send, dissert_pages_2018)

def dissert_pages_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество страниц\nОбразец: 65")
    gostbot.register_next_step_handler(send, dissert_result_2018)

def dissert_result_2018(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    try:
        dissert_avtor = gost_dict[id_chat][0]
        print(dissert_avtor)
        dissert_name = (gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]).replace("\n"," ")
        dissert_rang = gost_dict[id_chat][2]
        dissert_shifr_vac = gost_dict[id_chat][3]
        dissert_vac_name = gost_dict[id_chat][4][0].capitalize() + gost_dict[id_chat][4][1:]
        if gost_dict[id_chat][5].lower() in SPB:
            dissert_city = "СПб."
        elif gost_dict[id_chat][5].lower() in MSC:
            dissert_city = "М."
        else:
            dissert_city = gost_dict[id_chat][5][0].capitalize() + gost_dict[id_chat][5][1:]
        dissert_year = gost_dict[id_chat][6]
        dissert_pages = gost_dict[id_chat][7] 
        result = f"""{dissert_avtor.split()[0]}, {dissert_avtor.split()[1][0]}.{dissert_avtor.split()[2][0]}. {dissert_name}: спец. {dissert_shifr_vac} «{dissert_vac_name}»: автореф. дис. ... {dissert_rang} / {dissert_avtor}. — {dissert_city}, {dissert_year}. — {dissert_pages} с."""

        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Dissertation2018", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["Aftoreferat2018"])
def aftoref_avtor_2018(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите автора диссертации\nОбразец: Иванов Александр Александорович")
    gostbot.register_next_step_handler(send, aftoref_name_2018)

def aftoref_name_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название диссертации")
    gostbot.register_next_step_handler(send, aftoref_rang_2018)

def aftoref_rang_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите ученую степень автора диссертации\nОбразец: канд. ист. наук")
    gostbot.register_next_step_handler(send, aftoref_shifr_vac_2018)

def aftoref_shifr_vac_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите шифр ВАК\nОбразец: 13.00.05")
    gostbot.register_next_step_handler(send, aftoref_vac_name_2018)

def aftoref_vac_name_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название ВАК (без кавычек) \nОбразец: Инжинерная геометрия и компьютерная графика")
    gostbot.register_next_step_handler(send, aftoref_city_2018)

def aftoref_city_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, aftoref_year_2018)

def aftoref_year_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год защиты (только цифра)")
    gostbot.register_next_step_handler(send, aftoref_pages_2018)

def aftoref_pages_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество страниц\nОбразец: 65")
    gostbot.register_next_step_handler(send, aftoref_result_2018)

def aftoref_result_2018(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    try:
        aftoref_avtor = gost_dict[id_chat][0]
        print(aftoref_avtor)
        aftoref_name = (gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]).replace("\n"," ")
        aftoref_rang = gost_dict[id_chat][2]
        aftoref_shifr_vac = gost_dict[id_chat][3]
        aftoref_vac_name = gost_dict[id_chat][4][0].capitalize() + gost_dict[id_chat][4][1:]
        if gost_dict[id_chat][5].lower() in SPB:
            aftoref_city = "СПб."
        elif gost_dict[id_chat][5].lower() in MSC:
            aftoref_city = "М."
        else:
            aftoref_city = gost_dict[id_chat][5][0].capitalize() + gost_dict[id_chat][5][1:]
        aftoref_year = gost_dict[id_chat][6]
        aftoref_pages = gost_dict[id_chat][7] 
        result = f"""{aftoref_avtor.split()[0]}, {aftoref_avtor.split()[1][0]}.{aftoref_avtor.split()[2][0]}. {aftoref_name}: спец. {aftoref_shifr_vac} «{aftoref_vac_name}»: автореф. дис. ... {aftoref_rang} / {aftoref_avtor}. — {aftoref_city}, {aftoref_year}. — {aftoref_pages} с."""

        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Aftoreferat2018", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)

@gostbot.message_handler(commands=["Mnogotomnik2018"])
def book_mnogotomnic_toms_avtors_2018(message):
    id_chat = message.chat.id
    add_user_in_db(id_chat, gost_dict)
    username = message.from_user
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите авторов\nОбразец: Иванов А.А., Петров А.А.")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_name_2018)

def book_mnogotomnic_toms_name_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название моготомного издания")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_add_inf_2018)

def book_mnogotomnic_toms_add_inf_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. сведения, относящиеся к названию (заглавию) если они есть\nЕсли их нет введите: . \nОбразец: учеб. для академ. бакалавриат.")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_count_toms_2018)

def book_mnogotomnic_toms_count_toms_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество томов всего (укажите только цифру)")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_tom_2018)

def book_mnogotomnic_toms_tom_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите информацию о номере вашего тома (укажите только цифру)")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_reissues_2018)

def book_mnogotomnic_toms_reissues_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите доп. информацию о издании, исправлениях и дополнениях\nЕсли ничего такого нет напишите: . \nОбразец: 5-е изд., перераб. и доп")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_city_2018)

def book_mnogotomnic_toms_city_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите город")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_publish_2018)

def book_mnogotomnic_toms_publish_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите название издательства")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_year_2018)

def book_mnogotomnic_toms_year_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите год издания (только цифра)")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_pages_2018)

def book_mnogotomnic_toms_pages_2018(message):
    id_chat = message.chat.id
    username = message.from_user
    gost_dict[id_chat].append(message.text)
    send = gostbot.send_message(id_chat, f"{username.first_name}, введите количество страниц\nОбразец: 65")
    gostbot.register_next_step_handler(send, book_mnogotomnic_toms_result_2018)

def book_mnogotomnic_toms_result_2018(message):
    id_chat = message.chat.id
    result = ""
    gost_dict[id_chat].append(message.text)
    book_mnogotomnic_avtors = [""]*5
    counter = 0
    try:
        print(gost_dict[id_chat][0].split(",")[:5])
        for i in gost_dict[id_chat][0].split(",")[:5]:
            book_mnogotomnic_avtors[counter] = i
            counter += 1
        print(book_mnogotomnic_avtors)
        name = gost_dict[id_chat][1][0].capitalize() + gost_dict[id_chat][1][1:]
        if gost_dict[id_chat][2] != ".":
            reissues = " " + gost_dict[id_chat][2].capitalize()
        else:
            reissues = ""
        count_toms = gost_dict[id_chat][3]
        tom_num = gost_dict[id_chat][4]
        if gost_dict[id_chat][5] != ".":
            responsibility = " — " + gost_dict[id_chat][5]
        else:
            responsibility = "" 
        if gost_dict[id_chat][6].lower() in SPB:
            city = "СПб."
        elif gost_dict[id_chat][6].lower() in MSC:
            city = "М."
        else:
            city = gost_dict[id_chat][4][0].capitalize() + gost_dict[id_chat][4][1:]
        publish = gost_dict[id_chat][7][0].capitalize() + gost_dict[id_chat][7][1:]
        year = gost_dict[id_chat][8]
        pages = gost_dict[id_chat][9]
        a1_f = book_mnogotomnic_avtors[0].strip()[:book_mnogotomnic_avtors[0].strip().find(" ")]
        a1_name = book_mnogotomnic_avtors[0].strip()[book_mnogotomnic_avtors[0].strip().find(" ")+1:]
        if book_mnogotomnic_avtors.count('') == 0:
            a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            a3 = book_mnogotomnic_avtors[2].strip()[book_mnogotomnic_avtors[2].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[2].strip()[:book_mnogotomnic_avtors[2].strip().index(" ")]
            result = f"""{a1_f}, {a1_name} {name}.{reissues} В {count_toms} т. Т. {tom_num} / {a1_name} {a1_f}, {a2}, {a3} [и др.].{responsibility} — {city}: {publish}, {year}. — {pages} с."""
        elif book_mnogotomnic_avtors.count('') == 1:
            a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            a3 = book_mnogotomnic_avtors[2].strip()[book_mnogotomnic_avtors[2].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[2].strip()[:book_mnogotomnic_avtors[2].strip().index(" ")]
            a4 = book_mnogotomnic_avtors[3].strip()[book_mnogotomnic_avtors[3].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[3].strip()[:book_mnogotomnic_avtors[3].strip().index(" ")]
            result = f"""{a1_f}, {a1_name} {name}.{reissues} В {count_toms} т. Т. {tom_num} / {a1_name} {a1_f}, {a2}, {a3}, {a4}.{responsibility} — {city}: {publish}, {year}. — {pages} с."""
        elif book_mnogotomnic_avtors.count('') == 2:
            a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            a3 = book_mnogotomnic_avtors[2].strip()[book_mnogotomnic_avtors[2].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[2].strip()[:book_mnogotomnic_avtors[2].strip().index(" ")]
            result = f"""{a1_f}, {a1_name} {name}.{reissues} В {count_toms} т. Т. {tom_num} / {a1_name} {a1_f}, {a2}, {a3}.{responsibility} — {city}: {publish}, {year}. — {pages} с."""
        elif book_mnogotomnic_avtors.count('') == 3:
            a2 = book_mnogotomnic_avtors[1].strip()[book_mnogotomnic_avtors[1].strip().index(" ")+1:] + " " + book_mnogotomnic_avtors[1].strip()[:book_mnogotomnic_avtors[1].strip().index(" ")]
            print(a2)
            result = f"""{a1_f}, {a1_name} {name}.{reissues} В {count_toms} т. Т. {tom_num} / {a1_name} {a1_f}, {a2}.{responsibility} — {city}: {publish}, {year}. — {pages} с."""
        else:
            result = f"""{a1_f}, {a1_name} {name}.{reissues} В {count_toms} т. Т. {tom_num} / {a1_name} {a1_f}.{responsibility} — {city}: {publish}, {year}. — {pages} с."""


        gostbot.send_message(id_chat, f"Твой ГОСТ готов \\!\n`{result}`", parse_mode="MarkdownV2")
        gostbot.send_message(id_chat, f"Чтобы воспользоваться этим оформлением снова введите:\n/Mnogotomnik2018", parse_mode="MarkdownV2", reply_markup=back())
        print(result)
        gost_dict[id_chat].clear()
    except:
        gost_dict[id_chat].clear()
        gostbot.send_animation(id_chat, animation="https://media1.tenor.com/m/oIuJXBhq4MwAAAAd/aesthetic-skull.gif")
        gostbot.send_message(id_chat, "Некорректный ввод. Перезапуск бота...")
        main(message)


@gostbot.message_handler(commands=["stop"])
def stop(message):
    chat_id = message.chat.id
    answer = """Остановлено!"""
    gostbot.reply_to(message, answer)
    gostbot.send_animation(chat_id, animation="https://tenor.com/ru/view/eralash-gif-19959945")

@gostbot.message_handler(commands=["about"])
def about(message):
    answer = """Этот бот был создан для того, чтобы студенты и школьники с лёгкостью могли оформлять источники в списке источников по ГОСТ-ам. Он поможет увеличить эффективность написания научных работ и сократить время на их выполнение."""
    gostbot.reply_to(message, answer)

@gostbot.message_handler(commands=["bug_report"])
def bug_report(message):
    gostbot.reply_to(message, "Если вы нашли баги и ошибки в работе бота - скидывайте скрины ошибки и описание проблемы\nhttps://t.me/Umor1st")
@gostbot.message_handler(commands=["help"])
def help_about(message):
    gostbot.reply_to(message, """/start - Начать пользоваться ботом\n/about - О боте\n/help - Cписок команд\n/bug_report - Информация на случай нахождения ошибок""")


# KEK handlers :D

@gostbot.message_handler(func=lambda message: message.text == "bra")
def bra(message):
    gostbot.reply_to(message, "Ну что сказать - bruuuuuh")

@gostbot.message_handler(func=lambda message: message.text == "sigma")
def sigma_moment(message):
    chat_id = message.chat.id
    gostbot.send_animation(chat_id, "https://media.tenor.com/Wg9fW_XEft0AAAAM/pout-christian-bale.gif")

@gostbot.message_handler()
def sigma_moment(message):
    chat_id = message.chat.id
    if message.text in ["god", "genius"]:
        gostbot.send_message(chat_id, "https://t.me/Umor1st")

# Запуск программы

if __name__ == "__main__":
    try:
        # Запускаем бесконечную работу бота
        gostbot.polling(non_stop=True)
    except:
        gostbot.polling(non_stop=True)