# -*- coding: utf-8 -*-
import telebot
import requests
import random
import os

import time
from telebot import types

token = '2119626828:AAFAKpu-nCf520e-peCEyM8e9sjJuZRlIdI'
bot = telebot.TeleBot(token)

from bot_functions import listofmemes, GeneratorMeme
from database_functions import CheckInDb

lm = listofmemes()
meme_generator  = GeneratorMeme(lm,10)

@bot.message_handler(commands = ['start'])
def start(message):

    username = message.chat.username
    user_id, if_exist = CheckInDb(username)
    print(user_id)
    if if_exist == False:
        bot.send_message(message.chat.id, 'Как тебя зовут?')

    markup_inline_ = types.InlineKeyboardMarkup()
    meme = next(meme_generator)

    bot.send_photo(message.chat.id, photo=open('./Memes/'+meme, 'rb'))
    stress = types.InlineKeyboardButton(text='\U0001F624', callback_data = '\U0001F624')
    rocket = types.InlineKeyboardButton(text='\U0001F680', callback_data = '\U0001F680')
    neutral= types.InlineKeyboardButton(text='\U0001F610', callback_data = '\U0001F610')
    chill = types.InlineKeyboardButton(text='\U0001F60C', callback_data = '\U0001F60C')
    cry = types.InlineKeyboardButton(text='\U0001F622', callback_data = '\U0001F622')
    markup_inline_.row(stress, rocket, neutral, chill, cry)
    bot.send_message(message.chat.id, 'Hello', reply_markup = markup_inline_)

    filename = context.bot.get_file(update.message.photo[-1].file_id)
    with open(filename, 'rb') as file:
        blobData = file.read()

    print(blobData)

@bot.message_handler(content_types=['text'])
def text_handler(message):

    cool_phrases = ["Я никогда не"]
    name = message.text
    intro = 'Продолжи фразу: \n'
    phrase = random.choice(cool_phrases)
    bot.send_message(message.chat.id, intro +  phrase)
    phrase = phrase + message.text

    start_butt = types.InlineKeyboardButton(text='начать!', callback_data =str(I_mus)  + '|''stmus'+username )
    markup_inline.add(start_butt)

bot.polling(none_stop=True, interval=0)
