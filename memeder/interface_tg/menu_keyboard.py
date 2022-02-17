import logging

from telebot import types

from memeder.interface_tg.config import MENU_BUTTONS


def get_reply_markup(button: str = 'm_start') -> (str, types.ReplyKeyboardMarkup):
    reply_markup = types.ReplyKeyboardMarkup()

    if (button == 'm_start') or (button == 'm_main_menu'):
        item_0_0 = types.KeyboardButton(MENU_BUTTONS['m0_gender'][0])
        item_0_1 = types.KeyboardButton(MENU_BUTTONS['m0_preferences'][0])
        item_1_0 = types.KeyboardButton(MENU_BUTTONS['m0_profile'][0])
        item_1_1 = types.KeyboardButton(MENU_BUTTONS['m0_goals'][0])
        item_2 = types.KeyboardButton(MENU_BUTTONS['m0_memes'][0])

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_1, item_1_0)
        reply_markup.row(item_2)

    elif button == 'm0_gender':
        item_0_0 = types.KeyboardButton(MENU_BUTTONS['m1_boy'][0])
        item_0_1 = types.KeyboardButton(MENU_BUTTONS['m1_girl'][0])
        item_1 = types.KeyboardButton(MENU_BUTTONS['m_main_menu'][0])

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1)

    elif button == 'm0_preferences':
        item_0_0 = types.KeyboardButton(MENU_BUTTONS['m2_boys'][0])
        item_0_1 = types.KeyboardButton(MENU_BUTTONS['m2_girls'][0])
        item_1_0 = types.KeyboardButton(MENU_BUTTONS['m2_all'][0])
        item_1_1 = types.KeyboardButton(MENU_BUTTONS['m2_memes'][0])
        item_2 = types.KeyboardButton(MENU_BUTTONS['m_main_menu'][0])

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_0, item_1_1)
        reply_markup.row(item_2)

    elif button == 'm0_profile':
        item_0_0 = types.KeyboardButton(MENU_BUTTONS['m3_bio'][0])
        item_0_1 = types.KeyboardButton(MENU_BUTTONS['m3_photo'][0])
        item_1_0 = types.KeyboardButton(MENU_BUTTONS['m3_del_bio'][0])
        item_1_1 = types.KeyboardButton(MENU_BUTTONS['m3_del_photo'][0])
        item_2_0 = types.KeyboardButton(MENU_BUTTONS['p3_profile'][0])
        item_2_1 = types.KeyboardButton(MENU_BUTTONS['m_main_menu'][0])

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_0, item_1_1)
        reply_markup.row(item_2_0, item_2_1)

    elif button == 'm0_goals':
        item_0_0 = types.KeyboardButton(MENU_BUTTONS['m4_friends'][0])
        item_0_1 = types.KeyboardButton(MENU_BUTTONS['m4_relationships'][0])
        item_1_0 = types.KeyboardButton(MENU_BUTTONS['m4_idk'][0])
        item_1_1 = types.KeyboardButton(MENU_BUTTONS['m4_memes'][0])
        item_2 = types.KeyboardButton(MENU_BUTTONS['m_main_menu'][0])

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_0, item_1_1)
        reply_markup.row(item_2)

    else:  # Case of some error --> returning to the main menu
        logging.exception("Case of some error in menu routing --> returning to the main menu;")

        item_0_0 = types.KeyboardButton(MENU_BUTTONS['m0_gender'][0])
        item_0_1 = types.KeyboardButton(MENU_BUTTONS['m0_preferences'][0])
        item_1_0 = types.KeyboardButton(MENU_BUTTONS['m0_profile'][0])
        item_1_1 = types.KeyboardButton(MENU_BUTTONS['m0_goals'][0])
        item_2 = types.KeyboardButton(MENU_BUTTONS['m0_memes'][0])

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_1, item_1_0)
        reply_markup.row(item_2)

        return MENU_BUTTONS['m_main_menu'][1], reply_markup

    return MENU_BUTTONS[button][1], reply_markup
