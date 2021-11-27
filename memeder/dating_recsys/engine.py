import numpy as np

from memeder.database_csv.users_db import _read_create_users_db
from memeder.database_csv.sent_memes_db import _read_create_sent_memes_db


def is_ready_to_date(chat_id: int, memes_per_dating: int = 10, database_src: str = 'database_csv') -> bool:
    sent_memes_db = _read_create_sent_memes_db(database_src=database_src)
    user_sent_memes_sub_db = sent_memes_db.loc[chat_id]
    return (len(user_sent_memes_sub_db) > 0) and (len(user_sent_memes_sub_db) % memes_per_dating == 0)


def recommend_date(chat_id, database_src: str = 'database_csv'):
    users_db = _read_create_users_db(database_src=database_src)
    # users = set(users_db.index.tolist()) - {chat_id}
    users = set(users_db.index.tolist())
    recommended_users = np.random.choice(list(users), size=3)
    return np.unique(recommended_users).tolist()
