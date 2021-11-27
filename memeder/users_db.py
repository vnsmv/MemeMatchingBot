from typing import Union

import pandas as pd

from memeder.paths import get_database_path


USERS_DB_NAME = 'users.csv'
USERS_DB_INDEX = 'UserID'
USERS_DB_COLUMNS = (
    USERS_DB_INDEX, 'UserIsBot', 'UserFirstName',
    'ChatID', 'Date',
    'UserLastName', 'UserUsername',
)


def _create_users_db():
    users_db = pd.DataFrame(columns=USERS_DB_COLUMNS)
    users_db.set_index(USERS_DB_INDEX, inplace=True)
    return users_db


def _read_users_db(database_src: str = 'database_csv'):
    users_db_path = get_database_path(database_src=database_src) / USERS_DB_NAME
    users_db = pd.read_csv(users_db_path, index_col=USERS_DB_INDEX)
    return users_db


def _update_users_db(users_db, database_src: str = 'database_csv'):
    users_db_path = get_database_path(database_src=database_src) / USERS_DB_NAME
    users_db.to_csv(users_db_path, index_label=USERS_DB_INDEX)


def _read_create_users_db(database_src: str = 'database_csv'):
    users_db_path = get_database_path(database_src=database_src) / USERS_DB_NAME

    if users_db_path.exists():
        users_db = _read_users_db(database_src=database_src)
    else:
        users_db = _create_users_db()
        _update_users_db(users_db, database_src=database_src)

    return users_db


def _check_user(users_db, user_id):
    return user_id in users_db.index


def _add_user(users_db,
              user_id: int, user_is_bot: bool, user_first_name: str, chat_id: int, date: int,
              user_last_name: Union[str, None] = None, user_username: Union[str, None] = None,
              database_src: str = 'database_csv'):

    user_entry = pd.Series({column: value for column, value in
                            zip(USERS_DB_COLUMNS[1:],
                                (user_is_bot, user_first_name, chat_id, date, user_last_name, user_username))},
                           name=user_id)

    users_db = users_db.append(user_entry)

    _update_users_db(users_db=users_db, database_src=database_src)

    return user_id


def check_add_user_id(user_id: int, user_is_bot: bool, user_first_name: str, chat_id: int, date: int,
                      user_last_name: Union[str, None] = None, user_username: Union[str, None] = None,
                      database_src: str = 'database_csv') -> bool:
    users_db = _read_create_users_db(database_src=database_src)
    is_new_user = not _check_user(users_db=users_db, user_id=user_id)
    if is_new_user:
        _add_user(users_db=users_db,
                  user_id=user_id, user_is_bot=user_is_bot, user_first_name=user_first_name,
                  chat_id=chat_id, date=date,
                  user_last_name=user_last_name, user_username=user_username,
                  database_src=database_src)
    else:
        # TODO: update the user's info
        # TODO: the update rate might be also a useful feature
        pass
    return is_new_user


def get_user_value(user_id, value, database_src: str = 'database_csv'):
    users_db = _read_create_users_db(database_src=database_src)
    if not _check_user(users_db=users_db, user_id=user_id):
        # TODO: logging
        raise KeyError(f'Found no user with id `{user_id}`.')

    return users_db.loc[user_id][value]
