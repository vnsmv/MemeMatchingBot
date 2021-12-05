from typing import Union
import time

from telebot import types

from memeder.database_csv.meme_reactions_db import add_meme_reaction_id
from memeder.database_csv.sent_memes_db import add_sent_meme_id, get_sent_meme_value
from memeder.dating_recsys.engine import is_ready_to_date, recommend_date
from memeder.meme_recsys.engine import recommend_meme
from memeder.paths import get_lib_root_path
from memeder.database_csv.users_db import check_add_user_id


def new_start(message, bot, force_start: bool = True,
              connection, cursor):
    # https://core.telegram.org/bots/api#message +
    # https://github.com/eternnoir/pyTelegramBotAPI#types =
    user = message.from_user  # https://core.telegram.org/bots/api#user
    date = message.date  # int
    chat = message.chat  # https://core.telegram.org/bots/api#chat

    user_id: int = user.id
    user_is_bot: bool = user.is_bot  # TODO: we can set filtering behavior for bots
    user_first_name: str = user.first_name
    user_last_name: Union[str, None] = user.last_name
    user_username: Union[str, None] = user.username

    chat_id: int = chat.id

    is_new_user = check_add_user_id(chat_id=chat_id, user_id=user_id, user_is_bot=user_is_bot,
                                    user_first_name=user_first_name, date=date,
                                    user_last_name=user_last_name, user_username=user_username,
                                    database_src=database_src)


def start(message, bot, force_start: bool = True,
          database_src: str = 'database_csv'):
    # https://core.telegram.org/bots/api#message +
    # https://github.com/eternnoir/pyTelegramBotAPI#types =
    user = message.from_user                            # https://core.telegram.org/bots/api#user
    date = message.date                                 # int
    chat = message.chat                                 # https://core.telegram.org/bots/api#chat

    user_id: int = user.id
    user_is_bot: bool = user.is_bot                      # TODO: we can set filtering behavior for bots
    user_first_name: str = user.first_name
    user_last_name: Union[str, None] = user.last_name
    user_username: Union[str, None] = user.username

    chat_id: int = chat.id

    is_new_user = check_add_user_id(chat_id=chat_id, user_id=user_id, user_is_bot=user_is_bot,
                                    user_first_name=user_first_name, date=date,
                                    user_last_name=user_last_name, user_username=user_username,
                                    database_src=database_src)

    # TODO: use logger
    # print(username, user_id, flush=True)
    # bot.send_message(message.chat.id, 'Как тебя зовут?')

    if is_new_user or force_start:
        meme_id = _call_meme_generator(chat_id, database_src=database_src)
        _send_meme(chat_id, meme_id=meme_id, bot=bot, database_src=database_src)


def process(call, bot,
            database_src: str = 'database_csv'):
    chat_id = call.message.chat.id

    reaction = call.data  # TODO: ***Be aware that a bad client can send arbitrary data in this field.***

    # 1. Updating meme reactions database:
    date = int(time.time())  # TODO: i had not found date of callback query:(
    message_id = call.message.message_id
    meme_id = get_sent_meme_value(chat_id, message_id, column='MemeID', database_src=database_src)
    add_meme_reaction_id(chat_id, meme_id, reaction=reaction, date=date, database_src=database_src)

    # 2. Check is the person ready to date:
    if is_ready_to_date(chat_id, database_src=database_src):
        recommended_users = recommend_date(chat_id, database_src=database_src)
        _send_date(chat_id, recommended_users, bot=bot)

    meme_id = _call_meme_generator(chat_id, database_src=database_src)
    _send_meme(chat_id, meme_id=meme_id, bot=bot, database_src=database_src)


def _get_meme_reply_inline():

    markup_inline = types.InlineKeyboardMarkup()

    lol = types.InlineKeyboardButton(text='\U0001F923', callback_data='lol')
    smile = types.InlineKeyboardButton(text='\U0001F642', callback_data='smile')
    neutral = types.InlineKeyboardButton(text='\U0001F610', callback_data='neutral')
    shook = types.InlineKeyboardButton(text='\U0001F631', callback_data='neutral')
    crap = types.InlineKeyboardButton(text='\U0001F4A9', callback_data='neutral')
    clown = types.InlineKeyboardButton(text='\U0001F921	', callback_data='neutral')
    cry = types.InlineKeyboardButton(text='\U0001F625	', callback_data='neutral')
    mind_blast = types.InlineKeyboardButton(text='\U0001F92F', callback_data='neutral')
    cum = types.InlineKeyboardButton(text='\U0001F4A5' +'\U0001F4AB' + '\U0001F4A6', callback_data='neutral')

    flash = types.InlineKeyboardButton(text='\U0001F633	', callback_data='neutral')
    confused = types.InlineKeyboardButton(text='\U0001F615	', callback_data='neutral')
    smirking = types.InlineKeyboardButton(text='\U0001F60F	', callback_data='neutral')
    clown = types.InlineKeyboardButton(text='\U0001F921	', callback_data='neutral')

    markup_inline.row(lol, smile, neutral, shook, crap, cry, clown, mind_blast, cum, flash,confused,smirking)

    return markup_inline


def _call_meme_generator(chat_id, database_src: str = 'database_csv'):
    meme_id = recommend_meme(chat_id=chat_id, database_src=database_src)
    return meme_id


def _send_meme(chat_id, meme_id, bot, database_src: str = 'database_csv'):
    with open(get_lib_root_path() / f'Memes/{meme_id}', 'rb') as meme_img:
        bot.send_photo(chat_id, photo=meme_img)
        message = bot.send_message(chat_id, 'How do you like it?', reply_markup=_get_meme_reply_inline())

        message_id = message.message_id
        date = message.date
        add_sent_meme_id(chat_id, message_id, meme_id=meme_id, date=date, database_src=database_src)


def _send_date(chat_id, recommended_users, bot):
    recommended_users_str = ', '.join(['_id' + str(u) for u in recommended_users])
    bot.send_message(chat_id,
                     f'We recommend you to date with users that have following chat IDs: '
                     f'{recommended_users_str}. Now go find them. '
                     f'(This feature is not implemented yet. '
                     f'Please, continue to watch the same memes again and again. '
                     f'We definitely update them... maybe.)')
