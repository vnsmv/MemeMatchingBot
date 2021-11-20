from telebot import types

from memeder.meme_recsys.engine import recommend_meme
from memeder.paths import get_lib_root_path
from memeder.users_db import get_add_user_id


def start(message, bot, meme_generator, force=False):
    username = message.chat.username
    user_id, is_new_user = get_add_user_id(username=username)
    # TODO: if new - send meme
    #       else skip (?) -- that means that our bot waits for reply

    # TODO: use logger
    # print(username, user_id, flush=True)
    # bot.send_message(message.chat.id, 'Как тебя зовут?')

    if is_new_user or force:
        call_meme_generator(meme_generator, user_id, bot=bot, chat_id=message.chat.id)


def process(call, bot, meme_generator):
    message = call.message
    username = message.chat.username
    user_id = get_add_user_id(username=username)

    condition_to_call_meme_generator = True  # TODO: otherwise call person proposal

    if condition_to_call_meme_generator:
        call_meme_generator(meme_generator, user_id, bot=bot, chat_id=message.chat.id)
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


def call_meme_generator(meme_generator, user_id, bot, chat_id):
    meme = recommend_meme(meme_generator=meme_generator, user_id=user_id)
    with open(get_lib_root_path() / f'Memes/{meme}', 'rb') as meme_img:
        bot.send_photo(chat_id, photo=meme_img)
        bot.send_message(chat_id, 'Reaction on meme:', reply_markup=get_meme_reply_inline())
