import pandas as pd

from memeder.paths import get_lib_root_path


def _read_create_users_db():
    users_db_path = get_lib_root_path() / 'users.csv'
    if users_db_path.exists():
        users_db = pd.read_csv(users_db_path, index_col='UserName')
    else:
        users_db = pd.DataFrame(columns=['UserName', 'UserID'])
        users_db.set_index('UserName', inplace=True)
        users_db.to_csv(users_db_path, index_label='UserName')

    return users_db


def _get_user_id(username, users_db):
    return users_db.loc[username]


def _add_user(username, users_db) -> int:
    user_id = len(users_db)
    users_db = users_db.append(pd.Series({'UserID': user_id}, name=username))
    users_db.to_csv(get_lib_root_path() / 'users.csv', index_label='UserName')
    return user_id


def get_add_user_id(username: str) -> int:
    users_db = _read_create_users_db()
    try:
        user_id = _get_user_id(username=username, users_db=users_db)
    except KeyError:
        user_id = _add_user(username=username, users_db=users_db)
    return user_id
