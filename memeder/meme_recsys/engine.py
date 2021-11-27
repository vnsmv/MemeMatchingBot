import os
import random

import numpy as np

from memeder.paths import get_lib_root_path


def get_list_of_memes():
    files = os.listdir(get_lib_root_path() / 'Memes')
    random.shuffle(files)
    return tuple(files)


def meme_generator(list_memes=get_list_of_memes()):
    i = 0
    l = len(list_memes)
    while True:
        yield list_memes[i % l]
        i += 1


def get_random_meme():
    return np.random.permutation(os.listdir(get_lib_root_path() / 'Memes'))[0]


def recommend_meme(chat_id, database_src: str = 'database_csv'):
    # TODO: run recommendation engine here
    meme_id = get_random_meme()
    return meme_id
