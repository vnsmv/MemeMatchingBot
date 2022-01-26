import logging
from datetime import datetime

import numpy as np

from memeder.database.connect import connect_to_db
from memeder.interface_tg.config import MEME_REACTION2BUTTON, USER_REACTION2BUTTON


def user_exist(chat_id):
    cursor, connection = connect_to_db()

    sql_query = """SELECT EXISTS (SELECT 1 FROM users WHERE chat_id = %s)"""
    try:
        cursor.execute(sql_query, (chat_id,))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    connection.commit()
    is_exist = cursor.fetchone()[0]
    connection.close()
    return is_exist


def add_user(tg_first_name, tg_id, tg_username, tg_chat_id):
    cursor, connection = connect_to_db()

    date_add = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    sql_query = """INSERT INTO users (name, telegram_id, telegram_username, chat_id, date_add, is_fresh)
    VALUES (%s, %s, %s, %s, %s, %s)"""
    try:
        cursor.execute(sql_query, (tg_first_name, tg_id, tg_username, tg_chat_id, date_add, True))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    sql_query = """INSERT INTO profiles (chat_id, preferences, goals, bio, use_bio, bio_update_flag, 
        photo_id, photo_unique_id, use_photo, photo_update_flag, sex)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    try:
        cursor.execute(sql_query, (tg_chat_id, 3003, 4003, '', False, False, '', '', False, False, 5002))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()


def update_profile(chat_id, column, value):
    cursor, connection = connect_to_db()

    q = f"UPDATE profiles SET {column} = %s WHERE chat_id = %s;"
    try:
        cursor.execute(q, (value, chat_id))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()


def add_meme(file_id: str, file_unique_id: str, chat_id: int, file_type: str):
    cursor, connection = connect_to_db()

    sql_query = """SELECT file_id FROM memes"""
    try:
        cursor.execute(sql_query)
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    file_ids = cursor.fetchall()
    if (not file_ids) or (file_id not in np.array(file_ids).squeeze(-1)):
        sql_query = """INSERT INTO memes (file_id, file_unique_id, author_id, create_date, file_type) 
        VALUES (%s, %s, %s, %s, %s)"""
        try:
            date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            cursor.execute(sql_query, (file_id, file_unique_id, chat_id, date, file_type))
        except Exception as e:
            logging.exception(e)
            cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()


def add_user_meme_init(chat_id, meme_id, message_id):
    cursor, connection = connect_to_db()
    sql_query = """INSERT INTO users_memes (chat_id, memes_id, reaction, date, message_id) VALUES (%s, %s, %s, %s, %s)"""

    try:
        date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        cursor.execute(sql_query, (chat_id, meme_id, MEME_REACTION2BUTTON['DB_EMPTY'][1], date, message_id))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()


def add_user_meme_reaction(chat_id, message_id, reaction):
    cursor, connection = connect_to_db()

    # 1. Check existing reaction:
    sql_query = """SELECT reaction FROM users_memes WHERE chat_id = %s AND message_id = %s"""
    try:
        cursor.execute(sql_query, (chat_id, message_id))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")
    existing_reaction = cursor.fetchone()

    # 2. Update empty reaction:
    if existing_reaction is None:
        logging.exception(f'add_user_meme_reaction: '
                          f'Updating empty reaction: {chat_id}, {message_id}, {reaction}.')
    else:
        if existing_reaction[0] == MEME_REACTION2BUTTON['DB_EMPTY'][1]:
            sql_query = """UPDATE users_memes SET (reaction, date_reaction) = (%s, %s)
            WHERE chat_id = %s AND message_id = %s"""
            try:
                date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                cursor.execute(sql_query, (reaction, date, chat_id, message_id))
            except Exception as e:
                logging.exception(e)
                cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()


def add_user_user_init(chat_id_obj, chat_id_subj, message_id):
    cursor, connection = connect_to_db()

    sql_query = """SELECT reaction FROM users_users WHERE user_id = %s AND rec_user_id = %s"""
    try:
        cursor.execute(sql_query, (chat_id_obj, chat_id_subj))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")
    existing_reaction_ij = cursor.fetchone()

    date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    if existing_reaction_ij is None:
        sql_query = """INSERT INTO users_users (user_id, rec_user_id, reaction, date, message_id)
        VALUES (%s, %s, %s, %s, %s)"""
        try:
            cursor.execute(sql_query, (chat_id_obj, chat_id_subj, USER_REACTION2BUTTON['DB_PENDING'][1], date,
                                       message_id))
        except Exception as e:
            logging.exception(e)
            cursor.execute("ROLLBACK")
    else:
        logging.exception(f'add_user_user_init: '
                          f'Initializing existing reaction: {existing_reaction_ij}, {chat_id_obj}, {chat_id_subj}, '
                          f'{date}.')

    connection.commit()
    connection.close()


def add_user_user_reaction(chat_id_obj, message_id, reaction):
    cursor, connection = connect_to_db()

    # 1. Check existing reaction:
    sql_query = """SELECT reaction FROM users_users WHERE user_id = %s AND message_id = %s"""
    try:
        cursor.execute(sql_query, (chat_id_obj, message_id))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")
    existing_reaction = cursor.fetchall()

    date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    if len(existing_reaction) == 0:
        logging.exception(f'Updating empty reaction: {chat_id_obj}, {message_id}, {reaction}, {date}.')
    elif existing_reaction[-1][0] != USER_REACTION2BUTTON['DB_PENDING'][1]:
        logging.exception(f'Updating final reaction: {chat_id_obj}, {message_id}, {reaction}, '
                          f'{existing_reaction}, {date}.')
    else:
        sql_query = """UPDATE users_users SET (reaction, date_reaction) = ( %s, %s)
                    WHERE user_id = %s AND message_id = %s"""
        try:
            cursor.execute(sql_query, (reaction, date, chat_id_obj, message_id))
        except Exception as e:
            logging.exception(e)
            cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()


def get_seen_meme_ids(chat_id):
    cursor, connection = connect_to_db()

    sql_query = """SELECT memes_id FROM users_memes WHERE chat_id = %s AND reaction != %s"""
    try:
        cursor.execute(sql_query, (chat_id, MEME_REACTION2BUTTON['DB_EMPTY'][1]))
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


def get_top_meme_ids():
    cursor, connection = connect_to_db()

    sql_query = """SELECT meme_id FROM top_memes"""
    try:
        cursor.execute(sql_query)
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    top_memes = cursor.fetchall()

    connection.commit()
    connection.close()
    return top_memes


def get_profile_value(chat_id, column):
    cursor, connection = connect_to_db()

    q = f'SELECT {column} FROM profiles WHERE chat_id = %s;'
    try:
        cursor.execute(q, (chat_id, ))
    except Exception as e:
        logging.exception(e)
        cursor.execute("ROLLBACK")

    connection.commit()
    value = cursor.fetchone()[0]
    connection.close()
    return value
