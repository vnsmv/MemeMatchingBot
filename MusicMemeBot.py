import telebot
from telebot import types
import urllib
import dropbox
import re
import random
import gspread
import spotipy
from telebot import types
from spotipy.oauth2 import SpotifyOAuth
from spotipy import oauth2
import time

from oauth2client.service_account import ServiceAccountCredentials
from parsing_memes import meme_matching, find_link_photo
from parsing_db import parsing, obtain_songs
from parsing_dropbox import photo
from spotify import put_playlist_to_db

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('mypython-326612-6af17f4344e7.json', scope)
client = gspread.authorize(creds)
spreadsheet  = client.open("_Tilda_Form_4559105_20210922195121X_")
sheet = spreadsheet.sheet1


bot = telebot.TeleBot('2037831985:AAGKohGKMRlAH-LuciaVefOzNPoN0kyfWIw')

@bot.message_handler(commands=['start'])

def start(message):

    meme_match_dict = []
    bot.send_message(message.chat.id, 'Привет!\nЯ помогаю найти соедей, используя твои предпочтения в быту и с учетом мемов, которые ты выбрал\nCreated by team 43 in Innowation Workshop @skoltech' +''+'\n@followthesun, @sub_mar, @annetta897, @artem_vergazov, @A_dderal')
    I_mem, I_mus = 0, 0
    username = message.chat.username
    #user_char_data
    markup_inline = types.InlineKeyboardMarkup()
    yes_butt = types.InlineKeyboardButton(text = 'Музыка', callback_data = str(I_mus)  + '|' + 'yemus' + username)
    no_butt = types.InlineKeyboardButton(text = 'Юмор', callback_data = str(I_mem)  + '|' +'stmem' + username)
    markup_inline.add(yes_butt, no_butt)
    bot.send_message(message.chat.id, 'Хотите мэтчи по музыке или по юмору?\n Для мэтчей по музыке нужен аккаунт в Spotify', reply_markup = markup_inline)

@bot.callback_query_handler(func=lambda call: True)
def start_callback(call):
    try:
        bot.send_message(call.message.chat.id, 'Ваши пары загружаются...')
        second_param = call.data.split('|')[1]
        username = second_param[5:]
        time.sleep(1)
        meme_match_dict = meme_matching(username, sheet)
        meme_match = list(meme_match_dict.keys())
    except BaseException:
        bot.send_message(call.message.chat.id, 'Перейдите в главное меню /start', )
    try:
        music_match = parsing(username)
    except StopIteration:
        bot.send_message(call.message.chat.id, 'Перейдите в главное меню /start', )
###########START MUSIC MENU##########################
    if second_param[0:5] == 'yemus':
        playlist_url = bot.send_message(call.message.chat.id, 'Поделись ссылкой на свой плейлист в spotify!')
        bot.register_next_step_handler(playlist_url, matching_for_music)
###########START MUSIC MATCH##########################
    if second_param[0:5] == 'stmus':
        I_mus = int( call.data.split('|')[0])
        markup_inline_ = types.InlineKeyboardMarkup()
        if I_mus < len(music_match):
            user_name = music_match[I_mus]
            I_mus = I_mus + 1
            music_match = parsing(user_name)
            random_songs = obtain_songs(user_name)
            song_str = 'Мои песни:'
            for song in random_songs:
                song_str = song_str +song + '\n'
                #print(song_str)
            url_photo = find_link_photo(user_name, sheet)
            like_butt_ = types.InlineKeyboardButton(text='Лайк!', url='https://t.me/' + user_name + '?start=+666')
            dislike_butt_ = types.InlineKeyboardButton(text='Дальше', callback_data = str(I_mus)  + '|'+'dlmus'+username)
            markup_inline_.add(dislike_butt_,like_butt_)
            bot.send_photo(call.message.chat.id, photo(url_photo))
            bot.send_message(call.message.chat.id, song_str, reply_markup = markup_inline_)
        else:
            I_mus = 0
            dislike_butt_ = types.InlineKeyboardButton(text='Начнем сначала?', callback_data = str(I_mus)  + '|'+'dlmus'+username,)
            markup_inline_.add(dislike_butt_)
            markup_inline_ = types.InlineKeyboardMarkup()
            start
            bot.send_message(call.message.chat.id, 'Пользователи закончились \n Для возврата в главное меню введи \start', reply_markup = markup_inline_)

    if second_param[0:5] == 'dlmus':
        I_mus = int( call.data.split('|')[0])
        if I_mus < len(music_match):
            user_name = music_match[I_mus]
            I_mus = I_mus + 1
            markup_inline_ = types.InlineKeyboardMarkup()
            music_match = parsing(user_name)
            random_songs = obtain_songs(user_name)
            song_str = 'Мои песни:'
            for song in random_songs:
                song_str = song_str +song + '\n'
                #print(song_str)
            url_photo = find_link_photo(user_name, sheet)
            like_butt_ = types.InlineKeyboardButton(text='Лайк!', url='https://t.me/' + user_name + '?start=+666')
            dislike_butt_ = types.InlineKeyboardButton(text='Дальше', callback_data = str(I_mus)+ '|' +'dlmus' + username)
            markup_inline_.add(dislike_butt_,like_butt_)
            bot.send_photo(call.message.chat.id, photo(url_photo))
            bot.send_message(call.message.chat.id, song_str, reply_markup = markup_inline_)
        else:
            I_mus = 0
            markup_inline_ = types.InlineKeyboardMarkup()
            dislike_butt_ = types.InlineKeyboardButton(text='Начнем сначала?', callback_data = str(I_mus)  + '|'+'dlmus'+username)
            markup_inline_.add(dislike_butt_)
            bot.send_message(call.message.chat.id, 'Пользователи закончились:( \n Для возврата в главное меню введи /start', reply_markup = markup_inline_)

    if second_param[0:5] == 'stmem':
        try:
            range_i = range(len(meme_match))
            for I_mem in range(len(meme_match)):
                user_name = meme_match[I_mem]
                I_mem = I_mem + 1
                markup_inline = types.InlineKeyboardMarkup()
                url_photo = meme_match_dict[user_name][1]
                like_butt = types.InlineKeyboardButton(text='Лайк!', url='https://t.me/' + user_name + '?start=+666')
                #dislike_butt = types.InlineKeyboardButton(text='Дальше', callback_data = str(I_mem)  + '|'+'dlmem'+username)
                markup_inline.add(like_butt)
                bot.send_photo(call.message.chat.id, photo(url_photo))
                name =  meme_match_dict[user_name][0]
                str_to_match = ''
                str_to_match = name + '\n' + 'Ваша совместимость: ' + str(round(meme_match_dict[user_name][4],0)) + '\n'+'Бюджет: ' + meme_match_dict[user_name][2] +'\n'+ 'Время сна: ' +  meme_match_dict[user_name][3]
                bot.send_message(call.message.chat.id, str_to_match, reply_markup=markup_inline)
            if I_mem == range_i:
                bot.send_message(call.message.chat.id, 'Пользователи закончились \n Для возврата в главное меню введи /start', reply_markup = markup_inline)
        except BaseException:
            bot.send_message(call.message.chat.id, 'Перейдите в главное меню /start', )


@bot.message_handler(content_types=['text'])
def matching_for_music(message):
    I_mus = 0
    username = message.chat.username
    playlist_url = message.text
    markup_inline = types.InlineKeyboardMarkup()
    try:
        put_playlist_to_db(username, playlist_url)
        start_butt = types.InlineKeyboardButton(text='начать!', callback_data =str(I_mus)  + '|''stmus'+username )
        markup_inline.add(start_butt)
        bot.send_message(message.chat.id, 'Хороший вкус!', reply_markup = markup_inline)
    except Exception as e :
        bot.send_message(message.chat.id, 'Неправильный адрес плэйлиста!\nВведите корректный адрес или выберите категорию "Юмор" в главном меню /start', reply_markup = markup_inline)

bot.polling(none_stop=True, interval=0)
