import argparse
import time

import numpy as np

from memeder.database.connect import connect_to_db
from memeder.interface_tg.config import MEME_BUTTONS
from memeder.meme_recsys.run_train_recsys import REACTION2VALUE


def update_top_memes(env_file: str = None,
                     top_n_memes: int = 100, min_reactions_th: int = 3, min_avg_rating_th: float = 1):

    cursor, connection = connect_to_db(env_file=env_file)
    q = """SELECT memes_id, reaction FROM users_memes WHERE reaction != %s AND reaction != %s;"""
    cursor.execute(q, (MEME_BUTTONS['DB_EMPTY'][1], MEME_BUTTONS['bu_users'][1]))
    meme_ids, reactions = np.array(cursor.fetchall()).T
    connection.commit()
    connection.close()

    meme_ids = np.int64(meme_ids)
    reactions = np.float32(list(map(lambda x: REACTION2VALUE[x], reactions)))

    unique_meme_ids, meme_id_counts = np.unique(meme_ids, return_counts=True)

    unique_meme_ids = unique_meme_ids[meme_id_counts >= min_reactions_th]
    meme_id_counts = meme_id_counts[meme_id_counts >= min_reactions_th]

    avg_rating = np.float32([np.mean(reactions[meme_ids == i]) for i in unique_meme_ids])

    unique_meme_ids = unique_meme_ids[avg_rating >= min_avg_rating_th]
    meme_id_counts = meme_id_counts[avg_rating >= min_avg_rating_th]
    avg_rating = avg_rating[avg_rating >= min_avg_rating_th]

    sorted_idxs = np.argsort(avg_rating)[::-1][:top_n_memes]
    top_memes = unique_meme_ids[sorted_idxs]
    top_counts = meme_id_counts[sorted_idxs]
    top_ratings = avg_rating[sorted_idxs]

    cursor, connection = connect_to_db(env_file=env_file)
    q_del = "DELETE FROM top_memes;"
    cursor.execute(q_del)

    q_add = "INSERT INTO top_memes (meme_id, n_reactions, avg_rating) VALUES"
    add_values = []
    for meme_id, meme_counts, meme_avg_rating in zip(top_memes, top_counts, top_ratings):
        q_add += " (%s, %s, %s),"
        add_values += [int(meme_id), int(meme_counts), float(meme_avg_rating)]
    q_add = q_add.strip(',') + ';'
    cursor.execute(q_add, add_values)

    connection.commit()
    connection.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True, type=str, choices=('test', 'deploy'))
    args = parser.parse_known_args()[0]

    if args.host == 'test':
        env_file = 'db_credentials_test.env'
    else:  # args.host == 'deploy':
        env_file = 'db_credentials.env'

    retrain_interval_min = 60
    t_retrain = retrain_interval_min * 60

    while True:
        print('>>> Run top memes selection...', flush=True)
        t_start = time.perf_counter()
        update_top_memes(env_file=env_file, top_n_memes=200)
        t_finish = time.perf_counter()
        t_train = int(np.round(t_finish - t_start))
        print(f'>>> Finish top memes selection (in {t_train} s)...', flush=True)
        print(flush=True)

        time.sleep(t_retrain)


if __name__ == '__main__':
    main()
