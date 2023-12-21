import pygame as pg
from pygamefunctions import load_image
import ents
import Globals
import vec
from E_Menu import Menu

class MousePointer(Menu):
    
    def initialize(self):
        ents.getmenulayer3().add(self)
        self.setSprite("greenpointer.png")
        self.viewmode = "all"
        
    def onTick(self):
        self.rect.center = pg.mouse.get_pos()
        if Globals.ActiveMenuItem != None and Globals.ViewMode == "1st":
            if Globals.ActiveMenuItem.crosshaircolor == 1 and self.editsprite != "yellowtarget.png":
                self.setSprite("yellowtarget.png")
            elif Globals.ActiveMenuItem.crosshaircolor == 2 and self.editsprite != "redtarget.png":
                self.setSprite("redtarget.png")
        else:
            if self.editsprite != "greenpointer.png":
                self.setSprite("greenpointer.png")