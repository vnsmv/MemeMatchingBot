from telebot import types


def get_reply_markup(stage=0):
    """
    0 - Main menu (start)

    1 - `Choose sex`
    2 - `Set preferences`
    3 - `Set goals`
    4 - `Configure profile`

    5 - Main menu (returning)
    """

    if (stage == 0) or (stage == 5):
        if stage == 0:
            message_body = '...'
        else:  # stage == 6:
            message_body = 'In main menu:'

        reply_markup = types.ReplyKeyboardMarkup()

        item_0_0 = types.KeyboardButton('Choose sex')
        item_0_1 = types.KeyboardButton('Set preferences')
        item_1_0 = types.KeyboardButton('Set goals')
        item_1_1 = types.KeyboardButton('Profile')
        item_2 = types.KeyboardButton('<< BACK TO MEMES')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_0, item_1_1)
        reply_markup.row(item_2)

        return message_body, reply_markup

    elif stage == 1:
        message_body = 'Choosing sex:'

        reply_markup = types.ReplyKeyboardMarkup()

        item_0_0 = types.KeyboardButton('Male')
        item_0_1 = types.KeyboardButton('Female')
        item_1 = types.KeyboardButton('<< main menu')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1)

        return message_body, reply_markup

    elif stage == 2:
        message_body = 'In preferences settings:'

        reply_markup = types.ReplyKeyboardMarkup()
        # 'Show me males', 'Show me females', 'Show me all', 'Show me only memes', '<< main menu',

        item_0_0 = types.KeyboardButton('Show me males')
        item_0_1 = types.KeyboardButton('Show me females')
        item_1_0 = types.KeyboardButton('Show me all')
        item_1_1 = types.KeyboardButton('Show me only memes')
        item_2 = types.KeyboardButton('<< main menu')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_0, item_1_1)
        reply_markup.row(item_2)

        return message_body, reply_markup

    elif stage == 3:
        message_body = 'In goals settings:'

        reply_markup = types.ReplyKeyboardMarkup()
        # 'Friends', 'Relationships', 'Unspecified', 'Only memes', '<< main menu',

        item_0_0 = types.KeyboardButton('Friends')
        item_0_1 = types.KeyboardButton('Relationships')
        item_1_0 = types.KeyboardButton('Unspecified')
        item_1_1 = types.KeyboardButton('Only memes')
        item_2 = types.KeyboardButton('<< main menu')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_0, item_1_1)
        reply_markup.row(item_2)

        return message_body, reply_markup

    elif stage == 4:
        message_body = 'In profile settings:'

        reply_markup = types.ReplyKeyboardMarkup()
        # 'Upload bio', 'Upload photo', 'Clear bio', 'Clear photo', '<< main menu',

        item_0_0 = types.KeyboardButton('Upload bio')
        item_0_1 = types.KeyboardButton('Upload photo')
        item_1_0 = types.KeyboardButton('Clear bio')
        item_1_1 = types.KeyboardButton('Clear photo')
        item_2 = types.KeyboardButton('Choose sex')
        item_3 = types.KeyboardButton('<< main menu')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_0, item_1_1)
        reply_markup.row(item_2)
        reply_markup.row(item_3)

        return message_body, reply_markup

    else:
        return 'Sample text', None
