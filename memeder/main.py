import telebot

# from bot_functions import listofmemes, GeneratorMeme
# from database_functions import CheckInDb

from memeder.content_scheduler import start
from memeder.meme_generator import listofmemes, GeneratorMeme


# filename = context.bot.get_file(update.message.photo[-1].file_id)
# with open(filename, 'rb') as file:
#     blobData = file.read()
#
# print(blobData)

# @bot.message_handler(content_types=['text'])
# def text_handler(message):
#
#     cool_phrases = ["Я никогда не"]
#     name = message.text
#     intro = 'Продолжи фразу: \n'
#     phrase = random.choice(cool_phrases)
#     bot.send_message(message.chat.id, intro +  phrase)
#     phrase = phrase + message.text
#
#     start_butt = types.InlineKeyboardButton(text='начать!', callback_data =str(I_mus)  + '|''stmus'+username )
#     markup_inline.add(start_butt)


def main():
    token = '2119626828:AAFAKpu-nCf520e-peCEyM8e9sjJuZRlIdI'
    bot = telebot.TeleBot(token)

    lm = listofmemes()
    meme_generator = GeneratorMeme(lm, 10)

    # TODO: how can we check (and refresh) the current state?
    #  ... a "bug" in @ffmemesbot with double meme caused by double /start command without reacting on prev. meme
    @bot.message_handler(commands=['start'])
    def _start(message):
        start(message, bot=bot, meme_generator=meme_generator)

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
