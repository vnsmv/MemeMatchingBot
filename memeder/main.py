import argparse

import telebot

from memeder.content_scheduler import start, process, receive_meme
from memeder.bot_credentials import token, token_test


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', required=False, action='store_true', default=False)
    args = parser.parse_known_args()[0]
    is_test = args.test

    _token = token_test if is_test else token
    bot = telebot.TeleBot(_token)

    # TODO: how can we check (and refresh) the current state?
    #  ... a "bug" in @ffmemesbot with double meme caused by double /start command without reacting on prev. meme

    @bot.message_handler(commands=['start'])
    def _start(message):
        start(message, bot, force_start=True, test=is_test)

    @bot.callback_query_handler(func=lambda call: True)
    def _handle_meme_reply(call):
        process(call, bot, test=is_test)
        bot.answer_callback_query(call.id)

    @bot.message_handler(content_types=['photo'])
    def _handle_photo(message):
        receive_meme(message=message, test=is_test)

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
