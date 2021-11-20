from telebot import types

from memeder.paths import get_lib_root_path
from memeder.users_db import get_add_user_id


def start(message, bot, meme_generator):
    username = message.chat.username
    user_id = get_add_user_id(username=username)

    # TODO: use logger
    print(username, user_id, flush=True)
    # bot.send_message(message.chat.id, 'Как тебя зовут?')

    # TODO: visual module
    markup_inline_ = types.InlineKeyboardMarkup()

    # TODO: call
    meme = next(meme_generator)

    with open(get_lib_root_path() / f'Memes/{meme}', 'rb') as meme_img:
        bot.send_photo(message.chat.id, photo=meme_img)
        stress = types.InlineKeyboardButton(text='\U0001F624', callback_data='\U0001F624')
        rocket = types.InlineKeyboardButton(text='\U0001F680', callback_data='\U0001F680')
        neutral = types.InlineKeyboardButton(text='\U0001F610', callback_data='\U0001F610')
        chill = types.InlineKeyboardButton(text='\U0001F60C', callback_data='\U0001F60C')
        cry = types.InlineKeyboardButton(text='\U0001F622', callback_data='\U0001F622')
        markup_inline_.row(stress, rocket, neutral, chill, cry)
        bot.send_message(message.chat.id, 'Hello', reply_markup=markup_inline_)
