from telebot import types

from memeder.interface_tg.config import REACTIONS2BUTTONS


def get_meme_reply_inline():

    markup_inline = types.InlineKeyboardMarkup()

    buttons_row1 = {button: types.InlineKeyboardButton(text=text, callback_data=callback_data)
                    for button, (text, callback_data) in REACTIONS2BUTTONS.items()
                    if button.startswith('b1_')}

    buttons_row2 = {button: types.InlineKeyboardButton(text=text, callback_data=callback_data)
                    for button, (text, callback_data) in REACTIONS2BUTTONS.items()
                    if button.startswith('b2_')}

    markup_inline.row(*list(buttons_row1.values()))
    markup_inline.row(*list(buttons_row2.values()))

    return markup_inline
