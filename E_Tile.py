import ents
import Globals
from E_Particle import Particle

class Tile(Particle):
    
    def tileSpriteData(self, offset):
        return Globals.TileSprites[self.tileoffset][offset]
    
    def applyparent(self, parent, translate):
        Particle.applyparent(self, parent, translate)
        if not translate: self.calculatePosition()
        i = ents.findCellIndexOfPos(self.position, parent.position, Globals.CellSize)
        parent.cellTiles[i][self.tileSpriteData(2)] = self
        self.vesselCell = i
        self.cellLayer = self.tileSpriteData(2)
            
    def setTileType(self, offset):
        self.tileoffset = offset
        self.setSprite(self.tileSpriteData(0))
        if self.tileSpriteData(2) == 0:
            ents.floorlayer_add(self)
        else:
            ents.walllayer_add(self)
        
    def getTileType(self):
        return self.tileoffset
    
    def initialize(self):
        self.tileoffset = 0
        Globals.ServerLastCreatedEnts.append(self)
    def getData(self):
        ans = Particle.getData(self)
        ans.append(self.tileoffset)
        ans[5] = ans[5] + "i"
        return ans
    def enterData(self, data, deref):
        Particle.enterData(self, data, deref)
        self.setTileType(int(data[7]))