import argparse
import os

import telebot
from dotenv import load_dotenv

from memeder.interface_tg.config import MENU_BUTTONS, menu_routing_buttons, menu_update_buttons
from memeder.paths import get_py_lib_path
from memeder.content_scheduler import start, process, receive_photo, start_meme, menu_routing, menu_update, \
    check_receive_bio, message_all, meme_all


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=False, type=str, choices=('test', 'deploy'), default=None)
    args = parser.parse_known_args()[0]

    if args.host is None:
        pass
        # (env variable on heroku platform)
    elif args.host == 'test':
        load_dotenv(get_py_lib_path() / 'test.env')
    else:  # args.host == 'deploy':
        load_dotenv(get_py_lib_path() / 'deploy.env')

    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if token is None:
        raise EnvironmentError('No token variable found in the current environment.')

    _menu_routing_texts = [MENU_BUTTONS[b][0] for b in menu_routing_buttons]
    _menu_update_texts = [MENU_BUTTONS[b][0] for b in menu_update_buttons]

    bot = telebot.TeleBot(token)

    # ### Starting: ###
    @bot.message_handler(commands=['start'])
    def _start(message):
        start(message, bot)

    # ### Send message to all: ###
    @bot.message_handler(commands=['post'])
    def _message_all(message):
        message_all(message, bot)

    # ### Send refreshing meme: ###
    @bot.message_handler(commands=['sendmeme'])
    def _meme_all(message):
        meme_all(message, bot)

    # ### Menu: ###
    @bot.message_handler(content_types=['text'], func=lambda msg: msg.text == MENU_BUTTONS['m0_memes'][0])
    def _start_meme(message):
        start_meme(message, bot)

    @bot.message_handler(content_types=['text'], func=lambda msg: msg.text in _menu_routing_texts)
    def _menu_routing(message):
        menu_routing(message, bot)

    @bot.message_handler(content_types=['text'], func=lambda msg: msg.text in _menu_update_texts)
    def _menu_update(message):
        menu_update(message, bot)

    @bot.message_handler(content_types=['text'])
    def _check_receive_bio(message):
        check_receive_bio(message, bot)

    # ### Processing reactions: ###
    @bot.callback_query_handler(func=lambda call: True)
    def _handle_meme_reply(call):
        process(call, bot)
        bot.answer_callback_query(call.id)

    # ### Receiving memes: ###
    @bot.message_handler(content_types=['photo'])
    def _handle_photo(message):
        receive_photo(message=message)

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
