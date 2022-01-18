import time

import numpy as np

from memeder.database.connect import connect_to_db
from memeder.interface_tg.config import MEME_REACTION2BUTTON
from memeder.meme_recsys.run_train_recsys import REACTION2VALUE


def top_memes_selection(top_n_memes: int = 100, min_reactions_th: int = 2, min_avg_rating_th: float = 0.1):
    cursor, connection = connect_to_db()

    q = """SELECT memes_id, reaction FROM users_memes WHERE reaction != %s AND reaction != %s;"""
    cursor.execute(q, (MEME_REACTION2BUTTON['DB_EMPTY'][1], MEME_REACTION2BUTTON['bu_users'][1]))

    meme_ids, reactions = np.array(cursor.fetchall()).T
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

    q_del = "DELETE FROM top_memes;"
    cursor.execute(q_del)
    for meme_id, meme_counts, meme_avg_rating in zip(top_memes, top_counts, top_ratings):
        q_add = "INSERT INTO top_memes (meme_id, n_reactions, avg_rating) VALUES (%s, %s, %s);"
        cursor.execute(q_add, (int(meme_id), int(meme_counts), float(meme_avg_rating)))

    connection.commit()
    connection.close()


def main():
    retrain_interval_min = 5
    t_retrain = retrain_interval_min * 60

    while True:
        print('>>> Run top memes selection...')
        t_start = time.perf_counter()
        top_memes_selection()
        t_finish = time.perf_counter()
        print('>>> Finish top memes selection...')
        print()

        t_train = int(np.round(t_finish - t_start))
        if t_train < t_retrain:
            time.sleep(t_retrain - t_train)


if __name__ == '__main__':
    main()
