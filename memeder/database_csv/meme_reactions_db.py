import pandas as pd

from memeder.paths import get_database_path


MEME_REACTIONS_DB_NAME = 'meme_reactions.csv'
MEME_REACTIONS_DB_INDEX = ('ChatID', 'MemeID', )
MEME_REACTIONS_DB_COLUMNS = (
    *MEME_REACTIONS_DB_INDEX,
    'Reaction', 'Date'
)


def _create_meme_reactions_db():
    meme_reactions_db = pd.DataFrame(columns=list(MEME_REACTIONS_DB_COLUMNS))
    meme_reactions_db.set_index(list(MEME_REACTIONS_DB_INDEX), inplace=True)
    return meme_reactions_db


def _read_meme_reactions_db(database_src: str = 'database_csv'):
    meme_reactions_db_path = get_database_path(database_src=database_src) / MEME_REACTIONS_DB_NAME
    meme_reactions_db = pd.read_csv(meme_reactions_db_path, index_col=MEME_REACTIONS_DB_INDEX)
    return meme_reactions_db


def _update_meme_reactions_db(meme_reactions_db, database_src: str = 'database_csv'):
    meme_reactions_db_path = get_database_path(database_src=database_src) / MEME_REACTIONS_DB_NAME
    meme_reactions_db.to_csv(meme_reactions_db_path, index_label=MEME_REACTIONS_DB_INDEX)


def _read_create_meme_reactions_db(database_src: str = 'database_csv'):
    meme_reactions_db_path = get_database_path(database_src=database_src) / MEME_REACTIONS_DB_NAME

    if meme_reactions_db_path.exists():
        meme_reactions_db = _read_meme_reactions_db(database_src=database_src)
    else:
        meme_reactions_db = _create_meme_reactions_db()
        _update_meme_reactions_db(meme_reactions_db, database_src=database_src)

    return meme_reactions_db


def _check_meme_reactions(meme_reactions_db, chat_id, meme_id):
    return (chat_id, meme_id) in meme_reactions_db.index


def _add_meme_reaction(meme_reactions_db,
                       chat_id: int, meme_id: str, reaction: str, date: int,
                       database_src: str = 'database_csv'):

    meme_reaction_entry = pd.Series({column: value for column, value in zip(MEME_REACTIONS_DB_COLUMNS[2:],
                                                                            (reaction, date))},
                                    name=(chat_id, meme_id))

    meme_reactions_db = meme_reactions_db.append(meme_reaction_entry)

    _update_meme_reactions_db(meme_reactions_db=meme_reactions_db, database_src=database_src)


def add_meme_reaction_id(chat_id: int, meme_id: str, reaction: str, date: int,
                         database_src: str = 'database_csv'):
    meme_reactions_db = _read_create_meme_reactions_db(database_src=database_src)
    is_new_meme_reaction = not _check_meme_reactions(meme_reactions_db=meme_reactions_db,
                                                     chat_id=chat_id, meme_id=meme_id)
    if is_new_meme_reaction:
        _add_meme_reaction(meme_reactions_db=meme_reactions_db,
                           chat_id=chat_id, meme_id=meme_id, reaction=reaction, date=date,
                           database_src=database_src)
    else:
        # TODO: how can we handle meme reaction repeats?
        # TODO: probably, we should sample unique memes at the level of the meme recommendation engine.
        pass
    # return is_new_meme_reaction


# def get_user_value(user_id, value, database_src: str = 'database_csv'):
#     users_db = _read_create_users_db(database_src=database_src)
#     if not _check_user(users_db=users_db, user_id=user_id):
#         # TODO: logging
#         raise KeyError(f'Found no user with id `{user_id}`.')
#
#     return users_db.loc[user_id][value]
