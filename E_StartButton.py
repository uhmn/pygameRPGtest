import pygame as pg
from pygamefunctions import load_image
import ents
import Globals
import vec
from E_Menu import Menu

class StartButton(Menu):
    def initialize(self):
        ents.getmenulayer1().add(self)
        self.pressed = False
        self.viewmode = "all"
    def isPressed(self):
        return self.pressed
    def onTick(self):
        if Globals.keys[0] == True:
            if (self.rect.collidepoint(pg.mouse.get_pos())):
                self.pressed = True