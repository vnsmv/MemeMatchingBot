from typing import Union

from telebot import types

from memeder.meme_recsys.engine import recommend_meme
from memeder.paths import get_lib_root_path
from memeder.users_db import check_add_user_id, get_user_value


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

    is_new_user = check_add_user_id(user_id=user_id, user_is_bot=user_is_bot, user_first_name=user_first_name,
                                    chat_id=chat_id, date=date,
                                    user_last_name=user_last_name, user_username=user_username,
                                    database_src=database_src)

    # TODO: use logger
    # print(username, user_id, flush=True)
    # bot.send_message(message.chat.id, 'Как тебя зовут?')

    if is_new_user or force_start:
        call_meme_generator(user_id, bot=bot, chat_id=chat_id)


def process(call, bot,
            database_src: str = 'database_csv'):
    user_id = call.message.from_user.id
    chat_id = call.message.chat.id

    # 1. Updating meme reactions database:



    condition_to_call_meme_generator = True  # TODO: otherwise call person proposal

    if condition_to_call_meme_generator:
        call_meme_generator(user_id, bot, chat_id=chat_id, database_src=database_src)
    else:
        # TODO: person proposal
        pass


def get_meme_reply_inline():
    markup_inline = types.InlineKeyboardMarkup()

    stress = types.InlineKeyboardButton(text='\U0001F624', callback_data='emoji-stress')
    rocket = types.InlineKeyboardButton(text='\U0001F680', callback_data='emoji-rocket')
    neutral = types.InlineKeyboardButton(text='\U0001F610', callback_data='emoji-neutral')
    chill = types.InlineKeyboardButton(text='\U0001F60C', callback_data='emoji-chill')
    cry = types.InlineKeyboardButton(text='\U0001F622', callback_data='emoji-cry')

    markup_inline.row(stress, rocket, neutral, chill, cry)

    return markup_inline


def call_meme_generator(user_id, bot, chat_id: int = None,
                        database_src: str = 'database_csv'):
    if chat_id is None:
        chat_id = get_user_value(user_id, 'ChatID', database_src=database_src)

    meme_id = recommend_meme(user_id=user_id, database_src=database_src)
    _send_meme(meme_id=meme_id, chat_id=chat_id, bot=bot)


def _send_meme(meme_id, chat_id, bot):
    with open(get_lib_root_path() / f'Memes/{meme_id}', 'rb') as meme_img:
        bot.send_photo(chat_id, photo=meme_img)
        bot.send_message(chat_id, 'Reaction on meme:', reply_markup=get_meme_reply_inline())
