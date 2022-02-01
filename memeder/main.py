import argparse
import os

import telebot
from dotenv import load_dotenv

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

    bot = telebot.TeleBot(token)

    # ### Starting: ###
    @bot.message_handler(commands=['start'])
    def _start(message):
        start(message, bot)

    # ### Send message to all: ###
    @bot.message_handler(commands=['post'])
    def _message_all(message):
        message_all(message, bot)

    # ### Send message to all: ###
    @bot.message_handler(commands=['sendmeme'])
    def _meme_all(message):
        meme_all(message, bot)

    # ### Menu: ###
    @bot.message_handler(content_types=['text'],
                         func=lambda msg: msg.text in ['\U0001F519'])
    def _start_meme(message):
        start_meme(message, bot)

    @bot.message_handler(content_types=['text'],
                         func=lambda msg: msg.text in ['Sex \U0001F466  \U0001F467',
                                                       'Matches preferences', 'I am searching for \U0001F498 \U0001F923',
                                                       'Edit Profile \U0001F58A \U0001F320', '\U0001F519'])
    def _menu_routing(message):
        menu_routing(message, bot)

    @bot.message_handler(content_types=['text'],
                         func=lambda msg: msg.text in ['Boys \U0001F466', 'Girls \U0001F469', 'All \U0001F469 \U0001F9D1',
                                                       'Only memes \U0001F60E', 'Friends \U0001F92A', 'Relationships \U0001F498', "I don't know \U0001F914",
                                                       'Just kill my free time \U0001F63C', 'Bio \U0001F53C', 'Photo \U0001F53C', 'Clear bio \U0001F6AB',
                                                       'Clear photo \U0001F6AB', 'Boy \U0001F468', 'Girl \U0001F469', 'Prefer not to say'])
    def _menu_update(message):
        menu_update(message, bot)

    @bot.message_handler(content_types=['text'])
    def _check_receive_bio(message):
        check_receive_bio(message)

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
