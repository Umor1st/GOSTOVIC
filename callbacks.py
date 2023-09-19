from main import gostbot as gostbot
from buttons import *
from telebot.types import ReplyKeyboardRemove
#Делаем список для сохранения клавиатур и текстов для функции back
backlist = []

#Callback возращает выбор года ГОСТа для студента
@gostbot.callback_query_handler(func=lambda call: call.data == "Student")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите одну из категорий:",markup_main()])
    gostbot.edit_message_text(text="Выберите год:",chat_id=id_chat,message_id = message_id)
    gostbot.edit_message_reply_markup(chat_id=id_chat,message_id=message_id,reply_markup = markup_years())

#Callback возращает выбор года ГОСТа для ученика
@gostbot.callback_query_handler(func=lambda call: call.data == "School")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите одну из категорий:",markup_main()])
    gostbot.edit_message_text(text="Выберите год:",chat_id=id_chat,message_id = message_id)
    gostbot.edit_message_reply_markup(chat_id=id_chat,message_id=message_id,reply_markup = markup_years())

#Callback возращает виды литры для,ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите год:",markup_years()])
    gostbot.edit_message_text(text="Материалы для ГОСТ 2003 года",chat_id=id_chat,message_id = message_id)
    gostbot.edit_message_reply_markup(chat_id=id_chat,message_id=message_id,reply_markup = markup_2003())   
    
#Callback возращает виды литры для 2008 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2008")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите год:",markup_years()])
    gostbot.edit_message_text(text="Материалы для ГОСТ 2008 года",chat_id=id_chat,message_id = message_id)
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup = markup_2008())


#Callback возращает виды литры для 2018 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2018")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите год:",markup_years()])
    gostbot.edit_message_text(text="Материалы для ГОСТ 2018 года",chat_id = id_chat, message_id=message_id)
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup = markup_2018())

#2003 год
#Callback возращает журнал для,ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003_journal")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2003 года", markup_2003()])
    gostbot.edit_message_text("Отправьте: `/Начать_Journal-2003`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает выбор двух видов книг,ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003_book")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2003 года", markup_2003()])
    gostbot.edit_message_text("Выберите одно оформление книги:", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=book_2003())

#Callback возращает начало работы с обычными книгами,ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003_book_normal")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите одно оформление книги:", book_2003()])
    gostbot.edit_message_text("Отправьте: `/Начать_Book-Normal-2003`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с интернет ресурсами,ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003_ethres")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2003 года", markup_2003()])
    gostbot.edit_message_text("Отправьте: `/Начать_Ethernet-2003`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с диссертациями,ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003_disert")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2003 года", markup_2003()])
    gostbot.edit_message_text("Отправьте: `/Начать_Dissertation-2003`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с авторефератами,ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003_autoref")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2003 года", markup_2003()])
    gostbot.edit_message_text("Отправьте: `/Начать_Aftoreferat-2003`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с законодательными материалами,ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003_zakun")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2003 года", markup_2003()])
    gostbot.edit_message_text("Выберите один из предложенных законодательных материалов", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=zakon_2003())

#Callback возращает начало работы с законодать. документами,ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003_zakun_document")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите один из предложенных законодательных материалов", zakon_2003()])
    gostbot.edit_message_text("Отправьте: `/Начать_Zakon-2003_Document`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с Фед. Законами,ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003_zakun_federation")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите один из предложенных законодательных материалов", zakon_2003()])
    gostbot.edit_message_text("Отправьте: `/Начать_Zakon-2003_Federation`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с Фед. Законами (Internet),ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003_zakun_federation_eth")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите один из предложенных законодательных материалов", zakon_2003()])
    gostbot.edit_message_text("Отправьте: `/Начать_Zakon-2003_Federation_Internet`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с постановлениями,ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003_zakun_postan")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите один из предложенных законодательных материалов", zakon_2003()])
    gostbot.edit_message_text("Отправьте: `/Начать_Zakon-2003_Postanovlenie`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с многотомными изданиями,ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003_mnogotom")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите одно оформление книги:", book_2003()])
    gostbot.edit_message_text("Выберете вид разделения издания:", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=book_mnogotom_2003())

#Callback возращает начало работы с многотомными изданиями,ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003_mnogotom_toms")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберете вид разделения издания:", book_mnogotom_2003()])
    gostbot.edit_message_text("Отправьте: `/Начать_Mnogotomnik-2003_toms`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с многотомными изданиями,ГОСТ 2003 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2003_mnogotom_chapters")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберете вид раздления издания:", book_mnogotom_2003()])
    gostbot.edit_message_text("Отправьте: `/Начать_Mnogotomnik-2003_chapters`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#2008 год
#Callback возращает журнал для,ГОСТ 2008 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2008_journal")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2008 года", markup_2008()])
    gostbot.edit_message_text("Отправьте: `/Начать_Journal-2008`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает выбор двух видов книг,ГОСТ 2008 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2008_book")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2008 года", markup_2008()])
    gostbot.edit_message_text("Выберите одно оформление книги:", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=book_2008())

#Callback возращает начало работы с обычными книгами,ГОСТ 2008 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2008_book_normal")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите одно оформление книги:", book_2008()])
    gostbot.edit_message_text("Отправьте: `/Начать_Book-Normal-2008`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с обычными книгами,ГОСТ 2008 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2008_book_EBC")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите одно оформление книги:", book_2008()])
    gostbot.edit_message_text("Отправьте: `/Начать_Book-EBC-2008`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с интернет ресурсами,ГОСТ 2008 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2008_ethres")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2008 года", markup_2008()])
    gostbot.edit_message_text("Отправьте: `/Начать_Ethernet-2008`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с диссертациями,ГОСТ 2008 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2008_disert")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2008 года", markup_2008()])
    gostbot.edit_message_text("Отправьте: `/Начать_Dissertation-2008`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с авторефератами,ГОСТ 2008 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2008_aftoref")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2008 года", markup_2008()])
    gostbot.edit_message_text("Отправьте: `/Начать_Aftoreferat-2008`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с томом из многотомного издания,ГОСТ 2008 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2008_tom_iz_mnogotom")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2008 года", markup_2008()])
    gostbot.edit_message_text("Отправьте: `/Начать_Mnogotomnik-2008`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#2018 год
#Callback возращает журнал для,ГОСТ 2018 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2018_journal")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2018 года", markup_2018()])
    gostbot.edit_message_text("Отправьте: `/Начать_Journal-2018`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает выбор двух видов книг,ГОСТ 2008 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2018_book")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2018 года", markup_2018()])
    gostbot.edit_message_text("Выберите одно оформление книги:", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=book_2018())

#Callback возращает начало работы с обычными книгами,ГОСТ 2018 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2018_book_normal")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите одно оформление книги:", book_2018()])
    gostbot.edit_message_text("Отправьте: `/Начать_Book-Normal-2018`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с обычными книгами,ГОСТ 2018 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2018_book_EBC")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Выберите одно оформление книги:", book_2018()])
    gostbot.edit_message_text("Отправьте: `/Начать_Book-EBC-2018`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с интернет ресурсами,ГОСТ 2008 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2018_ethres")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2018 года", markup_2008()])
    gostbot.edit_message_text("Отправьте: `/Начать_Ethernet-2018`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с диссертациями,ГОСТ 2018 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2018_disert")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2018 года", markup_2018()])
    gostbot.edit_message_text("Отправьте: `/Начать_Dissertation-2018`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с авторефератами,ГОСТ 2018 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2018_aftoref")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2018 года", markup_2018()])
    gostbot.edit_message_text("Отправьте: `/Начать_Aftoreferat-2018`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())

#Callback возращает начало работы с томом из многотомного издания,ГОСТ 2018 года
@gostbot.callback_query_handler(func=lambda call: call.data == "2018_tom_iz_mnogotom")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    backlist.append(["Материалы для ГОСТ 2008 года", markup_2008()])
    gostbot.edit_message_text("Отправьте: `/Начать_Mnogotomnik-2018`", id_chat, message_id, parse_mode="MarkdownV2")
    gostbot.edit_message_reply_markup(id_chat, message_id, reply_markup=back())




#Callback для переноса пользователя на прошлую менюшку
@gostbot.callback_query_handler(func=lambda call: call.data == "back")
def callback_query(call):
    id_chat = call.message.chat.id
    message_id = call.message.message_id
    #Здесь мы выясняем есть ли в нашей "базе"(списке) хотя бы одно значение
    #Чтобы понять является ли менюшка главной т.е. стопить или бекать
    if len(backlist) == 0:
        gostbot.delete_message(message_id=message_id,chat_id = id_chat)
        gostbot.send_animation(chat_id=id_chat,animation="https://tenor.com/ru/view/ponasenkov-%D0%BF%D0%BE%D0%BD%D0%B0%D1%81%D0%B5%D0%BD%D0%BA%D0%BE%D0%B2-%D0%BA%D1%80%D1%83%D1%82%D0%B8%D1%82%D1%81%D1%8F-kmza-gif-23502971")
    else:
        #Здесь мы берем последний элемент списка(Это массив в котором лежит нужный текст и клавиатура)
        #И заменяем текст и клавиатуру сообщения на прошлое
        #Дальше удаляем этот элемент из списка и престо функция back готова!    
        gostbot.edit_message_text(backlist[-1][0],id_chat,message_id)
        gostbot.edit_message_reply_markup(id_chat, message_id,reply_markup = backlist[-1][1])
        backlist.pop()