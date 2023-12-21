import pygame as pg
from pygamefunctions import load_image
import ents
import Globals
import vec
from E_Menu import Menu

class MenuB(Menu):
    
    def initialize(self):
        ents.menulayer2_add(self)