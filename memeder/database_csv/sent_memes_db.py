import pandas as pd

from memeder.paths import get_database_path


SENT_MEMES_DB_NAME = 'sent_memes.csv'
SENT_MEMES_DB_INDEX = ('ChatID', 'MessageID', )
SENT_MEMES_DB_COLUMNS = (
    *SENT_MEMES_DB_INDEX,
    'MemeID', 'Date'
)


def _create_sent_memes_db():
    sent_memes_db = pd.DataFrame(columns=list(SENT_MEMES_DB_COLUMNS))
    sent_memes_db.set_index(list(SENT_MEMES_DB_INDEX), inplace=True)
    return sent_memes_db


def _read_sent_memes_db(database_src: str = 'database_csv'):
    sent_memes_db_path = get_database_path(database_src=database_src) / SENT_MEMES_DB_NAME
    sent_memes_db = pd.read_csv(sent_memes_db_path, index_col=SENT_MEMES_DB_INDEX)
    return sent_memes_db


def _update_sent_memes_db(sent_memes_db, database_src: str = 'database_csv'):
    sent_memes_db_path = get_database_path(database_src=database_src) / SENT_MEMES_DB_NAME
    sent_memes_db.to_csv(sent_memes_db_path, index_label=SENT_MEMES_DB_INDEX)


def _read_create_sent_memes_db(database_src: str = 'database_csv'):
    sent_memes_db_path = get_database_path(database_src=database_src) / SENT_MEMES_DB_NAME

    if sent_memes_db_path.exists():
        sent_memes_db = _read_sent_memes_db(database_src=database_src)
    else:
        sent_memes_db = _create_sent_memes_db()
        _update_sent_memes_db(sent_memes_db, database_src=database_src)

    return sent_memes_db


def _check_sent_memes(sent_memes_db, chat_id, message_id):
    return (chat_id, message_id) in sent_memes_db.index


def _add_sent_meme(sent_memes_db,
                   chat_id: int, message_id: int, meme_id: str, date: int,
                   database_src: str = 'database_csv'):

    sent_meme_entry = pd.Series({column: value for column, value in zip(SENT_MEMES_DB_COLUMNS[2:], (meme_id, date))},
                                name=(chat_id, message_id))

    sent_memes_db = sent_memes_db.append(sent_meme_entry)

    _update_sent_memes_db(sent_memes_db=sent_memes_db, database_src=database_src)


def add_sent_meme_id(chat_id: int, message_id: int, meme_id: str, date: int,
                     database_src: str = 'database_csv'):
    sent_memes_db = _read_create_sent_memes_db(database_src=database_src)
    is_new_sent_meme = not _check_sent_memes(sent_memes_db=sent_memes_db, chat_id=chat_id, message_id=message_id)
    if is_new_sent_meme:
        _add_sent_meme(sent_memes_db=sent_memes_db,
                       chat_id=chat_id, message_id=message_id, meme_id=meme_id, date=date,
                       database_src=database_src)
    else:
        # TODO: it is most likely a mistake? or is it? check it out!
        pass


def get_sent_meme_value(chat_id: int, message_id: int, column: str, database_src: str = 'database_csv'):
    sent_memes_db = _read_create_sent_memes_db(database_src=database_src)
    if not _check_sent_memes(sent_memes_db=sent_memes_db, chat_id=chat_id, message_id=message_id):
        # TODO: logging
        raise KeyError(f'Found no user with id `{chat_id}`.')

    value = sent_memes_db.loc[(chat_id, message_id)][column]
    if isinstance(value, pd.core.series.Series):
        value = value.iloc[0]

    return value
