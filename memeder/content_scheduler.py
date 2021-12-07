from typing import Union
from datetime import datetime
from telebot import types

from memeder.database.db_functions import add_user, user_exist, add_user_meme_reaction, \
    add_meme, add_user_meme_init
from memeder.meme_recsys.engine import recommend_meme


# https://core.telegram.org/bots/api#message +
# https://github.com/eternnoir/pyTelegramBotAPI#types =
# https://core.telegram.org/bots/api#user
# https://core.telegram.org/bots/api#chat


def start(message, bot, force_start: bool = True):

    user = message.from_user
    chat = message.chat
    user_id: int = user.id                    # TODO: we can set filtering behavior for bots
    user_first_name: str = user.first_name
    tg_username: Union[str, None] = user.username
    chat_id: int = chat.id
    # user_is_bot: bool = user.is_bot
    # user_last_name: Union[str, None] = user.last_name
    d_time = datetime.now()
    d_time_str = d_time.strftime("%d/%m/%Y %H:%M:%S")

    # TODO: use logger
    if not user_exist(tg_username):
        add_user(user_first_name, user_id, tg_username, chat_id, d_time_str, '')

    meme_id, file_id = _call_meme_generator(chat_id)
    _send_meme(chat_id, meme_id=meme_id, file_id=file_id, bot=bot)


def process(call, bot):

    chat_id = call.message.chat.id
    reaction = call.data  # TODO: ***Be aware that a bad client can send arbitrary data in this field.***

    # 1. Updating meme reactions database:
    message_id = call.message.message_id
    add_user_meme_reaction(chat_id, message_id=message_id, reaction=reaction)

    # 2. Check is the person ready to date:
    # if is_ready_to_date(chat_id, database_src=database_src):
    #     recommended_users = recommend_date(chat_id, database_src=database_src)
    #     _send_date(chat_id, recommended_users, bot=bot)
    #
    meme_id, file_id = _call_meme_generator(chat_id)
    _send_meme(chat_id, meme_id=meme_id, file_id=file_id, bot=bot)


def receive_meme(message):
    if message.chat.id in (354637850, 2106431824, ):  # Boris, ffmemesbot (API proxy), ...
        add_meme(file_id=message.photo[-1].file_id, chat_id=message.chat.id, file_type='photo')


def _get_meme_reply_inline():

    markup_inline = types.InlineKeyboardMarkup()

    lol = types.InlineKeyboardButton(text='\U0001F923', callback_data='0')
    smile = types.InlineKeyboardButton(text='\U0001F600', callback_data='1')
    smirking = types.InlineKeyboardButton(text='\U0001F60F	', callback_data='2')
    smiling = types.InlineKeyboardButton(text='\U0000263A', callback_data='3')
    up_down = types.InlineKeyboardButton(text='\U0001F643', callback_data='4')
    thinking = types.InlineKeyboardButton(text='\U0001F914', callback_data='5')
    neutral = types.InlineKeyboardButton(text='\U0001F610', callback_data='6')
    yawn = types.InlineKeyboardButton(text='\U0001F971', callback_data='7')

    crappy = types.InlineKeyboardButton(text=3 * '\U0001F4A9', callback_data='10')
    orgasm_str = '\U0001F4A5' + '\U0001F4AF' + '\U0001F4A3' + '\U0001F4AF' + '\U0001F4A5'
    meme_orgasm = types.InlineKeyboardButton(text=orgasm_str, callback_data='100')

    markup_inline.row(lol, smile, smirking, smiling, up_down, thinking, neutral, yawn)
    markup_inline.row(meme_orgasm, crappy)
    return markup_inline


def _call_meme_generator(chat_id):
    meme_id, file_id = recommend_meme(chat_id)
    return meme_id, file_id


def _send_meme(chat_id, meme_id, file_id, bot):

    bot.send_photo(chat_id, photo=file_id)
    message = bot.send_message(chat_id, 'How do you like it?', reply_markup=_get_meme_reply_inline())
    add_user_meme_init(chat_id=chat_id, meme_id=meme_id, message_id=message.message_id)


def _send_date(chat_id, recommended_users, bot):
    recommended_users_str = ', '.join(['_id' + str(u) for u in recommended_users])
    bot.send_message(chat_id,
                     f'We recommend you to date with users that have following chat IDs: '
                     f'{recommended_users_str}. Now go find them. '
                     f'(This feature is not implemented yet. '
                     f'Please, continue to watch the same memes again and again. '
                     f'We definitely update them... maybe.)')
