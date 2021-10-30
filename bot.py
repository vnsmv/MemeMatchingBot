import telebot
import requests
import random
import speech_recognition as sr
import os
from pydub import AudioSegment
#import pyttsx3
import time

token = '2026169199:AAFPR9PnI4989V5AWyeuS2ZDzHMGjobZXmk'
bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['start'])
def start(message):
    username = message.chat.username
    bot.send_message(message.chat.id, 'Привет ' + "\U0001F60A")

# ____________________VOICE PROCESSING____________________

@bot.message_handler(content_types = ['voice'])
def start(message):
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
    src = file_info.file_path[:6] + 'oga' + file_info.file_path[5:]
    dst = file_info.file_path[:6] + 'wav' + file_info.file_path[5:-3] + 'wav'
    print(src)
    with open(src,'wb') as f:
        f.write(file.content)
    file = AudioSegment.from_ogg('./voice/oga/file_3.ogg')
    file.export('notaaudio.wav', format = 'wav')

bot.polling(none_stop=True, interval=0)
