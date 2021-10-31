import telebot
import requests
import random
import os
from pydub import AudioSegment
#import pyttsx3
import time
import uuid
import pydub
from pathlib import Path
##########################################################
# ____________________IMPORT FUNCTIONS____________________
from speech_processing import speech_metrics
from calculate_stress import stress_percantage, append_gsheets
########################################################
# ____________________BOT ATTRIBUTES____________________

token = '2026169199:AAFPR9PnI4989V5AWyeuS2ZDzHMGjobZXmk'
bot = telebot.TeleBot(token)

###################################################
# ____________________SRART BOT____________________

@bot.message_handler(commands = ['start'])
def start(message):
    username = message.chat.username
    bot.send_message(message.chat.id, 'Привет, расскажи мне как прошел твой день)')
    time.sleep(2)
    bot.send_message(message.chat.id, 'Запиши голосовое, хочу послушать тебя. Только рассказывай подробно)' + "\U0001F60A")
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
    speech_data = speech_metrics(username, file_name_full_wav)
    stress_level = round(stress_percantage(username))
    # append data to gsheets
    speech_data += f' {stress_level}'
    append_gsheets(speech_data)
    bot.send_message(message.chat.id, 'Голос такой приятный ' + "\U0001F60C" + '\n' + 'Я посчитала твой уровень стресса...' +
     '\n' +str(stress_level)+ '/100')
    time.sleep(2)
    if stress_level < 20:
        bot.send_message(message.chat.id, 'На чиле, на расслабоне ' + "\U0001F60E" + "\U0001F919")
    elif stress_level > 20 and stress_level < 40:
        bot.send_message(message.chat.id, 'Тебе нужно отвлечься от повседневной рутины\n' + 'A little party never killed nobody' + "\U0001F483")
    elif stress_level > 40 and stress_level < 80:
        bot.send_message(message.chat.id,  'Тебе нужен отдых! \n'+
        'Почитай статьи о выгорании\n https://probolezny.ru/emocionalnoe-vygoranie/ \n' +
        'https://www.gq.ru/entertainment/burn-out \n'+
        'Займись йогой https://www.youtube.com/c/yogawithadriene \n' +
        'Смени обстановку https://vandrouki.ru/ \n ')
    elif stress_level > 80:
        bot.send_message(message.chat.id, 'Это очень высокий уровень , тебе требуется немедленная консультация с психологом.\n' +'\n'+ 'Горячая линия 88007008805')
    time.sleep(2)
    bot.send_message(message.chat.id, 'Полученные от тебя метариалы позволят создать приложение, где на основе AI оценивалось бы психологическое состояние человека.' +
    '\nМы верим, что вместе сможем сделать действительно классный продукт и уменьшить проблему выгорания:) \n' + 'Если у тебя есть вопросы или ты хочешь стать частью нашей команды - пиши:\n'
     + '@followthesun, @spatzie, @anvlasova, @Penchekrak')


##########################################################
# ____________________TEXT PROCESSING____________________
@bot.message_handler(content_types = ['text'])
def message(message):
    bot.send_message(message.chat.id, 'Давай голосовым ' + "\U0001F60F")

bot.polling(none_stop=True, interval=0)
