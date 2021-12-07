from memeder.database.connect import connect_to_db


def user_exist(tg_username):
    cursor, connection = connect_to_db()
    sql_query = """SELECT EXISTS (SELECT 1 FROM users WHERE telegram_username = %s) """

    try:
        cursor.execute(sql_query, (tg_username,))
    except Exception as e:
        print(e)
        cursor.execute("ROLLBACK")
    connection.commit()
    is_exist = cursor.fetchone()[0]
    connection.close()
    # returns False if tg_username don't in database
    return is_exist

def get_last_meme_id(chat_id):
    cursor, connection = connect_to_db()
    sql_query = """ SELECT last_meme FROM users WHERE  chat_id = %s"""
    try:
        cursor.execute(sql_query, (chat_id,))
    except Exception as e:
        print(e)
        cursor.execute("ROLLBACK")
    last_meme_id = cursor.fetchone()[0]
    connection.commit()
    connection.close()
    return chat_id


def add_meme(id_meme, date, author_id):
    cursor, connection = connect_to_db()
    sql_query = """INSERT INTO memes (tg_id, author_id, create_date)  VALUES  ( %s, %s, %s)"""

    try:
        cursor.execute(sql_query, (id_meme, author_id, date))
    except Exception as e:
        print(e)
        cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()
    return True


def add_meme_reaction(chat_id, meme_id, reaction, date):
    cursor, connection = connect_to_db()
    sql_query = """INSERT INTO users_memes (chat_id, memes_id, reaction, date) VALUES  ( %s, %s, %s, %s)"""

    try:
        cursor.execute(sql_query, (chat_id, meme_id, reaction, date))
    except Exception as e:
        print(e)
        cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()
    return True


def add_user(tg_first_name, tg_id, tg_username, tg_chat_id, date_add, user_bio):
    cursor, connection = connect_to_db()
    sql_query = """INSERT INTO users (name, user_bio, telegram_id, telegram_username, chat_id, date_add, last_meme)  VALUES  ( %s, %s, %s, %s, %s, %s, %s)"""

    try:
        cursor.execute(sql_query, (tg_first_name, user_bio, tg_id, tg_username, tg_chat_id, date_add, 0))
    except Exception as e:
        print(e)
        cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()
    return True


def recommended_meme_id(chat_id):

    cursor, connection = connect_to_db()
    sql_query = """ SELECT last_meme FROM users WHERE  chat_id = %s"""
    try:
        cursor.execute(sql_query, (chat_id,))
    except Exception as e:
        print(e)
        cursor.execute("ROLLBACK")

    last_meme_id = cursor.fetchone()[0]
    connection.commit()

    recommended_id = last_meme_id + 1

    sql_query = """ SELECT tg_id FROM memes WHERE  id = %s"""

    cursor.execute(sql_query, (recommended_id,))

    if cursor.fetchone() == None:

        sql_query = """ UPDATE users SET last_meme = %s WHERE chat_id = %s"""
        cursor.execute(sql_query, (0, chat_id))
        connection.commit()
        sql_query = """ SELECT tg_id FROM memes WHERE  id = %s"""
        cursor.execute(sql_query, (1,))
        recommended_tg_id = cursor.fetchone()[0]
    else:
        sql_query = """ SELECT tg_id FROM memes WHERE  id = %s"""
        cursor.execute(sql_query, (recommended_id,))
        recommended_tg_id = cursor.fetchone()[0]

    sql_query = """ UPDATE users SET last_meme = %s WHERE chat_id = %s"""

    try:
        cursor.execute(sql_query, (recommended_id, chat_id))
    except Exception as e:
        print(e)
        cursor.execute("ROLLBACK")

    connection.commit()
    connection.close()
    return recommended_tg_id

# Test functions
if __name__ == '__main__':
    # add_user('sdfsdf', 123, 123, 123, 'dfs_askask', 'bio')
    print(user_exist('followthesun'))
    pass