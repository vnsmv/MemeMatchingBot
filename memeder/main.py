import argparse
import os

import telebot
from dotenv import load_dotenv

from memeder.paths import get_py_lib_path
from memeder.content_scheduler import start, process, receive_meme, start_meme, menu_routing, menu_update


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

    # ### Menu: ###
    @bot.message_handler(content_types=['text'],
                         func=lambda msg: msg.text in ['<< BACK TO MEMES'])
    def _start_meme(message):
        start_meme(message, bot)

    @bot.message_handler(content_types=['text'],
                         func=lambda msg: msg.text in ['Set privacy', 'Set preferences', 'Set goals', 'Profile',
                                                       'Choose sex', '<< main menu', '<< profile settings'])
    def _menu_routing(message):
        menu_routing(message, bot)

    @bot.message_handler(content_types=['text'],
                         func=lambda msg: msg.text in ['Seen to males', 'Seen to females', 'Seen to all',
                                                       'Seen to nobody', 'Show me males', 'Show me females',
                                                       'Show me all', 'Show me only memes', 'Friends', 'Relationships',
                                                       'Unspecified', 'Only memes', 'Upload bio', 'Upload photo',
                                                       'Clear bio', 'Clear photo', 'Male', 'Female',
                                                       'Prefer not to say'])
    def _menu_update(message):
        menu_update(message, bot)

    # ### Processing reactions: ###
    @bot.callback_query_handler(func=lambda call: True)
    def _handle_meme_reply(call):
        process(call, bot)
        bot.answer_callback_query(call.id)

    # ### Receiving memes: ###
    @bot.message_handler(content_types=['photo'])
    def _handle_photo(message):
        receive_meme(message=message)

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
