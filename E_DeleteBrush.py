import pygame as pg
from pygamefunctions import load_image
import ents
import Globals
import vec
import entity_list as e

class DeleteBrush(e.Tile):
    
    def onTick(self):
        ent = ents.findBlocksAt(self.position, self.parent)[1]
        if ent != None: ent.remove()
        self.remove()