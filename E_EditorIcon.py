import pygame as pg
from pygamefunctions import load_image
import ents
import Globals
import vec
from E_Menu import Menu

class EditorIcon(Menu):
    
    def initialize(self):
        ents.menulayer2_add(self)
        ents.allbuttons_append(self)
        self.viewmode = "Editor"
        self.editsprite = "strawberry"
        
    def setSprite(self, image1):
        self.image, self.rect = load_image(image1, -1)
        self.editsprite = image1
    def setproperties(self, offset):
        self.tileoffset = offset
        self.enttype = Globals.TileSprites[offset][1]
        self.setSprite(Globals.TileSprites[offset][0])
        
    def onTick(self):
        if self.viewmode == "Editor":
            if vec.collision(self.rect.center, 16, pg.mouse.get_pos()):
                if Globals.keys[0] == True:
                    Globals.EditorType = self.editsprite
                    Globals.EditorEntType = self.enttype
                    Globals.EditorTileOffset = self.tileoffset
                    Globals.EditBrush.setSprite(Globals.EditorType)