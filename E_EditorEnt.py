import pygame as pg
from pygamefunctions import load_image, MousePosToGridPos
import ents
import Globals
import vec
import E_Particle
import sound

class EditorEnt(E_Particle.Particle):
    def initialize(self): 
        ents.editlayer_add(self)
        self.image.set_alpha(128)
        self.whiff_sound = sound.load("Crank.wav")
        Globals.EditBrush = self
    def onTick(self):
        if Globals.ViewMode == "Editor" and Globals.Mouseover == "Game" and ents.getTick() > 0:
            self.image.set_alpha(128)
            self.posOffset = MousePosToGridPos(self.parent.position[0], self.parent.position[1])
            if Globals.keysHeld[0] == True:
                entlayer = Globals.TileSprites[Globals.EditorTileOffset][2]
                previous = ents.findBlocksAt(self.position, self.parent)
                
                lastsprite = None
                if previous[entlayer] != None: lastsprite = previous[entlayer].editsprite
                
                if lastsprite != Globals.EditorType or (entlayer == 0 and previous[1] != None):
                    if previous[entlayer] != None: previous[entlayer].remove()
                    if entlayer == 0:
                        if previous[1] != None: previous[1].remove()
                    if Globals.EditorEntType != "DeleteBrush": self.whiff_sound.play()
                    placed = ents.create(Globals.EditorEntType)
                    placed.setTileType(Globals.EditorTileOffset)
                    placed.setSprite(Globals.EditorType)
                    placed.setPos(self.position)
                    placed.setParent(self.parent)
        else:
            self.image.set_alpha(0)