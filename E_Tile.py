import pygame as pg
from pygamefunctions import load_image
import ents
import Globals
import vec
from E_Particle import Particle

class Tile(Particle):
    
    def applyparent(self, parent):
        Particle.applyparent(self, parent)
        i = ents.findCellIndexOfPos(self.position, parent.position, Globals.CellSize)
        parent.cellTiles[i][Globals.TileSprites[self.tileoffset][2]] = self
        self.vesselCell = i
        self.cellLayer = Globals.TileSprites[self.tileoffset][2]
            
    def setTileType(self, offset):
        self.tileoffset = offset
        self.setSprite(Globals.TileSprites[offset][0])
        if Globals.TileSprites[offset][2] == 0:
            ents.floorlayer_add(self)
        else:
            ents.walllayer_add(self)
        
    def getTileType(self):
        return self.tileoffset
    
    def initialize(self):
        self.tileoffset = 0
    def getData(self):
        ans = Particle.getData(self)
        ans.append(self.tileoffset)
        ans[5] = ans[5] + "i"
        return ans
    def enterData(self, data):
        Particle.enterData(self, data)
        self.setTileType(int(data[7]))