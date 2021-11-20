import os
import random

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


def recommend_meme(meme_generator, user_id):
    return next(meme_generator)
