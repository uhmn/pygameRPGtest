import pygame as pg
import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

def _load(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound

allsounds = {}

def load(name):
    for soundname in allsounds:
        if soundname == name:
            return allsounds[soundname]
    newsound = _load(name)
    allsounds.update({name:newsound})
    return newsound
