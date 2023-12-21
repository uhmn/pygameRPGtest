import pygame as pg
from pygamefunctions import load_image
import ents
import Globals
import vec
import saveloadfunctions as slf

class SaveButton(slf.SaveLoadButton):
    def pressed(self):
        slf.SaveGame()