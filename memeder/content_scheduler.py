import datetime
from typing import Union

from memeder.database.db_functions import add_user, user_exist, add_user_meme_reaction, \
    add_meme, add_user_meme_init, add_user_user_init, add_user_user_reaction, update_profile, get_profile_value, \
    get_all_user_ids
from memeder.interface_tg.config import MEME_REACTION2BUTTON, USER_REACTION2BUTTON
from memeder.interface_tg.meme_reply_keyboard import get_meme_reply_inline, get_user_reply_inline, \
    get_user2meme_reply_inline
from memeder.interface_tg.reply_markup import get_reply_markup
from memeder.meme_recsys.engine import recommend_meme, recommend_user
from memeder.meme_recsys.refreshing_activity import top_memes_selection, is_sending_meme, select_meme


# https://core.telegram.org/bots/api#message +
# https://github.com/eternnoir/pyTelegramBotAPI#types =
# https://core.telegram.org/bots/api#user
# https://core.telegram.org/bots/api#chat


def start(message, bot):

    user = message.from_user
    chat = message.chat
    user_id: int = user.id
    user_first_name: str = user.first_name
    tg_username: Union[str, None] = user.username
    chat_id: int = chat.id
    # user_last_name: Union[str, None] = user.last_name

    is_new_user = not user_exist(chat_id)
    if is_new_user:
        add_user(user_first_name, user_id, tg_username, chat_id)

    # _send_menu(chat_id, bot=bot, stage=0 if is_new_user else 5)
    _send_menu(chat_id, bot=bot, stage=0)

    # meme_id, file_id = _call_meme_generator(chat_id)
    # _send_meme(chat_id, meme_id=meme_id, file_id=file_id, bot=bot)


def start_meme(message, bot):
    chat_id: int = message.chat.id
    meme_id, file_id = _call_meme_generator(chat_id)
    _send_meme(chat_id, meme_id=meme_id, file_id=file_id, bot=bot)


def process(call, bot):

    chat_id = call.message.chat.id
    reaction = call.data

    # 0. Checking existence of the user in the database (e.g., the latter was updated):
    if not user_exist(chat_id):
        bot.send_message(chat_id, 'Please, restart the bot (/start), so that we could process your feedback;)')

    else:
        message_id = call.message.message_id

        # 1. Updating meme reactions database:
        if reaction in [v[1] for k, v in MEME_REACTION2BUTTON.items() if k.startswith('b')]:

            if reaction == MEME_REACTION2BUTTON['bu_users'][1]:
                chat_id_rec, telegram_username, message_body = _call_user_generator(chat_id=chat_id)
                if chat_id_rec is None:
                    _send_user2meme(chat_id=chat_id, message_body=message_body, bot=bot)
                else:
                    _send_user(chat_id=chat_id, chat_id_rec=chat_id_rec, telegram_username=telegram_username,
                               message_body=message_body, bot=bot)
            else:
                add_user_meme_reaction(chat_id, message_id=message_id, reaction=reaction)

                # 3. recommend new meme
                meme_id, file_id = _call_meme_generator(chat_id)
                _send_meme(chat_id, meme_id=meme_id, file_id=file_id, bot=bot)

        # 4. Updating users reactions database:
        if reaction in [v[1] for k, v in USER_REACTION2BUTTON.items() if k.startswith('b')]:
            add_user_user_reaction(chat_id, message_id=message_id, reaction=reaction)

            if reaction == USER_REACTION2BUTTON['bm_memes'][1]:
                # 5. recommend new meme
                meme_id, file_id = _call_meme_generator(chat_id)
                _send_meme(chat_id, meme_id=meme_id, file_id=file_id, bot=bot)
            else:
                chat_id_rec, telegram_username, message_body = _call_user_generator(chat_id=chat_id)
                if chat_id_rec is None:
                    _send_user2meme(chat_id=chat_id, message_body=message_body, bot=bot)
                else:
                    _send_user(chat_id=chat_id, chat_id_rec=chat_id_rec, telegram_username=telegram_username,
                               message_body=message_body, bot=bot)

    # TODO: do we need to force dating recommendations?


def receive_photo(message):
    chat_id = message.chat.id
    if get_profile_value(chat_id, column='photo_update_flag'):
        file_id = message.photo[-1].file_id
        file_unique_id = message.photo[-1].file_unique_id
        update_profile(chat_id=chat_id, column='photo_id', value=file_id)
        update_profile(chat_id=chat_id, column='photo_unique_id', value=file_unique_id)
        update_profile(chat_id=chat_id, column='use_photo', value=True)
        update_profile(chat_id=chat_id, column='photo_update_flag', value=False)

    elif chat_id in (354637850, 2106431824, ):  # Boris, ffmemesbot (API proxy), ...
        add_meme(file_id=message.photo[-1].file_id, file_unique_id=message.photo[-1].file_unique_id,
                 chat_id=message.chat.id, file_type='photo')


def menu_routing(message, bot):
    text2stage = {'Sex \U0001F466  \U0001F467': 1, 'Matches preferences': 2, 'I am searching for \U0001F498 \U0001F923': 3, 'Edit Profile \U0001F58A \U0001F320': 4, 'Main menu \U0001F519': 5}
    _send_menu(chat_id=message.chat.id, bot=bot, stage=text2stage[message.text])


def menu_update(message, bot):
    chat_id = message.chat.id
    update = message.text
    update2message = {
        # 'Seen to males':        ('Your privacy is set to `Seen to males`.', 'privacy', 2000),
        # 'Seen to females':      ('Your privacy is set to `Seen to females`.', 'privacy', 2001),
        # 'Seen to all':          ('Your privacy is set to `Seen to all`.', 'privacy', 2002),
        # 'Seen to nobody':       ('Your privacy is set to `Seen to nobody`.', 'privacy', 2003),
        'Boys \U0001F466':        ('Got it! \n Dont hesitate to write first \U0001F609', 'preferences', 3000),
        'Girls \U0001F469':      ('Ok, \n fingers crossed! \U0001F60A', 'preferences', 3001),
        'All \U0001F469 \U0001F9D1':          ('Ok, will show you all users', 'preferences', 3002),
        'Only memes \U0001F60E':   ('Just memes, good choice!', 'preferences', 3003),
        'Friends \U0001F92A':              ('Yeap!', 'goals', 4000),
        'Relationships \U0001F498':        ('Good look to find you love \U0001F49E', 'goals', 4001),
        "I don't know \U0001F914":          ('Killing free time?)', 'goals', 4002),
        'Just killing my free time \U0001F63C':           ('Just memes, got it!', 'goals', 4003),
        'Bio \U0001F53C':           ('Send me your bio:)', 'bio_update_flag', True),
        'Photo \U0001F53C':         ('Send me your photo:)', 'photo_update_flag', True),
        'Clear bio \U0001F6AB':            ('Successfully deleted bio', 'use_bio', False),
        'Clear photo \U0001F6AB':          ('Successfully deleted photo', 'use_photo', False),
        'Boy \U0001F468':                 ('Success!', 'sex', 5000),
        'Girl \U0001F469':               ('Success!', 'sex', 5001),
    }
    update_profile(chat_id=chat_id, column=update2message[update][1], value=update2message[update][2])
    bot.send_message(chat_id, update2message[update][0] )
    _send_menu(chat_id=chat_id, bot=bot, stage=5)


def check_receive_bio(message):
    chat_id = message.chat.id
    if get_profile_value(chat_id, column='bio_update_flag'):
        update_profile(chat_id=chat_id, column='bio', value=message.text)
        update_profile(chat_id=chat_id, column='use_bio', value=True)
        update_profile(chat_id=chat_id, column='bio_update_flag', value=False)


def message_all(message, bot):

    msg = \
        """
Hi there,
Meme Dating team on the line! We received your feedback and present you v 0.2. What's new:\n
- User's photo 🌠  and bio 🖌\n
- Dating preferences (show me just girls/boys/all/memes) 🤦‍♀️🙎‍♂️\n
- Better memes recommendation system !💥\n
> Soon, we will add .gif and .mp4 support so you will be able to enjoy better memes.
"""

    host_id = message.chat.id
    if host_id == 354637850:
        chat_ids = get_all_user_ids()
        for chat_id in chat_ids:
            # if chat_id in (481807223, 354637850, 11436017):
            try:
                bot.send_message(chat_id, msg)
                print('Sent message to ', chat_id, flush=True)
            except Exception:
                print('Failed to send a message to ', chat_id, flush=True)
                pass


def meme_all(message, bot):

    host_id = message.chat.id
    if host_id == 354637850:
        chat_ids = get_all_user_ids()
        top_meme_ids, _, _ = top_memes_selection()

        for chat_id in chat_ids:
            # if chat_id in (481807223, 354637850, 11436017):
            if is_sending_meme(chat_id=chat_id, time_delta=datetime.timedelta(days=2)):
                meme_id, file_id = select_meme(chat_id, top_meme_ids)
                if meme_id is None:
                    meme_id, file_id = _call_meme_generator(chat_id)

                try:
                    _send_meme(chat_id, meme_id=meme_id, file_id=file_id, bot=bot)
                    print(f'Sent a refresh meme {meme_id} to {chat_id}', flush=True)
                except Exception:
                    print(f'Failed to send a refresh meme {meme_id} to {chat_id}', flush=True)
                    pass


def _call_meme_generator(chat_id):
    meme_id, file_id = recommend_meme(chat_id)
    return meme_id, file_id


def _call_user_generator(chat_id):
    chat_id_rec, telegram_username, name, n_reactions_to_do = recommend_user(chat_id=chat_id)

    if n_reactions_to_do > 0:
        message_body = f'To calculate the best match for you, '\
                       f'we need more meme reactions. Enjoy {n_reactions_to_do} more memes:)'
    elif n_reactions_to_do == -1:
        message_body = 'We need some time to update recommendations ' \
                       'Or you review all users  \U0001F642' \

    elif n_reactions_to_do == -2:
        message_body = 'Specify your gender \n' \
                        '\U0001F466 ' + '\U0001F467 \n' \
                       '(type command /start)'
    elif n_reactions_to_do == -3:
        message_body = 'Specify your preferences \n' \
                       '(type command /start)'
    elif n_reactions_to_do == -4:
        message_body = 'Specify your goals \n ' \
                       'It could be done quickly from the main menu (/start).'
    else:  # n_reactions_to_do == 0:
        message_body = f' {name} '
    return chat_id_rec, telegram_username, message_body


def _send_meme(chat_id, meme_id, file_id, bot): #update_profile
    # bot.send_message(chat_id, 'New meme for you:)')
    message = bot.send_photo(chat_id, photo=file_id, reply_markup=get_meme_reply_inline())
    add_user_meme_init(chat_id=chat_id, meme_id=meme_id, message_id=message.message_id)


def _send_user(chat_id, chat_id_rec, telegram_username, message_body, bot):
    bot.send_message(chat_id, message_body.split('^_^')[0] + '^_^')
    # if user don't upload a photo
    bot.send_photo(chat_id, photo=get_profile_value(chat_id_rec, column='photo_id'))

    if get_profile_value(chat_id_rec, column='use_photo'):
        bot.send_photo(chat_id, photo=get_profile_value(chat_id_rec, column='photo_id'))

    if get_profile_value(chat_id_rec, column='use_bio'):
        bio = get_profile_value(chat_id_rec, column='bio')
        if bio:
            bot.send_message(chat_id, bio)

    message = bot.send_message(chat_id, '^_^' + message_body.split('^_^')[1],
                               reply_markup=get_user_reply_inline(telegram_username=telegram_username))

    add_user_user_init(chat_id_obj=chat_id, chat_id_subj=chat_id_rec, message_id=message.message_id)


def _send_user2meme(chat_id, message_body, bot):
    bot.send_message(chat_id, message_body, reply_markup=get_user2meme_reply_inline())


def _send_menu(chat_id, bot, stage):
    message_body, reply_markup = get_reply_markup(stage=stage)
    bot.send_message(chat_id, message_body, reply_markup=reply_markup)
