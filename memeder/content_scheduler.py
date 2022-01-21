from typing import Union

from memeder.database.db_functions import add_user, user_exist, add_user_meme_reaction, \
    add_meme, add_user_meme_init, add_user_user_init, add_user_user_reaction
from memeder.interface_tg.config import MEME_REACTION2BUTTON, USER_REACTION2BUTTON
from memeder.interface_tg.meme_reply_keyboard import get_meme_reply_inline, get_user_reply_inline, \
    get_user2meme_reply_inline
from memeder.meme_recsys.engine import recommend_meme, recommend_user


# https://core.telegram.org/bots/api#message +
# https://github.com/eternnoir/pyTelegramBotAPI#types =
# https://core.telegram.org/bots/api#user
# https://core.telegram.org/bots/api#chat


def start(message, bot, force_start: bool = True):

    user = message.from_user
    chat = message.chat
    user_id: int = user.id
    user_first_name: str = user.first_name
    tg_username: Union[str, None] = user.username
    chat_id: int = chat.id
    # user_is_bot: bool = user.is_bot  # TODO: we can set filtering behavior for bots
    # user_last_name: Union[str, None] = user.last_name

    if not user_exist(chat_id):
        add_user(user_first_name, user_id, tg_username, chat_id, '')

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
            add_error = add_user_user_reaction(chat_id, message_id=message_id, reaction=reaction)

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


def receive_meme(message):
    if message.chat.id in (354637850, 2106431824, ):  # Boris, ffmemesbot (API proxy), ...
        add_meme(file_id=message.photo[-1].file_id, chat_id=message.chat.id, file_type='photo')


def _call_meme_generator(chat_id):
    meme_id, file_id = recommend_meme(chat_id)
    return meme_id, file_id


def _call_user_generator(chat_id):
    chat_id_rec, telegram_username, name, n_reactions_to_do = recommend_user(chat_id=chat_id)

    if n_reactions_to_do > 0:
        message_body = f'To calculate the best match for you, '\
            f'we need more meme reactions. Enjoy {n_reactions_to_do} more memes:)'
    elif n_reactions_to_do == -1:
        message_body = 'Now, we need some time to update recommendations... ' \
                       'Or you are crazy enough to review all users O.O. ' \
                       'You may enjoy more memes for now, ' \
                       'and do not forget to share this bot with your friends;)'
    else:  # n_reactions_to_do == 0:
        message_body = f'We have found {name} for you. ^_^ ' \
            f'You can jump right to the chat with {name}, ' \
            f'or react and get the next recommendation.'
    return chat_id_rec, telegram_username, message_body


def _send_meme(chat_id, meme_id, file_id, bot):
    bot.send_photo(chat_id, photo=file_id)
    message = bot.send_message(chat_id, 'How do you like it?', reply_markup=get_meme_reply_inline())
    add_user_meme_init(chat_id=chat_id, meme_id=meme_id, message_id=message.message_id)


def _send_user(chat_id, chat_id_rec, telegram_username, message_body, bot):
    message = bot.send_message(chat_id, message_body,
                               reply_markup=get_user_reply_inline(telegram_username=telegram_username))
    add_user_user_init(chat_id_obj=chat_id, chat_id_subj=chat_id_rec, message_id=message.message_id)


def _send_user2meme(chat_id, message_body, bot):
    bot.send_message(chat_id, message_body, reply_markup=get_user2meme_reply_inline())
