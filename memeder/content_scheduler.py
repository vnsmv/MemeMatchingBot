from typing import Union

from memeder.database.db_functions import add_user, user_exist, add_user_meme_reaction, \
    add_meme, add_user_meme_init
from memeder.interface_tg.config import REACTIONS2BUTTONS
from memeder.interface_tg.meme_reply_keyboard import get_meme_reply_inline
from memeder.meme_recsys.engine import recommend_meme


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

    # 1. Updating meme reactions database:
    message_id = call.message.message_id

    if reaction in [v[1] for k, v in REACTIONS2BUTTONS.items() if k.startswith('b')]:
        add_user_meme_reaction(chat_id, message_id=message_id, reaction=reaction)

    # 2. Check is the person ready to date:
    # if is_ready_to_date(chat_id, database_src=database_src):
    #     recommended_users = recommend_date(chat_id, database_src=database_src)
    #     _send_date(chat_id, recommended_users, bot=bot)
    #
    meme_id, file_id = _call_meme_generator(chat_id)
    _send_meme(chat_id, meme_id=meme_id, file_id=file_id, bot=bot)


def receive_meme(message):
    if message.chat.id in (354637850, 2106431824, ):  # Boris, ffmemesbot (API proxy), ...
        add_meme(file_id=message.photo[-1].file_id, chat_id=message.chat.id, file_type='photo')


def _call_meme_generator(chat_id):
    meme_id, file_id = recommend_meme(chat_id)
    return meme_id, file_id


def _send_meme(chat_id, meme_id, file_id, bot):

    bot.send_photo(chat_id, photo=file_id)
    message = bot.send_message(chat_id, 'How do you like it?', reply_markup=get_meme_reply_inline())
    add_user_meme_init(chat_id=chat_id, meme_id=meme_id, message_id=message.message_id)


def _send_date(chat_id, recommended_users, bot):
    recommended_users_str = ', '.join(['_id' + str(u) for u in recommended_users])
    bot.send_message(chat_id,
                     f'We recommend you to date with users that have following chat IDs: '
                     f'{recommended_users_str}. Now go find them. '
                     f'(This feature is not implemented yet. '
                     f'Please, continue to watch the same memes again and again. '
                     f'We definitely update them... maybe.)')
