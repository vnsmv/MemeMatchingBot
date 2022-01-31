from telebot import types


def get_reply_markup(stage=0):
    """
    0 - Main menu (start)

    1 - `Choose gender`
    2 - `Set preferences`
    3 - `Set goals`
    4 - `Configure profile`

    5 - Main menu (returning)
    """

    if (stage == 0) or (stage == 5):
        if stage == 0:
            message_body = 'Configure your profile to find your best match! \n' \
                           '· Sex \U0001F466  \U0001F467 \n' \
                           '· Preferences for the dating \U0001F498  \U0001F923\n' \
                           '· Describe yourself! \U0001F58A \n' \
                           '· Share your photo \U0001F320'
        else:  # stage == 6:
            message_body = 'In main menu:'

        reply_markup = types.InlineKeyboardMarkup()

        item_0_0 = types.InlineKeyboardButton(text='Choose gender')
        item_0_1 = types.InlineKeyboardButton(text='Set preferences')
        item_1_0 = types.InlineKeyboardButton(text='Set goals')
        item_1_1 = types.InlineKeyboardButton(text='Profile')
        item_2 = types.InlineKeyboardButton(text='<< BACK TO MEMES')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_0, item_1_1)
        reply_markup.row(item_2)

        return message_body, reply_markup

    elif stage == 1:
        message_body = 'Choosing gender:'

        reply_markup = types.InlineKeyboardMarkup()

        item_0_0 = types.InlineKeyboardButton(text='Male')
        item_0_1 = types.InlineKeyboardButton(text='Female')
        item_1 = types.InlineKeyboardButton(text='<< main menu')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1)

        return message_body, reply_markup

    elif stage == 2:
        message_body = 'In preferences settings:'

        reply_markup = types.InlineKeyboardMarkup()
        # 'Show me males', 'Show me females', 'Show me all', 'Show me only memes', '<< main menu',

        item_0_0 = types.InlineKeyboardButton(text='Show me males')
        item_0_1 = types.InlineKeyboardButton(text='Show me females')
        item_1_0 = types.InlineKeyboardButton(text='Show me all')
        item_1_1 = types.InlineKeyboardButton(text='Show me only memes')
        item_2 = types.InlineKeyboardButton(text='<< main menu')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_0, item_1_1)
        reply_markup.row(item_2)

        return message_body, reply_markup

    elif stage == 3:
        message_body = 'In goals settings:'

        reply_markup = types.InlineKeyboardMarkup()
        # 'Friends', 'Relationships', 'Unspecified', 'Only memes', '<< main menu',

        item_0_0 = types.InlineKeyboardButton(text='Friends')
        item_0_1 = types.InlineKeyboardButton(text='Relationships')
        item_1_0 = types.InlineKeyboardButton(text='Unspecified')
        item_1_1 = types.InlineKeyboardButton(text='Only memes')
        item_2 = types.InlineKeyboardButton(text='<< main menu')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_0, item_1_1)
        reply_markup.row(item_2)

        return message_body, reply_markup

    elif stage == 4:
        message_body = 'In profile settings:'

        reply_markup = types.InlineKeyboardMarkup()
        # 'Upload bio', 'Upload photo', 'Clear bio', 'Clear photo', '<< main menu',

        item_0_0 = types.InlineKeyboardButton(text='Upload bio')
        item_0_1 = types.InlineKeyboardButton(text='Upload photo')
        item_1_0 = types.InlineKeyboardButton(text='Clear bio')
        item_1_1 = types.InlineKeyboardButton(text='Clear photo')
        item_2 = types.InlineKeyboardButton(text='Choose sex')
        item_3 = types.InlineKeyboardButton(text='<< main menu')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_0, item_1_1)
        reply_markup.row(item_2)
        reply_markup.row(item_3)

        return message_body, reply_markup

    else:
        return 'Sample text', None
