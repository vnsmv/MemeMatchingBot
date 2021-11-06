# -*- coding: utf-8 -*-
import telebot
import requests
import random
import os
from pydub import AudioSegment
#import pyttsx3
import time
import uuid
import pydub
from telebot import types
from pathlib import Path
##########################################################
# ____________________IMPORT FUNCTIONS____________________
from speech_processing import speech_metrics
from calculate_stress import stress_percantage, append_gsheets,random_talks
from psychology_help import RandomPeopleHelpers, MoodTable
########################################################
# ____________________BOT ATTRIBUTES____________________

token = '2026169199:AAFPR9PnI4989V5AWyeuS2ZDzHMGjobZXmk'
bot = telebot.TeleBot(token)

###################################################
# ____________________SRART BOT____________________

@bot.message_handler(commands = ['start'])
def start(message):
    username = message.chat.username
    markup_inline_ = types.InlineKeyboardMarkup()

    # buttons
    bot.send_message(message.chat.id, 'Привет, на связи TalkToMe version 1.0.1. \n' +
    'Пока я работаю над предсказанием уровня стресса по голосу и видео, но вот что я умею сейчас: \n'+
    '• Веду дневник твоего состояния на каждый день\n' +
    '• Можешь поделиться своими проблемами и поговорить с кем-нибудь \n'
    )

    stress = types.InlineKeyboardButton(text='\U0001F624', callback_data = '\U0001F624')
    rocket = types.InlineKeyboardButton(text='\U0001F680', callback_data = '\U0001F680')
    neutral= types.InlineKeyboardButton(text='\U0001F610', callback_data = '\U0001F610')
    chill = types.InlineKeyboardButton(text='\U0001F60C', callback_data = '\U0001F60C')
    cry = types.InlineKeyboardButton(text='\U0001F622', callback_data = '\U0001F622')
    markup_inline_.row(stress, rocket,neutral,chill,cry)
    bot.send_message(message.chat.id, 'Привет, как прошел твой день?', reply_markup = markup_inline_)
    #bot.send_message(message.chat.id, 'Запиши голосовое, хочу послушать тебя. Только рассказывай подробно' + "\U0001F60A")
    #bot.send_message(message.chat.id, str(stress_percantage(username)))

##########################################################
# ____________________VOICE PROCESSING____________________

@bot.message_handler(content_types = ['voice'])
def message(message):

    # processing voice message
    username = message.chat.username
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = str(uuid.uuid4())
    file_name_full = "./voice/"+filename+".ogg"
    file_name_full_wav = "./voice/"+filename+".wav"
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)

    file = AudioSegment.from_ogg(Path(file_name_full))
    file.export(file_name_full_wav, format = 'wav')
    os.remove(file_name_full)

    #calculate speech metrics
    try:
        if username[0] == '@':
            username = username[1:]
    except TypeError:
        pass

    speech_data = speech_metrics(username, file_name_full_wav)
    stress_level = round(stress_percantage(username))
    #________________________________________________
    #                     BOT REPLY
    #________________________________________________
    if stress_level == 101:
        bot.send_message(message.chat.id, 'Возможно вы неправильно ввели свой username. Напишите @followthesun ' )
    else:
        # append data to gsheets
        speech_data += f' {stress_level}'
        append_gsheets(speech_data)
        os.remove(file_name_full_wav)
        # bot.send_message(message.chat.id, 'Голос такой приятный ' + "\U0001F60C" + '\n' + 'Я посчитала твой уровень стресса...' +
        #  '\n' +str(stress_level)+ '/100')
        # time.sleep(2)
        # if stress_level < 25:
        #     bot.send_message(message.chat.id, 'На чиле, на расслабоне ' + "\U0001F60E" + "\U0001F919")
        # elif stress_level > 25 and stress_level < 45:
        #     bot.send_message(message.chat.id, 'Тебе нужно немного отвлечься от повседневной рутины\n' + 'A little party never killed nobody' + "\U0001F483")
        # elif stress_level > 45 and stress_level < 80:
        #     bot.send_message(message.chat.id,  'Тебе нужен отдых! \n'+
        #     'Почитай статьи о выгорании\n https://probolezny.ru/emocionalnoe-vygoranie/ \n' +
        #     'https://www.gq.ru/entertainment/burn-out \n'+
        #     'Займись йогой https://www.youtube.com/c/yogawithadriene \n' +
        #     'Смени обстановку https://vandrouki.ru/ \n ')
        # elif stress_level > 80:
        #     bot.send_message(message.chat.id, 'Это очень высокий уровень , тебе требуется немедленная консультация с психологом.\n' +'\n'+ 'Горячая линия 88007008805')
        # time.sleep(2)
        #bot.send_message(message.chat.id, 'Полученные от тебя метариалы позволят создать приложение, где на основе AI оценивалось бы психологическое состояние человека.' +
        #'\nМы верим, что вместе сможем сделать действительно классный продукт и уменьшить проблему выгорания\n' + 'Если у тебя есть вопросы или ты хочешь стать частью нашей команды - пиши:\n'
        # + '@followthesun, @spatzie, @anvlasova, @Penchekrak')
        markup_inline_ = types.InlineKeyboardMarkup()

        want_to_talk = types.InlineKeyboardButton(text='Да', callback_data = 'ok')
        markup_inline_.add(want_to_talk)
        bot.send_message(message.chat.id, 'Хочешь поговорить?', reply_markup = markup_inline_)

#________________________________________________
#                     TEXT PROCESSING
#________________________________________________
@bot.message_handler(content_types = ['text'])
def message(message):
    bot.send_message(message.chat.id, 'Давай голосовым ' + "\U0001F60F")

#________________________________________________
#                     CALLBACK HANDLING
#________________________________________________
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data in ['\U0001F624','\U0001F680','\U0001F610','\U0001F60C','\U0001F622']:
        moods = MoodTable(call.message.chat.username, call.data)
        moods_str = ''
        for mood in moods:
            moods_str = moods_str + mood + '\n'
        bot.send_message(call.message.chat.id, 'Твои последние состояния: \n' + moods_str )

        yes = types.InlineKeyboardButton(text='Да', callback_data = 'yes')
        no = types.InlineKeyboardButton(text='Нет', callback_data = 'no')
        markup_inline_ = types.InlineKeyboardMarkup()
        markup_inline_.add(yes, no)
        bot.send_message(call.message.chat.id, 'Хочешь поговорить?', reply_markup = markup_inline_)
    if call.data == 'yes':
        person_talk  = RandomPeopleHelpers()
        if call.data == 'yes':
            if person_talk[0] != '@':
                person_talk = '@' + person_talk
            markup_inline_ = types.InlineKeyboardMarkup()
            try_another = types.InlineKeyboardButton(text = 'Поискать  еще', callback_data = 'yes')
            markup_inline_.add(try_another)
            bot.send_message(call.message.chat.id, 'Нашла тебе собеседника \n' + person_talk, reply_markup = markup_inline_)

bot.polling(none_stop=True, interval=0)
