import argparse

import numpy as np

from memeder.database.connect import connect_to_db


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True, type=str, choices=('test', 'deploy'))
    args = parser.parse_known_args()[0]

    if args.host == 'test':
        cursor, connection = connect_to_db(env_file='db_credentials_test.env')
        random = True
    else:  # args.host == 'deploy':
        cursor, connection = connect_to_db(env_file='db_credentials.env')
        random = False

    q = 'SELECT chat_id FROM users;'
    cursor.execute(q)
    users = np.array(cursor.fetchall()).ravel().tolist()

    q_add = "INSERT INTO profiles "
    q_add += "(chat_id, preferences, goals, bio, use_bio, bio_update_flag, "
    q_add += "photo_id, photo_unique_id, use_photo, photo_update_flag, sex) VALUES"
    add_values = []
    for chat_id in users:
        q_add += " (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),"
        add_values += [
            chat_id,
            # int(np.random.choice((2000, 2001, 2002, 2003))) if random else 2003,
            int(np.random.choice((3000, 3001, 3002, 3003))) if random else 3003,
            int(np.random.choice((4000, 4001, 4002, 4003))) if random else 4003,
            'Sample random bio' if random else '',
            bool(np.random.choice((True, False))) if random else False,
            False,
            '',
            '',
            False,
            False,
            int(np.random.choice((4000, 4001, 4002))) if random else 4002,
        ]
    q_add = q_add.strip(',') + ';'

    try:
        cursor.execute(q_add, tuple(add_values))
    except Exception:
        cursor.execute('ROLLBACK')

    connection.commit()
    connection.close()


if __name__ == '__main__':
    main()
