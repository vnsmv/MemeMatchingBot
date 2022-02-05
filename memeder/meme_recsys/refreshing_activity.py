import datetime

import numpy as np

from memeder.database.connect import connect_to_db
from memeder.interface_tg.config import MEME_BUTTONS
from memeder.meme_recsys.run_train_recsys import REACTION2VALUE


def is_sending_meme(chat_id,
                    time_delta: datetime.timedelta = datetime.timedelta(days=2),
                    return_delta: bool = False):
    cursor, connection = connect_to_db()

    q = "SELECT date FROM users_memes WHERE chat_id = %s ORDER BY date DESC;"
    cursor.execute(q, (chat_id, ))
    last_meme_reaction_date = cursor.fetchone()

    q = "SELECT date FROM users_users WHERE user_id = %s ORDER BY date DESC;"
    cursor.execute(q, (chat_id, ))
    last_user_reaction_date = cursor.fetchone()

    connection.commit()
    connection.close()

    curr_date = datetime.datetime.now()

    if (last_meme_reaction_date is None) and (last_user_reaction_date is None):
        delta = None
    elif last_meme_reaction_date is not None:
        delta = curr_date - last_meme_reaction_date[0]
    elif last_user_reaction_date is not None:
        delta = curr_date - last_user_reaction_date[0]
    else:
        delta = curr_date - np.max(last_meme_reaction_date[0], last_user_reaction_date[0])

    if delta is None:
        sending_meme_status = True
    else:
        sending_meme_status = delta >= time_delta

    return (sending_meme_status, delta) if return_delta else sending_meme_status


def top_memes_selection(top_n_memes: int = 500, min_reactions_th: int = 3, min_avg_rating_th: float = 0):
    cursor, connection = connect_to_db()
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

    return top_memes, top_counts, top_ratings


def select_meme(chat_id, top_meme_ids):
    cursor, connection = connect_to_db()

    q = "SELECT memes_id FROM users_memes WHERE chat_id = %s AND reaction != %s;"
    cursor.execute(q, (chat_id, MEME_BUTTONS['bu_users'][1]))

    seen_memes = cursor.fetchall()
    if seen_memes:
        seen_memes = np.array(seen_memes).ravel().tolist()
    else:
        seen_memes = []

    for meme_id in top_meme_ids:
        if meme_id not in seen_memes:
            meme_id = int(meme_id)
            q = "SELECT file_id FROM memes WHERE id = %s;"
            cursor.execute(q, (meme_id, ))
            file_id = cursor.fetchone()[0]

            connection.commit()
            connection.close()

            return meme_id, file_id

    connection.commit()
    connection.close()

    return None, None
