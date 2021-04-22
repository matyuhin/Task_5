from flask import Flask, request, jsonify
import sqlite3
from newsapi import NewsApiClient


api_key = " "  # Ключ newsapi.org
newsapi = NewsApiClient(api_key=api_key)
app = Flask(__name__)


def create_db():
    """Подключение к БД и создание таблиц"""
    try:
        sqlite_connection = sqlite3.connect('telenews.db')
        sqlite_create_table_users = '''CREATE TABLE IF NOT EXISTS users (
                                        id INTEGER PRIMARY KEY);'''
        sqlite_create_table_category = '''CREATE TABLE IF NOT EXISTS categories (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            name TEXT NOT NULL,
                                            user_id INTEGER SECONDARY KEY);'''
        sqlite_create_table_keywords = '''CREATE TABLE IF NOT EXISTS keywords (
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            name TEXT NOT NULL,
                                            user_id INTEGER SECONDARY KEY);'''

        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_users)
        cursor.execute(sqlite_create_table_category)
        cursor.execute(sqlite_create_table_keywords)
        sqlite_connection.commit()
        print("Таблица SQLite создана")
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def add_users(query):
    """Добавление пользователя в базу"""
    user_id = query['user_id']
    try:
        sqlite_connection = sqlite3.connect('telenews.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_with_param = """INSERT INTO users
                                      (id)
                                      VALUES (?);"""
        data_tuple = (user_id,)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        print("Запись успешно вставлена в таблицу users ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def check_exist(table, name, user_id):
    list_category = []
    rows = []
    try:
        sqlite_connection = sqlite3.connect('telenews.db')
        cursor = sqlite_connection.cursor()
        sqlite_show_with_param = f"""SELECT name FROM {table} WHERE name = ? AND user_id = ?"""
        data_tuple = (name, user_id)
        cursor.execute(sqlite_show_with_param, data_tuple)
        rows = cursor.fetchall()
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
        if len(rows) > 0:
            for item in rows:
                list_category.append(item[0])
    if len(list_category):
        return True
    else:
        return False


def show_keywords(user_id):
    """Просмотр списка ключевых слов из базы"""
    list_keyword = []
    rows = []
    try:
        sqlite_connection = sqlite3.connect('telenews.db')
        cursor = sqlite_connection.cursor()
        sqlite_query = f"""SELECT name FROM keywords WHERE user_id = {user_id}"""
        cursor.execute(sqlite_query)
        rows = cursor.fetchall()
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
        if len(rows) > 0:
            for item in rows:
                list_keyword.append(item[0])
    return list_keyword


def del_keywords(query):
    """Удаление ключевых слов из базы"""
    user_id = query['user_id']
    keywords = query['name']
    response_sql = {"success": [], "fail": []}
    for keyword in keywords:
        if check_exist('keywords', keyword, user_id):
            try:
                sqlite_connection = sqlite3.connect('telenews.db')
                cursor = sqlite_connection.cursor()
                sqlite_delete_with_param = """DELETE FROM keywords WHERE name = ? AND user_id = ?"""
                data_tuple = (keyword, user_id)
                cursor.execute(sqlite_delete_with_param, data_tuple)
                sqlite_connection.commit()
                response_sql["success"].append(keyword)
                print(f"Запись {keyword} успешно удалена из таблицы keywords", cursor.rowcount)
                cursor.close()
            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)
            finally:
                if sqlite_connection:
                    sqlite_connection.close()
                    print("Соединение с SQLite закрыто")
        else:
            response_sql["fail"].append(keyword)
    return response_sql


def add_keywords(query):
    """Добавление ключевых слов в базу"""
    user_id = query['user_id']
    keywords = query['name']
    # print(show_keyword(user_id))
    response_sql = {"success": [], "fail": []}
    for keyword in keywords:
        if not check_exist('keywords', keyword, user_id):
            try:
                sqlite_connection = sqlite3.connect('telenews.db')
                cursor = sqlite_connection.cursor()
                sqlite_insert_with_param = f"""INSERT INTO keywords
                                                  (name, user_id)
                                                  VALUES (?, ?);"""
                data_tuple = (keyword, user_id)
                cursor.execute(sqlite_insert_with_param, data_tuple)
                sqlite_connection.commit()
                response_sql["success"].append(keyword)
                print(f"Запись {keyword} успешно добавлена в таблицу keyword", cursor.rowcount)
                cursor.close()
            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)
            finally:
                if sqlite_connection:
                    sqlite_connection.close()
                    print("Соединение с SQLite закрыто")
        else:
            response_sql["fail"].append(keyword)
    return response_sql


def show_categories(user_id):
    """Просмотр списка категорий из базы"""
    list_category = []
    rows = []
    try:
        sqlite_connection = sqlite3.connect('telenews.db')
        cursor = sqlite_connection.cursor()
        sqlite_query = f"""SELECT name FROM categories WHERE user_id = {user_id}"""
        cursor.execute(sqlite_query)
        rows = cursor.fetchall()
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
        if len(rows) > 0:
            for item in rows:
                list_category.append(item[0])
    return list_category


def add_categories(query):
    """Добавление категории в базу"""
    user_id = query['user_id']
    categories = query['name']
    list_category = ("business", "entertainment", "general", "health", "science", "sports", "technology")
    response_sql = {"success": [], "fail": [], "fail_invalid": []}
    for category in categories:
        if category in list_category:
            if not check_exist('categories', category, user_id):
                try:
                    sqlite_connection = sqlite3.connect('telenews.db')
                    cursor = sqlite_connection.cursor()
                    sqlite_insert_with_param = """INSERT INTO categories
                                                      (name, user_id)
                                                      VALUES (?, ?);"""
                    data_tuple = (category, user_id)
                    cursor.execute(sqlite_insert_with_param, data_tuple)
                    sqlite_connection.commit()
                    response_sql["success"].append(category)
                    print(f"Запись {category} успешно добавлена в таблицу category", cursor.rowcount)
                    cursor.close()
                except sqlite3.Error as error:
                    print("Ошибка при работе с SQLite", error)
                finally:
                    if sqlite_connection:
                        sqlite_connection.close()
                        print("Соединение с SQLite закрыто")
            else:
                response_sql["fail"].append(category)
        else:
            response_sql["fail_invalid"].append(category)
    return response_sql


def del_categories(query):
    """Удаление категории из базы"""
    user_id = query['user_id']
    categories = query['name']
    response_sql = {"success": [], "fail": []}
    for category in categories:
        if check_exist('categories', category, user_id):
            try:
                sqlite_connection = sqlite3.connect('telenews.db')
                cursor = sqlite_connection.cursor()
                sqlite_delete_with_param = """DELETE FROM categories WHERE name = ? AND user_id = ?"""
                data_tuple = (category, user_id)
                cursor.execute(sqlite_delete_with_param, data_tuple)
                sqlite_connection.commit()
                response_sql["success"].append(category)
                print(f"Запись {category} успешно удалена из таблицы categories", cursor.rowcount)
                cursor.close()
            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)
            finally:
                if sqlite_connection:
                    sqlite_connection.close()
                    print("Соединение с SQLite закрыто")
        else:
            response_sql["fail"].append(category)
    return response_sql


@app.route('/keywords', methods=['GET', 'POST', 'DELETE'])
def keywords_rest():
    if request.method == 'POST':
        name = request.form.getlist('name')
        user_id = request.form['user_id']
        query = {"user_id": user_id, "name": name}
        return jsonify(add_keywords(query))
    elif request.method == 'DELETE':
        name = request.form.getlist('name')
        user_id = request.form['user_id']
        query = {"user_id": user_id, "name": name}
        return jsonify(del_keywords(query))
    else:
        user_id = request.args.get('user_id')
        return jsonify(show_keywords(user_id))


@app.route('/categories', methods=['GET', 'POST', 'DELETE'])
def categories_rest():
    if request.method == 'POST':
        # add_keywords()
        name = request.form.getlist('name')
        user_id = request.form['user_id']
        query = {"user_id": user_id, "name": name}
        # print(query)
        return jsonify(add_categories(query))
    elif request.method == 'DELETE':
        name = request.form.getlist('name')
        user_id = request.form['user_id']
        query = {"user_id": user_id, "name": name}
        return jsonify(del_categories(query))
    else:
        user_id = request.args.get('user_id')
        return jsonify(show_categories(user_id))


@app.route('/users', methods=['POST'])
def users_rest():
    if request.method == 'POST':
        name = request.form.getlist('name')
        user_id = request.form['user_id']
        query = {"user_id": user_id, "name": name}
        return jsonify(add_users(query))


@app.route('/news', methods=['GET'])
def news_rest():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        return jsonify(get_news(user_id))



def get_news(query):
    """Получение подборки новостей"""
    list_keywords = show_keywords(query)
    list_category = show_categories(query)
    list_sources = []
    list_news = []
    if len(list_category) > 0:
        for category in list_category:
            sources = newsapi.get_sources(category=category)
            print()
            for source in sources['sources']:
                list_sources.append(source['id'])
        response = newsapi.get_everything(
                                          q=' OR '.join(list_keywords),
                                          sources=','.join(list_sources),
                                          sort_by='relevancy',
                                          page_size=10
                                          )
    elif len(list_keywords) > 0:
        response = newsapi.get_everything(
            q=' OR '.join(list_keywords),
            sort_by='relevancy',
            page_size=10
        )
    else:
        response = {"articles": []}

    if len(response["articles"]) < 10:
        count_news = len(response["articles"])
    else:
        count_news = 10
    if len(response["articles"]) > 0:
        for i in range(count_news):
            list_news.append({
                "title": response["articles"][i]["title"],
                "description": response["articles"][i]["description"],
                "url": response["articles"][i]["url"],
                "urlToImage": response["articles"][i]["urlToImage"],
                "publishedAt": response["articles"][i]["publishedAt"],
                "content": response["articles"][i]["content"],
            })
    return list_news


create_db()

host = '0.0.0.0'
port = 8080
api_url = f"http://{host}:{port}"
if __name__ == '__main__':
    app.run(host=host, port=port)
    print(api_url)
