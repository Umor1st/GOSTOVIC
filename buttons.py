from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_markup(mk_dict_arr):
    buttons = []
    for row in mk_dict_arr:
        row_arr = []
        for button_text, button_callback in row.items():
            row_arr.append(InlineKeyboardButton(
                text=button_text, callback_data=button_callback))
        buttons.append(row_arr)
    return buttons


def markup_main():
    markup_buttons = generate_markup([{"Cтудент": "Student",
                       "Ученик": "School"},
                      {"stop": "back"}])
    return InlineKeyboardMarkup(keyboard=markup_buttons)

# Inline клавиатура для видов годов


def markup_years():
    markup_buttons = generate_markup([{"2003": "2003",
                       "2008": "2008",
                       "2018": "2018"},
                      {"back": "back"}])
    return InlineKeyboardMarkup(keyboard=markup_buttons)

# Inline клавиатура для видов литератур госта 2003


def markup_2003():
    markup_buttons = generate_markup([{"Журнал": "2003_journal",
                       "Книга": "2003_book",
                       "Интернет ресурс": "2003_ethres"},
                      {"Диссертация": "2003_disert",
                       "Автореферат": "2003_autoref"},
                      {"Законодательные материалы": "2003_zakun"},
                      {"back": "back"}])
    return InlineKeyboardMarkup(keyboard=markup_buttons)

# Inline клавиатура для видов литератур госта 2008


def markup_2008():
    markup_buttons = generate_markup([{"Журнал": "2008_journal",
                       "Книга": "2008_book",
                       "Интернет ресурс": "2008_ethres"},
                      {"Автореферат": "2008_aftoref",
                       "Диссертация": "2008_disert"},
                      {"back": "back"}])

    return InlineKeyboardMarkup(keyboard=markup_buttons)

# Inline клавиатура для видов литератур госта 2018


def markup_2018():
    markup_buttons = generate_markup([{"Журнал": "2018_journal",
                       "Книга": "2018_book",
                       "Интернет ресурс": "2018_ethres"},
                      {"Автореферат": "2018_aftoref",
                       "Диссертация": "2018_disert"},
                      {"back": "back"}])

    return InlineKeyboardMarkup(keyboard=markup_buttons)

# Inline клавиатура для видов книг госта 2003


def book_2003():
    markup_buttons = generate_markup([{"Книга - обыч.": "2003_book_normal"},
                      {"Том из многотомного издания": "2003_mnogotom"},
                      {"back": "back"}])

    return InlineKeyboardMarkup(keyboard=markup_buttons)

# Inline клавиатура для видов многотомных книг госта 2003


def book_mnogotom_2003():
    markup_buttons = generate_markup([{"По томам": "2003_mnogotom_toms"},
                      {"По частям": "2003_mnogotom_chapters"},
                      {"back": "back"}])

    return InlineKeyboardMarkup(keyboard=markup_buttons)

# Inline клавиатура для видов законодательных материалов госта 2003


def zakon_2003():
    markup_buttons = generate_markup([{"Федеральный документ": "2003_zakun_document"},
                      {"Федеральный закон": "2003_zakun_federation"},
                      {"Федеральный закон(интернет рес.)": "2003_zakun_federation_eth"},
                      {"Постановление": "2003_zakun_postan"},
                      {"back": "back"}])

    return InlineKeyboardMarkup(keyboard=markup_buttons)

# Inline клавиатура для видов книг госта 2008


def book_2008():
    markup_buttons = generate_markup([{"Книга - Обыч.": "2008_book_normal",
                       "Книга - ЭБС": "2008_book_EBC"},
                      {"Том из многотомного издания": "2008_tom_iz_mnogotom"},
                      {"back": "back"}])

    return InlineKeyboardMarkup(keyboard=markup_buttons)

# Inline клавиатура для видов книг госта 2018


def book_2018():
    markup_buttons = generate_markup([{"Книга - Обыч.": "2018_book_normal"},
                      {"Том из многотомного издания": "2018_tom_iz_mnogotom"},
                      {"back": "back"}])

    return InlineKeyboardMarkup(keyboard=markup_buttons)

# Специальная одиночная кнопка back для неразработанных участков кода


def back():
    back_button =generate_markup([{"back": "back"}])
    return InlineKeyboardMarkup(keyboard=back_button)
