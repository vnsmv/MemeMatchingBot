import os
import random

import numpy as np

from memeder.paths import get_lib_root_path

# from telethon import TelegramClient, events, sync
# #stole memes from Fast Food Memes bot
#
# api_id = 15806656
# api_hash = 'f5fc3ffced16b257c1b36aace17014b9'
#
# client = TelegramClient('session_name', api_id, api_hash)
# client.start()

def meme_generator():
    messages = client.get_messages('ffmemesbot')
    msg = messages[0]
    meme_id = msg.photo.id
    messages[0].click()
    return meme_id

def get_list_of_memes():
    files = os.listdir(get_lib_root_path() / 'Memes')
    random.shuffle(files)
    return tuple(files)


# def meme_generator(list_memes=get_list_of_memes()):
#     i = 0
#     l = len(list_memes)
#     while True:
#         yield list_memes[i % l]
#         i += 1


def get_random_meme():
    return np.random.permutation(os.listdir(get_lib_root_path() / 'Memes'))[0]


def recommend_meme(chat_id, database_src: str = 'database_csv'):
    # TODO: run recommendation engine here
    meme_id = get_random_meme()
    return meme_id
