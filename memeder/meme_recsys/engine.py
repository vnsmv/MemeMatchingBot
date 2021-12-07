import os
import random
import numpy as np

from memeder.database.db_functions import get_seen_meme_ids, get_all_meme_ids


def recommend_meme(chat_id):
    all_meme_ids = get_all_meme_ids()
    if not all_meme_ids:
        return None

    seen_meme_ids = get_seen_meme_ids(chat_id=chat_id)

    meme_ids, file_ids = np.array(all_meme_ids).T
    if not seen_meme_ids:
        meme_id = np.random.choice(meme_ids)[0]
    else:
        unseen_meme_ids = list(set(meme_ids.tolist()) - set(np.array(seen_meme_ids).squeeze(-1).tolist()))
        if not unseen_meme_ids:
            meme_id = np.random.choice(meme_ids)[0]
        else:
            meme_id = np.random.choice(unseen_meme_ids)

    return meme_id, file_ids[meme_ids == meme_id][0]

