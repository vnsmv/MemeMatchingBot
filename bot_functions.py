import os
import random

def listofmemes():
    files = os.listdir('./Memes/')
    random.shuffle(files)
    return files

def GeneratorMeme(list_memes, k):
    i = 0
    while i < k:
        yield list_memes[i]
        i = i + 1
