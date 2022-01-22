import os

import telebot

from memeder.content_scheduler import start, process, receive_meme


def main():
    token = os.environ.get('MEMEDATINGTESTBOT_TOKEN')
    if token is None:
        token = os.environ.get('MEMEDATINGBOT_TOKEN')
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
