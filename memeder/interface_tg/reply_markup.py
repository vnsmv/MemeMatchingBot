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
            message_body = 'Configure your profile to find your best match!'
                           #  ''\
                           # '· Sex \U0001F466  \U0001F467 \n' \
                           # '· Preferences for the dating \U0001F498  \U0001F923\n' \
                           # '· Describe yourself! \U0001F58A \n' \
                           # '· Share your photo \U0001F320'
        else:  # stage == 6:
            message_body = 'Main menu::'

        reply_markup = types.ReplyKeyboardMarkup()

        item_0_0 = types.KeyboardButton('Sex \U0001F466  \U0001F467')
        item_0_1 = types.KeyboardButton('Matches preferences')
        item_1_0 = types.KeyboardButton('I am searching for \U0001F498 \U0001F923')
        item_1_1 = types.KeyboardButton('Edit Profile \U0001F58A \U0001F320')
        item_2 = types.KeyboardButton('\U0001F519')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_1, item_1_0)
        reply_markup.row(item_2)

        return message_body, reply_markup

    elif stage == 1:
        message_body = 'Choosing gender:'

        reply_markup = types.ReplyKeyboardMarkup()

        item_0_0 = types.KeyboardButton('Boy \U0001F468')
        item_0_1 = types.KeyboardButton('Girl \U0001F469')
        item_1 = types.KeyboardButton('\U0001F519')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1)

        return message_body, reply_markup

    elif stage == 2:
        message_body = 'I want to see:'

        reply_markup = types.ReplyKeyboardMarkup()
        # 'Show me males', 'Show me females', 'Show me all', 'Show me only memes', '<< main menu',

        item_0_0 = types.KeyboardButton('Boys \U0001F466')
        item_0_1 = types.KeyboardButton('Girls \U0001F469')
        item_1_0 = types.KeyboardButton('All \U0001F469 \U0001F9D1')
        item_1_1 = types.KeyboardButton('Only memes \U0001F60E')
        item_2 = types.KeyboardButton('\U0001F519')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_0, item_1_1)
        reply_markup.row(item_2)

        return message_body, reply_markup

    elif stage == 3:
        message_body = 'My preferences:'

        reply_markup = types.ReplyKeyboardMarkup()
        # 'Friends', 'Relationships', 'Unspecified', 'Only memes', '<< main menu',

        item_0_0 = types.KeyboardButton('Friends \U0001F92A')
        item_0_1 = types.KeyboardButton('Relationships \U0001F498')
        item_1_0 = types.KeyboardButton("I don't know \U0001F914")
        item_1_1 = types.KeyboardButton('Just killing my free time \U0001F63C')
        item_2 = types.KeyboardButton('\U0001F519')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_0, item_1_1)
        reply_markup.row(item_2)

        return message_body, reply_markup

    elif stage == 4:
        message_body = 'In profile settings:'

        reply_markup = types.ReplyKeyboardMarkup()
        # 'Upload bio', 'Upload photo', 'Clear bio', 'Clear photo', '<< main menu',

        item_0_0 = types.KeyboardButton('Bio \U0001F53C')
        item_0_1 = types.KeyboardButton('Photo \U0001F53C')
        item_1_0 = types.KeyboardButton('Clear bio \U0001F6AB')
        item_1_1 = types.KeyboardButton('Clear photo \U0001F6AB')
        # item_2 = types.KeyboardButton('Choose sex')
        item_3 = types.KeyboardButton('\U0001F519')

        reply_markup.row(item_0_0, item_0_1)
        reply_markup.row(item_1_0, item_1_1)
        # reply_markup.row(item_2)
        reply_markup.row(item_3)

        return message_body, reply_markup

    else:
        return 'Sample text', None