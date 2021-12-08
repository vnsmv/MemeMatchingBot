import logging
from datetime import datetime

from memeder.database.connect import connect_to_db
from memeder.interface_tg.config import REACTIONS2BUTTONS


def user_exist(chat_id):
    cursor, connection = connect_to_db()
    sql_query = """SELECT EXISTS (SELECT 1 FROM users WHERE chat_id = %s) """

    try:
        cursor.execute(sql_query, (chat_id,))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    connection.commit()
    is_exist = cursor.fetchone()[0]
    connection.close()

    return is_exist


def add_user(tg_first_name, tg_id, tg_username, tg_chat_id, user_bio):
    # TODO: do we need to invoke a connection every time?
    cursor, connection = connect_to_db()
    sql_query = """INSERT INTO users (name, user_bio, telegram_id, telegram_username, chat_id, date_add, last_meme)  VALUES  ( %s, %s, %s, %s, %s, %s, %s)"""

    try:
        date_add = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cursor.execute(sql_query, (tg_first_name, user_bio, tg_id, tg_username, tg_chat_id, date_add, 0))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()
    return True


def get_last_meme_id(chat_id):
    cursor, connection = connect_to_db()
    sql_query = """ SELECT last_meme FROM users WHERE  chat_id = %s"""
    try:
        cursor.execute(sql_query, (chat_id,))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")
    last_meme_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return last_meme_id


def add_meme(file_id: str, chat_id: int, file_type: str):
    cursor, connection = connect_to_db()
    sql_query = """INSERT INTO memes (file_id, author_id, create_date, file_type)  VALUES  ( %s, %s, %s, %s)"""

    try:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cursor.execute(sql_query, (file_id, chat_id, date, file_type))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()


def add_user_meme_init(chat_id, meme_id, message_id):
    cursor, connection = connect_to_db()
    sql_query = """INSERT INTO users_memes (chat_id, memes_id, reaction, date, message_id) VALUES  (%s, %s, %s, %s, %s)"""

    try:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cursor.execute(sql_query, (chat_id, meme_id, REACTIONS2BUTTONS['DB_EMPTY'][1], date, message_id))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()


def add_user_meme_reaction(chat_id, message_id, reaction):
    cursor, connection = connect_to_db()

    sql_query = """UPDATE users_memes SET (reaction, date) = ( %s, %s) WHERE chat_id = %s AND message_id = %s"""
    try:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cursor.execute(sql_query, (reaction, date, chat_id, message_id))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()


def get_seen_meme_ids(chat_id):
    cursor, connection = connect_to_db()

    sql_query = """SELECT memes_id FROM users_memes WHERE chat_id = %s"""
    try:
        cursor.execute(sql_query, (chat_id, ))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    seen_memes = cursor.fetchall()

    connection.commit()
    connection.close()
    return seen_memes


def get_all_meme_ids():
    cursor, connection = connect_to_db()

    sql_query = """SELECT id, file_id FROM memes"""
    try:
        cursor.execute(sql_query)
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    all_meme_ids = cursor.fetchall()
    connection.commit()
    connection.close()
    return all_meme_ids


# Test functions
if __name__ == '__main__':
    # add_user('sdfsdf', 123, 123, 123, 'dfs_askask', 'bio')
    print(user_exist('followthesun'))
    pass
