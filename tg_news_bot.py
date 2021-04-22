import telebot
from telebot import types
import requests


token = " "  # Токен бота
api_url = "http://localhost:8080"
api_url_keywords = api_url + "/keywords"
api_url_categories = api_url + "/categories"
api_url_users = api_url + "/users"
api_url_news = api_url + "/news"
bot = telebot.TeleBot(token, parse_mode=None)
command_add_category = ('добавить категорию', 'добавить категории')
command_del_category = ('удалить категорию', 'удалить категории')
command_show_category = ('показать категории', 'показать категории')
command_add_keyword = ('добавить ключевые слова', 'добавить ключевое слово')
command_del_keyword = ('удалить ключевые слова', 'удалить ключевое слово')
command_show_keyword = ('показать ключевые слова')
command_show_news = ('показать новости')
query = {"command": '', "options": [], "user_id": ''}
help_text = """
Для взаимодействия с ботом жми на кнопки и следуй указаниям.
С помощью данного бота можно:
 - Подписаться на категорию
   Доступны следующие категории: <b>business, entertainment, general, health, science, sports, technology</b>
 - Удалить категории из подписок
 - Вывести список категорий, на которые вы подписаны
 - Подписаться на ключевые слова
 - Удалить ключевые слова из подписок
 - Вывести список ключевых слов, на которые вы подписаны
 - Показать подборку новостей
"""


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, help_text, parse_mode="html")


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    add_user(user_id)


def add_user(user_id):
    """Добавление пользователя в базу"""
    data = {'user_id': user_id}
    requests.post(url=api_url_users, data=data)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*create_list_btns(user_id))
    bot.send_message(user_id, f"""Привет!
Я помогу тебе получать только самые важные новости. 
Загляни в /help, чтобы посмотреть, что я умею""", reply_markup=keyboard)


def get_news(query):
    '''Получение Новостей'''
    user_id = query['user_id']
    data = {'user_id': user_id}
    r = requests.get(url=api_url_news, params=data)
    return r.json()


def show_keywords(query):
    '''Получение ключевых слов'''
    user_id = query['user_id']
    data = {'user_id': user_id}
    r = requests.get(url=api_url_keywords, params=data)
    return r.json()


def add_keywords(message):
    '''Добавление ключевых слов'''
    global query
    user_id = query['user_id']
    query['options'].extend(message.text.lower().split())
    options = query['options']
    data = {'user_id': user_id, 'name': options}
    r = requests.post(url=api_url_keywords, data=data)
    success = r.json()['success']
    fail = r.json()['fail']
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*create_list_btns(user_id))
    if len(success):
        bot.send_message(user_id, f'Вы успешно подписались на ключевые слова: {" ".join(success)}', reply_markup=keyboard)
    if len(fail):
        bot.send_message(user_id, f'Вы уже подписаны на ключевые слова: {" ".join(fail)}', reply_markup=keyboard)


def del_keywords(message):
    '''Удаление ключевых слов'''
    global query
    user_id = query['user_id']
    query['options'].extend(message.text.lower().split())
    options = query['options']
    data = {'user_id': user_id, 'name': options}
    r = requests.delete(url=api_url_keywords, data=data)
    success = r.json()['success']
    fail = r.json()['fail']
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*create_list_btns(user_id))
    if len(success):
        bot.send_message(user_id, f'Вы успешно удалили подписку на ключевые слова: {" ".join(success)}')
    if len(fail):
        bot.send_message(user_id, f'Вы не подписаны на ключевые слова: {" ".join(fail)}')


def show_categories(query):
    '''Получение категорий'''
    user_id = query['user_id']
    data = {'user_id': user_id}
    r = requests.get(url=api_url_categories, params=data)
    return r.json()


def add_categories(message):
    '''Добавление категорий'''
    global query
    user_id = query['user_id']
    query['options'].extend(message.text.lower().split())
    options = query['options']
    data = {'user_id': user_id, 'name': options}
    r = requests.post(url=api_url_categories, data=data)
    success = r.json()['success']
    fail = r.json()['fail']
    fail_invalid = r.json()['fail_invalid']
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*create_list_btns(user_id))
    if len(success):
        bot.send_message(user_id, f'Вы успешно подписались на категории: {" ".join(success)}', reply_markup=keyboard)
    if len(fail):
        bot.send_message(user_id, f'Вы уже подписаны на категории: {" ".join(fail)}', reply_markup=keyboard)
    if len(fail_invalid):
        bot.send_message(user_id, f'Недопустимое значение категории. {" ".join(fail)} Загляни в /help', reply_markup=keyboard)


def del_categories(message):
    '''Удаление категорий'''
    global query
    user_id = query['user_id']
    query['options'].extend(message.text.lower().split())
    options = query['options']
    data = {'user_id': user_id, 'name': options}
    r = requests.delete(url=api_url_categories, data=data)
    success = r.json()['success']
    fail = r.json()['fail']
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*create_list_btns(user_id))
    if len(success):
        bot.send_message(user_id, f'Вы успешно удалили подписку на категории: {" ".join(success)}', reply_markup=keyboard)
    if len(fail):
        bot.send_message(user_id, f'Вы не подписаны на категории: {" ".join(fail)}', reply_markup=keyboard)


def parse_msg(message):
    global query
    words = message.text.lower().split()
    key = ('ключевые', 'ключевое')
    if len(words) > 1:
        if words[1] in key:
            count_command = 3
        else:
            count_command = 2
        query = {"command": ' '.join(words[:count_command]), "options": words[count_command:],
                 "user_id": message.from_user.id}
    else:
        query = {'command': 'Неверная команда'}
    return query

def create_list_btns(user_id):
    btns = ["Показать новости", "Добавить категории", "Добавить ключевые слова"]
    query = {'user_id': user_id}
    if len(show_keywords(query)):
        btns.extend(["Показать ключевые слова", "Удалить ключевые слова"])
    if len(show_categories(query)):
        btns.extend(["Показать категории", "Удалить категории"])
    return btns


@bot.message_handler(func=lambda message: True)
def answer_to_message(message):
    global query
    query = parse_msg(message)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*create_list_btns(message.from_user.id))
    if query['command'] in command_add_category:
        msg = bot.send_message(query['user_id'], 'Введите категории через пробел. Доступны следующие категории: <b>business entertainment general health science sports technology</b>',parse_mode='html', reply_markup=keyboard)
        bot.register_next_step_handler(msg, add_categories)
    elif query['command'] in command_del_category:
        msg = bot.send_message(query['user_id'], 'Введите категории через пробел:', reply_markup=keyboard)
        bot.register_next_step_handler(msg, del_categories)
    elif query['command'] in command_show_category:
        if len(show_categories(query)):
            bot.send_message(message.from_user.id, f"Вы подписаны на категории: {' '.join(show_categories(query))}")
        else:
            bot.send_message(message.from_user.id, f"Вы не подписаны ни на одну категорию", reply_markup=keyboard)
    elif query['command'] in command_add_keyword:
        msg = bot.send_message(query['user_id'], 'Введите ключевые слова через пробел:', reply_markup=keyboard)
        bot.register_next_step_handler(msg, add_keywords)
    elif query['command'] in command_del_keyword:
        msg = bot.send_message(query['user_id'], 'Введите ключевые слова через пробел:', reply_markup=keyboard)
        bot.register_next_step_handler(msg, del_keywords)
    elif query['command'] in command_show_keyword:
        if len(show_keywords(query)):
            bot.send_message(message.from_user.id, f"Вы подписаны на ключевые слова: {' '.join(show_keywords(query))}")
        else:
            bot.send_message(message.from_user.id, f"Вы не подписаны ни на одно ключевое слово", reply_markup=keyboard)
    elif query['command'] in command_show_news:
            list_news = get_news(query)
            if len(list_news) > 0:
                for i in range(len(list_news)):
                    title = list_news[i]["title"]
                    description = list_news[i]["description"]
                    url = list_news[i]["url"]
                    urlToImage = list_news[i]["urlToImage"]
                    publishedAt = list_news[i]["publishedAt"]
                    content = list_news[i]["content"]
                    markup = types.InlineKeyboardMarkup()
                    btn_more = types.InlineKeyboardButton(text='Подробнее', url=url)
                    markup.add(btn_more)
                    if list_news[i]["urlToImage"]:
                        try:
                            bot.send_photo(message.from_user.id, urlToImage,
                                       f"{title} \n\n {description}\n", reply_markup=markup)
                        except Exception:
                            bot.send_message(message.from_user.id,
                                             f"{title}\n\n{description}\n", reply_markup=markup,
                                             disable_web_page_preview=True)
                    else:
                        bot.send_message(message.from_user.id,
                                         f"{title}\n\n{description}\n", reply_markup=markup,
                                         disable_web_page_preview=True)
            else:
                bot.send_message(message.from_user.id, f"К сожалению, по вашим подпискам нет новостей :-( ")
    else:
        bot.send_message(message.from_user.id, f"Команда не поддерживается. Загляни в /help")


bot.polling()
