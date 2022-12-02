import os

from memeder.database.connect import connect_to_db
from memeder.database.db_functions import get_profile_value
from memeder.interface_tg.config import MENU_BUTTONS
from memeder.interface_tg.meme_reply_keyboard import get_user_reply_inline


def _get_telegram_username_and_name(chat_id: int):
    cursor, connection = connect_to_db()
    q = "SELECT telegram_username, name FROM users WHERE chat_id = %s;"
    cursor.execute(q, (chat_id, ))
    telegram_username, name = cursor.fetchone()
    connection.commit()
    connection.close()
    return telegram_username, name


def _get_goals(chat_id: int):
    goals_code = get_profile_value(chat_id, column='goals')
    goals_code2text = {MENU_BUTTONS[k][3]: MENU_BUTTONS[k][0] for k in MENU_BUTTONS.keys() if k.startswith('m4')}
    return goals_code2text[goals_code]


def get_user_profile(chat_id, similarity):
    boy_photo_id = 'AgACAgIAAxkBAAEC0tljid2Kp7zLB0lBlfq8sXKU1TLvFQACCrkxG2vI6Uvs8mhQ97znsQEAAwIAA3MAAysE'
    girl_photo_id = 'AgACAgIAAxkBAAEC0tpjid3AZo8YRfSJICc0AeqlTJRr2AACDbkxG2vI6UsN11Set9I2yAEAAwIAA3MAAysE'

    if get_profile_value(chat_id, column='use_photo'):
        photo_id = get_profile_value(chat_id, column='photo_id')
    else:
        if get_profile_value(chat_id, column='sex') == MENU_BUTTONS['m1_girl'][-1]:
            photo_id = girl_photo_id
        else:  # get_profile_value(chat_id_rec, column='sex') == MENU_BUTTONS['m1_boy'][-1]:
            photo_id = boy_photo_id

    telegram_username, name = _get_telegram_username_and_name(chat_id=chat_id)

    user_reply_markup = get_user_reply_inline(telegram_username=telegram_username)

    profile_description = f'{name}\n\n'

    profile_description += f'\U0001F3AF {_get_goals(chat_id=chat_id)}\n\n'

    profile_description += f'\U0001F4AB	Совместимость по чувству юмора {similarity}%\n\n'

    bio = ''
    if get_profile_value(chat_id, column='use_bio'):
        bio = get_profile_value(chat_id, column='bio')
    if not bio:
        bio = 'Пользователь еще не добавил био...'

    profile_description += f'\U0001F58B {bio}'

    return photo_id, profile_description, user_reply_markup
