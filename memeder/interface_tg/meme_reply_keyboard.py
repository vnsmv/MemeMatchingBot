from telebot import types

from memeder.interface_tg.config import MEME_REACTION2BUTTON, USER_REACTION2BUTTON


def get_meme_reply_inline():

    markup_inline = types.InlineKeyboardMarkup()

    # buttons_row1 = {button: types.InlineKeyboardButton(text=text, callback_data=callback_data)
    #                 for button, (text, callback_data) in MEME_REACTION2BUTTON.items()
    #                 if button.startswith('b1_')}
    #
    # buttons_row2 = {button: types.InlineKeyboardButton(text=text, callback_data=callback_data)
    #                 for button, (text, callback_data) in MEME_REACTION2BUTTON.items()
    #                 if button.startswith('b2_')}

    buttons_row1 = {button: types.InlineKeyboardButton(text=MEME_REACTION2BUTTON[button][0],
                                                       callback_data=MEME_REACTION2BUTTON[button][1])
                    for button in ('b2_like', 'b1_upside', 'b2_dislike')}
    buttons_row2 = {button: types.InlineKeyboardButton(text=MEME_REACTION2BUTTON[button][0],
                                                       callback_data=MEME_REACTION2BUTTON[button][1])
                    for button in ('bu_users', )}

    markup_inline.row(*list(buttons_row1.values()))
    markup_inline.row(*list(buttons_row2.values()))

    return markup_inline


def get_user_reply_inline(telegram_username):

    markup_inline = types.InlineKeyboardMarkup()

    markup_inline.row(
        types.InlineKeyboardButton(text=USER_REACTION2BUTTON['b1_like'][0],
                                   callback_data=USER_REACTION2BUTTON['b1_like'][1]),
        types.InlineKeyboardButton(text=USER_REACTION2BUTTON['b1_chat'][0],
                                   # callback_data=USER_REACTION2BUTTON['b1_chat'][1],
                                   url=f'https://t.me/{telegram_username}?start=+666'),
        types.InlineKeyboardButton(text=USER_REACTION2BUTTON['b1_dislike'][0],
                                   callback_data=USER_REACTION2BUTTON['b1_dislike'][1]),
    )

    markup_inline.row(
        types.InlineKeyboardButton(text=USER_REACTION2BUTTON['bm_memes'][0],
                                   callback_data=USER_REACTION2BUTTON['bm_memes'][1]),
    )

    return markup_inline


def get_user2meme_reply_inline():

    markup_inline = types.InlineKeyboardMarkup()

    markup_inline.row(
        types.InlineKeyboardButton(text=USER_REACTION2BUTTON['bm_memes'][0],
                                   callback_data=USER_REACTION2BUTTON['bm_memes'][1]),
    )

    return markup_inline
