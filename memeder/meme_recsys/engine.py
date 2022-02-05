import numpy as np

from memeder.database.db_functions import get_seen_meme_ids, get_all_meme_ids, get_top_meme_ids
from memeder.database.connect import connect_to_db


def get_random_meme() -> (int, str):
    all_meme_ids = get_all_meme_ids()
    meme_ids, file_ids = np.array(all_meme_ids).T
    rnd_idx = np.random.randint(len(meme_ids))
    meme_id, file_id = meme_ids[rnd_idx], file_ids[rnd_idx]
    return int(meme_id), str(file_id)


def meme_id2file_id(meme_id: int, cursor):
    q = "SELECT file_id FROM memes WHERE id = %s;"
    cursor.execute(q, (meme_id, ))
    file_id = cursor.fetchone()[0]
    return file_id


def chat_id2telegram_username_and_name(chat_id: int, cursor):
    q = "SELECT telegram_username, name FROM users WHERE chat_id = %s;"
    cursor.execute(q, (chat_id, ))
    telegram_username, name = cursor.fetchone()
    return telegram_username, name


def recommend_meme(chat_id, cold_start_n_meme: int = 20):

    cursor, connection = connect_to_db()

    # ### 1. Is cold start? ###
    q = "SELECT is_fresh FROM users WHERE chat_id = %s;"
    cursor.execute(q, (chat_id, ))
    is_fresh = cursor.fetchone()

    if (is_fresh is None) or is_fresh[0]:
        seen_meme_ids = get_seen_meme_ids(chat_id=chat_id)
        if seen_meme_ids:
            seen_meme_ids = np.array(seen_meme_ids).ravel().tolist()

        top_meme_ids = get_top_meme_ids()
        if top_meme_ids:
            top_meme_ids = np.array(top_meme_ids).ravel().tolist()

        ids_to_recommend = list(set(top_meme_ids) - set(seen_meme_ids))

        if ids_to_recommend:
            meme_id = int(np.random.choice(ids_to_recommend))
            file_id = meme_id2file_id(meme_id=meme_id, cursor=cursor)
        else:
            meme_id, file_id = get_random_meme()

        q = "SELECT memes_id FROM users_memes WHERE chat_id = %s;"
        cursor.execute(q, (chat_id, ))
        n_reactions = len(cursor.fetchall())

        if n_reactions >= cold_start_n_meme:
            q = "UPDATE users SET is_fresh = %s WHERE chat_id = %s"
            cursor.execute(q, (False, chat_id))

    else:
        q = "SELECT meme_id FROM meme_proposals WHERE chat_id = %s AND status = %s;"
        cursor.execute(q, (chat_id, 0))
        meme_id = cursor.fetchone()

        if meme_id is None:
            meme_id, file_id = get_random_meme()
        else:
            meme_id = meme_id[0]
            file_id = meme_id2file_id(meme_id=meme_id, cursor=cursor)
            q = "UPDATE meme_proposals SET status = %s WHERE chat_id = %s AND meme_id = %s"
            try:
                cursor.execute(q, (1, chat_id, meme_id))
            except Exception:
                # actually the table is being updated now:)
                pass

    connection.commit()
    connection.close()

    return meme_id, file_id


def recommend_user(chat_id, cold_start_n_meme: int = 20):
    cursor, connection = connect_to_db()

    # ### 1. Is cold start? ###
    q = "SELECT is_fresh FROM users WHERE chat_id = %s;"
    cursor.execute(q, (chat_id,))
    is_fresh = cursor.fetchone()

    # ### 2. Is sex specified? ###
    q = "SELECT sex FROM profiles WHERE chat_id = %s;"
    cursor.execute(q, (chat_id,))
    sex = cursor.fetchone()

    # ### 3. Is preference not memes? ###
    q = "SELECT preferences FROM profiles WHERE chat_id = %s;"
    cursor.execute(q, (chat_id,))
    preferences = cursor.fetchone()

    # ### 4. Is goal not memes? ###
    q = "SELECT goals FROM profiles WHERE chat_id = %s;"
    cursor.execute(q, (chat_id,))
    goals = cursor.fetchone()

    if (is_fresh is None) or is_fresh[0]:
        q = "SELECT memes_id FROM users_memes WHERE chat_id = %s;"
        cursor.execute(q, (chat_id,))
        n_reactions = len(cursor.fetchall())

        n_reactions_to_do = cold_start_n_meme - n_reactions + 1
        chat_id_rec = None
        similarity = None

    elif (sex is None) or (sex[0] == 5002):
        chat_id_rec, similarity, n_reactions_to_do = None, None, -2

    elif (preferences is None) or (preferences[0] == 3003):
        chat_id_rec, similarity, n_reactions_to_do = None, None, -3

    elif (goals is None) or (goals[0] == 4003):
        chat_id_rec, similarity, n_reactions_to_do = None, None, -4

    else:
        q = "SELECT rec_chat_id, similarity FROM user_proposals WHERE chat_id = %s AND status = %s;"
        cursor.execute(q, (chat_id, 0))
        chat_id_rec__similarity = cursor.fetchone()

        if chat_id_rec__similarity is None:
            chat_id_rec, similarity, n_reactions_to_do = None, None, -1
        else:
            chat_id_rec, similarity, n_reactions_to_do = chat_id_rec__similarity[0], chat_id_rec__similarity[1], 0
            q = "UPDATE user_proposals SET status = %s WHERE chat_id = %s AND rec_chat_id = %s"
            try:
                cursor.execute(q, (1, chat_id, chat_id_rec))
            except Exception:
                # actually the table is being updated now:)
                pass

    if chat_id_rec is None:
        telegram_username, name = None, None
    else:
        telegram_username, name = chat_id2telegram_username_and_name(chat_id=chat_id_rec, cursor=cursor)

    connection.commit()
    connection.close()

    return chat_id_rec, similarity, telegram_username, name, n_reactions_to_do
