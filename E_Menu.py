import pygame as pg
from pygamefunctions import load_image
import ents
import Globals
import vec

class Menu(pg.sprite.Sprite):
    
    def start(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("strawberry.png", -1)
        self.editsprite = "strawberry.png"
        self.rect.center = (9000,9000)
        self.viewmode = "Editor"
        
    def setPos(self, pos):
        self.rect.center = pos
        
    def setPosDimensionless(self, pos):
        self.rect.center = vec.mult_2(pos, (Globals.ScreenX, Globals.ScreenY))
        
    def setViewMode(self, mode):
        self.viewmode = mode
    
    def setSprite(self, image1):
        prev_center = self.rect.center
        prev_alpha = self.image.get_alpha()
        self.image, self.rect = load_image(image1, 0)
        self.editsprite = image1
        self.rect.center = prev_center
        self.image.set_alpha(prev_alpha)
        
    def update(self):
        if self.viewmode == Globals.ViewMode or self.viewmode == "all":
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)
        self.onTick()
        
    def remove(self):
        ents.removeUI(self)
        
    def onTick(self):
        pass
    
    def initialize(self):
        ents.menulayer1_add(self)