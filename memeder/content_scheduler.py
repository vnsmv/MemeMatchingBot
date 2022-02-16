import datetime
from typing import Union

from memeder.database.db_functions import (
    add_user, user_exist, add_user_meme_reaction, add_meme, add_user_meme_init, add_user_user_init,
    add_user_user_reaction, update_profile, get_profile_value, get_all_user_ids
)
from memeder.interface_tg.config import (
    MEME_BUTTONS, USER_BUTTONS, menu_routing_buttons, menu_update_buttons, MENU_BUTTONS, MATCHING_MESSAGES,
    BORIS_ID, IVAN_API_ID
)
from memeder.interface_tg.meme_reply_keyboard import get_meme_reply_inline, get_user2meme_reply_inline
from memeder.interface_tg.menu_keyboard import get_reply_markup
from memeder.interface_tg.user_profile import get_user_profile
from memeder.meme_recsys.engine import recommend_meme, recommend_user, COLD_START_N_MEME
from memeder.meme_recsys.refreshing_activity import top_memes_selection, is_sending_meme, select_meme
from memeder.interface_tg.glob_messages import msg_g3


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

    _send_menu(chat_id, bot=bot, button='m_start')


def start_meme(message, bot):
    chat_id: int = message.chat.id
    meme_id, file_id, file_type, caption = recommend_meme(chat_id)
    _send_meme(chat_id, meme_id=meme_id, file_id=file_id, file_type=file_type, caption=caption, bot=bot)


def process(call, bot):

    chat_id = call.message.chat.id
    reaction = call.data

    # 0. Checking existence of the user in the database (e.g., the latter was updated):
    if not user_exist(chat_id):
        bot.send_message(chat_id, 'Please, restart the bot (/start), so that we could process your feedback;)')

    else:
        message_id = call.message.message_id

        # 1. Updating meme reactions database:
        if reaction in [v[1] for k, v in MEME_BUTTONS.items() if k.startswith('b')]:

            if reaction == MEME_BUTTONS['bu_users'][1]:
                chat_id_rec, similarity, message_body = _call_user_generator(chat_id=chat_id)
                if chat_id_rec is None:
                    _send_user2meme(chat_id=chat_id, message_body=message_body, bot=bot)
                else:
                    _send_user(chat_id=chat_id, chat_id_rec=chat_id_rec, similarity=similarity, bot=bot)
            else:
                add_user_meme_reaction(chat_id, message_id=message_id, reaction=reaction)

                # 3. recommend new meme
                meme_id, file_id, file_type, caption = recommend_meme(chat_id)
                _send_meme(chat_id, meme_id=meme_id, file_id=file_id, file_type=file_type, caption=caption, bot=bot)

        # 4. Updating users reactions database:
        if reaction in [v[1] for k, v in USER_BUTTONS.items() if k.startswith('b')]:
            add_user_user_reaction(chat_id, message_id=message_id, reaction=reaction)

            if reaction == USER_BUTTONS['bm_memes'][1]:
                # 5. recommend new meme
                meme_id, file_id, file_type, caption = recommend_meme(chat_id)
                _send_meme(chat_id, meme_id=meme_id, file_id=file_id, file_type=file_type, caption=caption, bot=bot)
            else:
                chat_id_rec, similarity, message_body = _call_user_generator(chat_id=chat_id)
                if chat_id_rec is None:
                    _send_user2meme(chat_id=chat_id, message_body=message_body, bot=bot)
                else:
                    _send_user(chat_id=chat_id, chat_id_rec=chat_id_rec, similarity=similarity, bot=bot)

    # TODO: do we need to force dating recommendations?


def receive_content(message, file_type: str, bot):
    chat_id = message.chat.id
    caption = message.caption

    if file_type == 'photo':
        file_id = message.photo[-1].file_id
        file_unique_id = message.photo[-1].file_unique_id

        if get_profile_value(chat_id, column='photo_update_flag'):
            update_profile(chat_id=chat_id, column='photo_id', value=file_id)
            update_profile(chat_id=chat_id, column='photo_unique_id', value=file_unique_id)
            update_profile(chat_id=chat_id, column='use_photo', value=True)
            update_profile(chat_id=chat_id, column='photo_update_flag', value=False)
            bot.send_photo(chat_id, photo=file_id, caption=MENU_BUTTONS['r3_photo'][1])
            _send_menu(chat_id=chat_id, bot=bot, button='m_main_menu')

        elif chat_id in (BORIS_ID, IVAN_API_ID, ):
            add_meme(file_id=file_id, file_unique_id=file_unique_id, chat_id=chat_id, file_type=file_type,
                     caption=caption)

    elif file_type == 'video':
        file_id = message.video.file_id
        file_unique_id = message.video.file_unique_id
        add_meme(file_id=file_id, file_unique_id=file_unique_id, chat_id=chat_id, file_type=file_type, caption=caption)

    elif file_type == 'animation':
        file_id = message.animation.file_id
        file_unique_id = message.animation.file_unique_id
        add_meme(file_id=file_id, file_unique_id=file_unique_id, chat_id=chat_id, file_type=file_type, caption=caption)


def menu_routing(message, bot):
    text2button = {MENU_BUTTONS[b][0]: b for b in menu_routing_buttons}
    _send_menu(chat_id=message.chat.id, bot=bot, button=text2button[message.text])


def menu_update(message, bot):
    chat_id = message.chat.id

    text2button_data = {MENU_BUTTONS[b][0]: MENU_BUTTONS[b] for b in menu_update_buttons}
    button_data = text2button_data[message.text]

    update_profile(chat_id=chat_id, column=button_data[2], value=button_data[3])
    bot.send_message(chat_id, button_data[1])
    _send_menu(chat_id=chat_id, bot=bot, button='m_main_menu')


def menu_show_profile(message, bot):
    chat_id = message.chat.id
    photo_id, profile_description, _ = get_user_profile(chat_id=chat_id, similarity=100)
    bot.send_photo(chat_id, photo=photo_id, caption=profile_description)
    _send_menu(chat_id=chat_id, bot=bot, button='m_main_menu')


def check_receive_bio(message, bot):
    chat_id = message.chat.id
    if get_profile_value(chat_id, column='bio_update_flag'):
        update_profile(chat_id=chat_id, column='bio', value=message.text)
        update_profile(chat_id=chat_id, column='use_bio', value=True)
        update_profile(chat_id=chat_id, column='bio_update_flag', value=False)
        bot.send_message(chat_id, MENU_BUTTONS['r3_bio'][1] + message.text)
        _send_menu(chat_id=chat_id, bot=bot, button='m_main_menu')
    else:  # interpret as a start:
        start(message, bot)


def message_all(message, bot):

    msg = msg_g3

    host_id = message.chat.id
    if host_id == BORIS_ID:
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
    if host_id == BORIS_ID:
        chat_ids = get_all_user_ids()
        top_meme_ids, _, _ = top_memes_selection()

        for chat_id in chat_ids:
            # if chat_id in (481807223, 354637850, 11436017):
            if is_sending_meme(chat_id=chat_id, time_delta=datetime.timedelta(days=2)):
                meme_id, file_id, file_type, caption = select_meme(chat_id, top_meme_ids)
                if meme_id is None:
                    meme_id, file_id, file_type, caption = recommend_meme(chat_id)

                try:
                    _send_meme(chat_id, meme_id=meme_id, file_id=file_id, file_type=file_type, caption=caption, bot=bot)
                    print(f'Sent a refresh meme {meme_id} to {chat_id}', flush=True)
                except Exception:
                    print(f'Failed to send a refresh meme {meme_id} to {chat_id}', flush=True)
                    pass


def top10memes(message, bot):
    # TODO: auto process + weekly process
    if message.chat.id == BORIS_ID:
        memes_info = (
            (4931, 'AgACAgQAAxkBAAEBHWRiBIBj_ONuIYBP2P40GEAoFPQLggAC7aoxG5SqnFBgFytBrBrHdwEAAwIAA3cAAyME', 'photo', None),
            (3465, 'AgACAgQAAxkBAAEBDpViBChDXzco8wpn0iPaBWz8K9FRdAACQ6sxG7BFvFEZKHmq8z51oQEAAwIAA3kAAyME', 'photo',
             "We've struck the mother load"),
            (1996, 'AgACAgQAAxkBAAITe2Gxdx13TCQEFKOl0KCRE9tGP9STAALDqzEbNpEUUssRiHZtbc2bAQADAgADeAADIwQ', 'photo', None),
            (278, 'AgACAgQAAxkBAAIGG2Gwjsp6BEJMMOo7KeHXqhGYtlnMAAKxqjEb7-TtUSu1LwcpsE4MAQADAgADdwADIwQ', 'photo', None),
            (2878, 'AgACAgIAAxkBAAL-pGIEBNdoqFs9CbbeKsYSIBwcP_tcAAITuDEbvki5S4GkgVazHRkXAQADAgADeAADIwQ', 'photo', None),
            (2690, 'AgACAgQAAxkBAAIWimGxo9iFvx2T8BnRIZWkYqtkSiDgAALrqjEbyyxFUNGCOigw1Qd0AQADAgADeQADIwQ', 'photo', None),
            (88, 'AgACAgIAAxkBAAIFImGv1rpwuogl0s6GFW80KVhcwVv3AALmrjEb2wrJScTxuvwoa1cxAQADAgADeAADIwQ', 'photo', None),
            (509, 'AgACAgQAAxkBAAIH9GGwxbpb_KfJyF-gPvPBaFrSlI83AAL1qjEb2f6kUapKNH9tfgn_AQADAgADeQADIwQ', 'photo', None),
            (239, 'AgACAgIAAxkBAAIF7GGwjCblvT2ny4vq2eSIAvmrnyITAAJgtjEbrLuJSCDarwOKXNKGAQADAgADeQADIwQ', 'photo', None),
            (253, 'AgACAgQAAxkBAAIGAAFhsI1KGUX5CXDNm2rcxdpqadFBtQACWqsxGx07rFDeqiu5cdYtUwEAAwIAA3kAAyME', 'photo', None),
        )
        for m in memes_info:
            try:
                _send_meme(chat_id=BORIS_ID, meme_id=m[0], file_id=m[1], file_type=m[2], caption=m[3], bot=bot,
                           uploading_content=True)
            except Exception:
                pass


def _call_user_generator(chat_id):
    chat_id_rec, similarity, n_reactions_to_do = recommend_user(chat_id=chat_id)

    if n_reactions_to_do == 0:
        message_body = None  # OK
    elif n_reactions_to_do > 0:
        message_body = MATCHING_MESSAGES[1].format(COLD_START_N_MEME, n_reactions_to_do)
    else:  # n_reactions_to_do < 0:  # --> and it's an error code
        message_body = MATCHING_MESSAGES[n_reactions_to_do]
    return chat_id_rec, similarity, message_body


def _send_meme(chat_id, meme_id, file_id, file_type, caption, bot, uploading_content: bool = False):
    reply_markup = None if uploading_content else get_meme_reply_inline()
    if file_type == 'photo':
        message = bot.send_photo(chat_id, photo=file_id, caption=caption, reply_markup=reply_markup)
    elif file_type == 'video':
        message = bot.send_video(chat_id, video=file_id, caption=caption, reply_markup=reply_markup)
    else:  # file_type == 'animation':
        message = bot.send_animation(chat_id, animation=file_id, caption=caption, reply_markup=reply_markup)

    if not uploading_content:
        add_user_meme_init(chat_id=chat_id, meme_id=meme_id, message_id=message.message_id)


def _send_user(chat_id, chat_id_rec, similarity, bot):
    photo_id, profile_description, user_reply_markup = get_user_profile(chat_id=chat_id_rec, similarity=similarity)
    message = bot.send_photo(chat_id, photo=photo_id, caption=profile_description, reply_markup=user_reply_markup)
    add_user_user_init(chat_id_obj=chat_id, chat_id_subj=chat_id_rec, message_id=message.message_id)


def _send_user2meme(chat_id, message_body, bot):
    bot.send_message(chat_id, message_body, reply_markup=get_user2meme_reply_inline())


def _send_menu(chat_id, bot, button):
    message_body, reply_markup = get_reply_markup(button=button)
    bot.send_message(chat_id, message_body, reply_markup=reply_markup)
