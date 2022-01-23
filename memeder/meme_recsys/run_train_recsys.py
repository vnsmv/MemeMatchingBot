import argparse
import time

import numpy as np
from scipy.sparse import coo_matrix
from scipy.spatial.distance import cdist

from memeder.database.connect import connect_to_db
from memeder.interface_tg.config import MEME_REACTION2BUTTON
from memeder.meme_recsys.matrix_factorization import unbiased_matrix_factorization


REACTION2VALUE = {'1001': -4, '107': -3, '106': -2, '105': -1, '104': 0,
                  '103': 1, '102': 2, '101': 3, '100': 4, '1000': 5}


def run_recommendation_train(env_file: str = None,
                             n_memes: int = 200, n_matches: int = 30,
                             personal_exploration_ratio=0.1, annotation_ratio=0.1, top_ratio=0.2,
                             seed=42):

    # TODO: try-except the cursor executions...

    # ### 1. Getting dataset: ###
    cursor, connection = connect_to_db(env_file=env_file)

    q1 = """SELECT chat_id FROM users"""
    cursor.execute(q1)
    chat_ids = [chat_id[0] for chat_id in cursor.fetchall()]

    q2 = """SELECT id FROM memes"""
    cursor.execute(q2)
    meme_ids = [meme_id[0] for meme_id in cursor.fetchall()]

    q3 = "SELECT chat_id, memes_id, reaction FROM users_memes WHERE reaction != %s AND reaction != %s;"
    cursor.execute(q3, (MEME_REACTION2BUTTON['DB_EMPTY'][1], MEME_REACTION2BUTTON['bu_users'][1]))
    users, items, reactions = np.array(cursor.fetchall()).T

    q4 = "SELECT meme_id FROM top_memes;"
    cursor.execute(q4)
    top_meme_ids = np.array(cursor.fetchall()).ravel()

    connection.commit()
    connection.close()

    users = np.int64(users)
    items = np.int64(items)

    chat_id2uid = {chat_id: uid for uid, chat_id in enumerate(chat_ids)}
    meme_id2iid = {meme_id: iid for iid, meme_id in enumerate(meme_ids)}

    users = np.array(list(map(lambda x: chat_id2uid[x], users)))
    items = np.array(list(map(lambda x: meme_id2iid[x], items)))

    for r, v in REACTION2VALUE.items():
        reactions[reactions == r] = v
    values = np.float32(reactions)

    # scaling to [-1, 1]
    values -= values.min()
    values /= values.max()
    values = (values - 0.5) * 2

    R = coo_matrix((values, (users, items)), shape=(len(chat_ids), len(meme_ids)))

    # ### 2. Training MF (matrix factorization): ###
    P, Q = unbiased_matrix_factorization(R, rank=3, num_epochs=10, lrate=0.07, reg=0.1, seed=seed)
    # TODO: should be retrained with other parameters with larger dataset!
    # TODO: run grid search!
    # val RMSE = 0.7757

    # ### 3. Getting memes recommendations: ###
    chat_id2recommended_meme_ids = {}
    uid2chat_id = {v: k for k, v in chat_id2uid.items()}
    iid2meme_id = {v: k for k, v in meme_id2iid.items()}
    iids = np.arange(len(meme_ids))
    globally_unseen_iids = list(set(iids) - set(np.unique(R.col).tolist()))
    top_iids = list(map(lambda x: meme_id2iid[x], top_meme_ids))

    for uid, u_p in enumerate(P):
        seen_iids = R.col[R.row == uid].tolist()
        unseen_iids = np.int64(list(set(iids.tolist()) - set(seen_iids)))
        unseen_top_iids = np.int64(list(set(top_iids) - set(seen_iids)))

        recommended_iids = iids[unseen_iids][np.argsort(u_p.dot(Q.T)[unseen_iids])[:-n_memes - 1:-1]]
        annotate_iids = np.random.choice(globally_unseen_iids, size=int(annotation_ratio * n_memes))
        random_iids = np.random.choice(unseen_iids, size=int(personal_exploration_ratio * n_memes))
        if len(unseen_top_iids) >= int(top_ratio * n_memes):
            unseen_top_iids = np.random.choice(unseen_top_iids, size=int(top_ratio * n_memes))

        recommended_meme_ids = list(map(lambda x: iid2meme_id[x], list(set(recommended_iids.tolist()
                                                                           + annotate_iids.tolist()
                                                                           + random_iids.tolist()
                                                                           + unseen_top_iids.tolist()))))
        chat_id2recommended_meme_ids[uid2chat_id[uid]] = recommended_meme_ids

    # ### 4. Getting users recommendations: ###
    users_similarity = cdist(P, P, metric='euclidean')

    cursor, connection = connect_to_db(env_file=env_file)
    q4 = """SELECT user_id, rec_user_id FROM users_users"""
    cursor.execute(q4)
    user_pairs = cursor.fetchall()
    connection.commit()
    connection.close()

    if user_pairs:
        users_obj, users_subj = np.array(user_pairs).T
        users_obj = np.array(list(map(lambda x: chat_id2uid[x], users_obj)) + np.arange(len(chat_ids)).tolist())
        users_subj = np.array(list(map(lambda x: chat_id2uid[x], users_subj)) + np.arange(len(chat_ids)).tolist())
        U = coo_matrix((np.ones_like(users_obj), (users_obj, users_subj)), shape=(len(chat_ids),) * 2)
    else:
        self_user_obj = np.arange(len(chat_ids))
        U = coo_matrix((np.ones_like(self_user_obj), (self_user_obj, self_user_obj)), shape=(len(chat_ids),) * 2)

    chat_id2recommended_chat_ids = {}
    uids = np.arange(len(chat_ids))
    for uid, u_s in enumerate(users_similarity):
        unseen_uids = np.int64(list(set(uids.tolist()) - set(U.getrow(uid).indices.tolist())))
        uids_flt = uids[unseen_uids]

        recommended_uids_flt = np.argsort(u_s[unseen_uids])[:n_matches]
        recommended_chat_ids = list(map(lambda x: uid2chat_id[x], uids_flt[recommended_uids_flt]))
        chat_id2recommended_chat_ids[uid2chat_id[uid]] = recommended_chat_ids

    # ### 5. Updating meme proposals: ###
    cursor, connection = connect_to_db(env_file=env_file)
    q_del = "DELETE FROM meme_proposals;"
    cursor.execute(q_del)

    q_add = "INSERT INTO meme_proposals (chat_id, meme_id, status) VALUES"
    add_values = []
    for chat_id, recommended_meme_ids in chat_id2recommended_meme_ids.items():
        for meme_id in recommended_meme_ids:
            q_add += " (%s, %s, %s),"
            add_values += [chat_id, meme_id, 0]
    q_add = q_add.strip(',') + ';'

    cursor.execute(q_add, tuple(add_values))
    connection.commit()
    connection.close()

    # ### 6. Updating user proposals: ###
    cursor, connection = connect_to_db(env_file=env_file)
    q_del = "DELETE FROM user_proposals;"
    cursor.execute(q_del)

    q_add = "INSERT INTO user_proposals (chat_id, rec_chat_id, status) VALUES"
    add_values = []
    for chat_id, recommended_chat_ids in chat_id2recommended_chat_ids.items():
        for rec_chat_id in recommended_chat_ids:
            q_add += " (%s, %s, %s),"
            add_values += [chat_id, rec_chat_id, 0]
    q_add = q_add.strip(',') + ';'

    cursor.execute(q_add, tuple(add_values))
    connection.commit()
    connection.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True, type=str, choices=('test', 'deploy'))
    args = parser.parse_known_args()[0]

    if args.host == 'test':
        env_file = 'db_credentials_test.env'
        n_memes = 10
        n_matches = 3
    else:  # args.host == 'deploy':
        env_file = 'db_credentials.env'
        n_memes = 100
        n_matches = 30

    retrain_interval_min = 5
    t_retrain = retrain_interval_min * 60

    while True:
        print('>>> Run recommendation training...')
        t_start = time.perf_counter()
        run_recommendation_train(env_file=env_file, n_memes=n_memes, n_matches=n_matches)
        t_finish = time.perf_counter()
        t_train = int(np.round(t_finish - t_start))
        print(f'>>> Finish recommendation training (in {t_train} s)...')
        print()

        if t_train < t_retrain:
            time.sleep(t_retrain - t_train)


if __name__ == '__main__':
    main()
