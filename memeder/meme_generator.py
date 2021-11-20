import os
import random

from memeder.paths import get_lib_root_path


def listofmemes():
    files = os.listdir(get_lib_root_path() / 'Memes')
    random.shuffle(files)
    return files


def GeneratorMeme(list_memes, k):
    i = 0
    while i < k:
        yield list_memes[i]
        i = i + 1
