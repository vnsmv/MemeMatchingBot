import argparse

from memeder.database.connect import connect_to_db


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True, type=str, choices=('test', 'deploy'))
    args = parser.parse_known_args()[0]

    if args.host == 'test':
        cursor, connection = connect_to_db(env_file='db_credentials_test.env')
    else:  # args.host == 'deploy':
        cursor, connection = connect_to_db(env_file='db_credentials.env')

    sql_query = """ALTER TABLE user_proposals ALTER COLUMN chat_id TYPE BIGINT;
    ALTER TABLE user_proposals ALTER COLUMN rec_chat_id TYPE BIGINT;
    ALTER TABLE meme_proposals ALTER COLUMN chat_id TYPE BIGINT;
    ALTER TABLE users_memes ALTER COLUMN chat_id TYPE BIGINT;
    ALTER TABLE users_users ALTER COLUMN user_id TYPE BIGINT;
    ALTER TABLE users_users ALTER COLUMN rec_user_id TYPE BIGINT;
    ALTER TABLE users ALTER COLUMN telegram_id TYPE BIGINT;
    ALTER TABLE users ALTER COLUMN chat_id TYPE BIGINT;"""
    try:
        cursor.execute(sql_query)
    except Exception:
        cursor.execute('ROLLBACK')

    connection.commit()
    connection.close()


if __name__ == '__main__':
    main()
