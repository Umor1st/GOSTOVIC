from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Короче, здесь расположены все клавиатуры с кнопками, которые используются в боте
# Для клав характерно добавление кнопок вида: [[BUTTON_FUNC],[BUTTON_FUNC]]


def markup_main():
    markup_main_buttons = [[InlineKeyboardButton(text="Cтудент",callback_data="Student"),
                            InlineKeyboardButton(text="Ученик",callback_data="School")],
                           [InlineKeyboardButton(text="stop",callback_data="back")]]
    # Создаем клавиатуру и return значение
    markup_main = InlineKeyboardMarkup(keyboard=markup_main_buttons)
    return markup_main

# Inline клавиатура для видов годов
def markup_years():
    markup_years_buttons = [[InlineKeyboardButton(text="2003",callback_data="2003"),
                            InlineKeyboardButton(text="2008",callback_data="2008"),
                            InlineKeyboardButton(text="2018",callback_data="2018")],
                           [InlineKeyboardButton(text="back",callback_data="back")]]
    # Создаем клавиатуру и return значение
    markup_years = InlineKeyboardMarkup(keyboard=markup_years_buttons)
    return markup_years

# Inline клавиатура для видов литератур госта 2003
def markup_2003():
    markup_g2003_buttons = [[InlineKeyboardButton(text="Журнал",callback_data="2003_journal"),
                             InlineKeyboardButton(text="Книга",callback_data="2003_book"),
                             InlineKeyboardButton(text="Интернет ресурс",callback_data="2003_ethres")],
                            [InlineKeyboardButton(text="Диссертация",callback_data="2003_disert"),
                             InlineKeyboardButton(text="Автореферат",callback_data="2003_autoref")],
                            [InlineKeyboardButton(text="Законодательные материалы",callback_data="2003_zakun")],
                            [InlineKeyboardButton(text="back",callback_data="back")]]
    markup_2003 = InlineKeyboardMarkup(keyboard=markup_g2003_buttons)
    return markup_2003

# Inline клавиатура для видов литератур госта 2008
def markup_2008():
    markup_g2008_buttons = [[InlineKeyboardButton(text="Журнал",callback_data="2008_journal"),
                             InlineKeyboardButton(text="Книга",callback_data="2008_book"),
                             InlineKeyboardButton(text="Интернет ресурс",callback_data="2008_ethres")],
                            [InlineKeyboardButton(text="Автореферат",callback_data="2008_aftoref"),
                             InlineKeyboardButton(text="Диссертация",callback_data="2008_disert")],
                            [InlineKeyboardButton(text="back",callback_data="back")]]
    markup_2008 = InlineKeyboardMarkup(keyboard=markup_g2008_buttons)
    return markup_2008
# Inline клавиатура для видов литератур госта 2018
def markup_2018():
    markup_g2018_buttons = [[InlineKeyboardButton(text="Журнал",callback_data="2018_journal"),
                             InlineKeyboardButton(text="Книга",callback_data="2018_book"),
                             InlineKeyboardButton(text="Интернет ресурс",callback_data="2018_ethres")],
                            [InlineKeyboardButton(text="Автореферат",callback_data="2018_aftoref"),
                             InlineKeyboardButton(text="Диссертация",callback_data="2018_disert")],
                            [InlineKeyboardButton(text="back",callback_data="back")]]
    markup_2018 = InlineKeyboardMarkup(keyboard=markup_g2018_buttons)
    return markup_2018

# Inline клавиатура для видов книг госта 2003
def book_2003():
    markup_book_2003_buttons = [[InlineKeyboardButton(text="Книга - обыч.",callback_data="2003_book_normal")],
                                [InlineKeyboardButton(text="Том из многотомного издания",callback_data="2003_mnogotom")],
                                [InlineKeyboardButton(text="back",callback_data="back")]]
    markup_book_2003 = InlineKeyboardMarkup(keyboard=markup_book_2003_buttons)
    return markup_book_2003

# Inline клавиатура для видов многотомных книг госта 2003
def book_mnogotom_2003():
    markup_book_mnogotom_2003_buttons = [[InlineKeyboardButton(text="По томам",callback_data="2003_mnogotom_toms")],
                                         [InlineKeyboardButton(text="По частям",callback_data="2003_mnogotom_chapters")],
                                         [InlineKeyboardButton(text="back",callback_data="back")]]
    markup_book_mnogotom_2003 = InlineKeyboardMarkup(keyboard=markup_book_mnogotom_2003_buttons)
    return markup_book_mnogotom_2003

# Inline клавиатура для видов законодательных материалов госта 2003
def zakon_2003():
    markup_zakon_2003_buttons = [[InlineKeyboardButton(text="Федеральный документ",callback_data="2003_zakun_document")],
                                 [InlineKeyboardButton(text="Федеральный закон",callback_data="2003_zakun_federation")],
                                 [InlineKeyboardButton(text="Федеральный закон(интернет рес.)",callback_data="2003_zakun_federation_eth")],
                                 [InlineKeyboardButton(text="Постановление",callback_data="2003_zakun_postan")],
                                 [InlineKeyboardButton(text="back",callback_data="back")]]
    markup_zakon_2003 = InlineKeyboardMarkup(keyboard=markup_zakon_2003_buttons)
    return markup_zakon_2003

# Inline клавиатура для видов книг госта 2008
def book_2008():
    markup_book_2008_buttons = [[InlineKeyboardButton(text="Книга - Обыч.",callback_data="2008_book_normal"),
                                 InlineKeyboardButton(text="Книга - ЭБС",callback_data="2008_book_EBC")],
                                [InlineKeyboardButton(text="Том из многотомного издания",callback_data="2008_tom_iz_mnogotom")],
                                [InlineKeyboardButton(text="back",callback_data="back")]]
    markup_book_2008 = InlineKeyboardMarkup(keyboard=markup_book_2008_buttons)
    return markup_book_2008

# Inline клавиатура для видов книг госта 2018
def book_2018():
    markup_book_2018_buttons = [[InlineKeyboardButton(text="Книга - Обыч.",callback_data="2018_book_normal")],
                                [InlineKeyboardButton(text="Том из многотомного издания",callback_data="2018_tom_iz_mnogotom")],
                                [InlineKeyboardButton(text="back",callback_data="back")]]
    markup_book_2018 = InlineKeyboardMarkup(keyboard=markup_book_2018_buttons)
    return markup_book_2018

# Специальная одиночная кнопка back для неразработанных участков кода
def back():
    back_button = [[InlineKeyboardButton(text="back",callback_data="back")]]
    back_menu = InlineKeyboardMarkup(keyboard=back_button)
    return back_menu


