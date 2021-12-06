from memeder.database.connect import connect_to_db


def user_exist(tg_username):

    cursor, connection = connect_to_db()
    sql_query = """SELECT EXISTS (SELECT 1 FROM users WHERE telegram_username = %s) """
    cursor.execute(sql_query, (tg_username,))
    connection.commit()
    # returns False if tg_username don't in database
    return cursor.fetchone()[0]


def add_meme_reactions():

    pass


def add_user(tg_first_name, tg_id, tg_username, tg_chat_id, date_add, user_bio):
    cursor, connection = connect_to_db()
    sql_query = """INSERT INTO users (name, user_bio, telegram_id, telegram_username, chat_id, date_add)  VALUES  ( %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql_query, (tg_first_name, user_bio, tg_id, tg_username, tg_chat_id, date_add))
    connection.commit()
    return True


# Test functions
if __name__ == '__main__':
    # add_user('sdfsdf', 123, 123, 123, 'dfs_askask', 'bio')
    # if_exist = check_if_exist('hui')
    # print(if_exist)
    pass