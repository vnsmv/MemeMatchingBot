import argparse
import os

import telebot

from memeder.content_scheduler import start, process, receive_meme


def main():
    token = os.environ.get('MEMEDATINGTESTBOT_TOKEN')

    bot = telebot.TeleBot(token)

    # TODO: how can we check (and refresh) the current state?
    #  ... a "bug" in @ffmemesbot with double meme caused by double /start command without reacting on prev. meme

    @bot.message_handler(commands=['start'])
    def _start(message):
        start(message, bot, force_start=True)

    @bot.callback_query_handler(func=lambda call: True)
    def _handle_meme_reply(call):
        process(call, bot)
        bot.answer_callback_query(call.id)

    @bot.message_handler(content_types=['photo'])
    def _handle_photo(message):
        receive_meme(message=message, test=is_test)

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
