import argparse
import os

import telebot
from dotenv import load_dotenv

from memeder.paths import get_py_lib_path
from memeder.content_scheduler import start, process, receive_meme


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

    @bot.message_handler(commands=['start'])
    def _start(message):
        start(message, bot, force_start=True)

    @bot.callback_query_handler(func=lambda call: True)
    def _handle_meme_reply(call):
        process(call, bot)
        bot.answer_callback_query(call.id)

    @bot.message_handler(content_types=['photo'])
    def _handle_photo(message):
        receive_meme(message=message)

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
