import telebot
import requests
import random
import speech_recognition as sr
import os
from pydub import AudioSegment
#import pyttsx3
import time
import uuid
import pydub
from pathlib import Path
import librosa
import librosa.display
import numpy as np

##########################################################
# ____________________IMPORT FUNCTIONS____________________
#from speech_processing import speech_metrics
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
    bot.send_message(message.chat.id, 'Привет ' + "\U0001F60A")
    bot.send_message(message.chat.id, str(stress_percantage(username)))

##########################################################
# ____________________VOICE PROCESSING____________________

@bot.message_handler(content_types = ['voice'])
def start(message):
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
    y, sr = librosa.load(file_name_full_wav, mono=True, duration=30)
    rms = librosa.feature.rms(y=y)
    chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y = y, sr = sr)
    to_append = f'{username} {np.mean(chroma_stft)} {np.mean(rms)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'

    stress_level = stress_percantage(username)
    to_append += f '{stress_level}'

    for e in mfcc:
        to_append += f' {np.mean(e)}'
    append_gsheets(to_append)

bot.polling(none_stop=True, interval=0)
