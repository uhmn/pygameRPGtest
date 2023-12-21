import pygame as pg
import vec
import Globals

"""
import Particle
import EditorEnt
import Vessel
import Creature
import Menu
import MenuB
import MenuItem
import MousePointer
import EditorIcon
import SaveButton
import LoadButton
import StartButton
import Tile
import DeleteBrush
import FloorItem
import Gun
import WaterGun
import Thruster
"""

class Ents():
    
    """
    def getEntityTypes(self):
        return ({
          "Particle"        :    Particle(),
          "EditorEnt"       :    EditorEnt(),
          "Vessel"          :    Vessel(),
          "Creature"        :    Creature(),
          "Menu"            :    Menu(),
          "MenuB"           :    MenuB(),
          "MenuItem"        :    MenuItem(),
          "MousePointer"    :    MousePointer(),
          "EditorIcon"      :    EditorIcon(),
          "SaveButton"      :    SaveButton(),
          "LoadButton"      :    LoadButton(),
          "StartButton"     :    StartButton(),
          "Tile"            :    Tile(),
          "DeleteBrush"     :    DeleteBrush(),
          "FloorItem"       :    FloorItem(),
          "Gun"             :    Gun(),
          "WaterGun"        :    WaterGun(),
          "Thruster"        :    Thruster()
        })
    """

    
    def __init__(self):
        self.allsprites = pg.sprite.RenderPlain()
        self.menulayer1 = pg.sprite.RenderPlain()
        self.menulayer2 = pg.sprite.RenderPlain()
        self.menulayer3 = pg.sprite.RenderPlain()
        self.allvessels = []
        self.allbuttons = []
        self.allparticles = []
        self.AllParticleLayers = []
        self.CreatureControlLink = 0
        self.MenuHoldingObject = 0
        self.MenuPositions = [(0,0),(0,0)]
        self.HotbarSprites = [None,None]
        self.MenuContents = [0,0]
        self.EditorType = "strawberry.png"
        self.EditorTileOffset = 0
        self.EditorEntType = "Tile"
        self.EditBrush = None
        self.entCount = 0
        self.GameTick = 0
        def makeLayer():
            layer = pg.sprite.RenderPlain()
            self.AllParticleLayers.append(layer)
            return layer
        self.floorlayer = makeLayer()
        self.walllayer = makeLayer()
        self.midlayer = makeLayer()
        self.playerlayer = makeLayer()
        self.playercosmeticlayer = makeLayer()
        self.editlayer = makeLayer()
        self.entTable = None
        
    def getEntityTypes(self):
        return self.entTable(self)
        
    def create(self, etype):
        entitytypes = self.getEntityTypes()
        ent = entitytypes[etype]
        ent.classname = etype
        ent.start()
        ent.initialize()
        self.allsprites.add(ent)
        return ent
    
    def update(self):
        self.allsprites.update()
        self.GameTick += 1
        
    def draw(self, screen):
        for layer in self.AllParticleLayers:
            layer.draw(screen)
        self.menulayer1.draw(screen)
        self.menulayer2.draw(screen)
        self.menulayer3.draw(screen)
        
    def findCellIndexOfPos(self, pos, vesselPos, cellSize):
        rowLength = (cellSize*2)+1
        Offset = vec.round2(vec.div(vec.sub_2(pos, vesselPos), 32))
        Xo = Offset[0]+cellSize
        Yo = Offset[1]+cellSize
        lis = Xo + (Yo * rowLength)
        return lis
    def findEntAtCellIndex(self, cellIndex, vessel, layer):
        if len(vessel.cellTiles) < cellIndex:
            return None
        return vessel.cellTiles[cellIndex][layer]
        
    def findBlocksAt(self, pos, vessel): #Enter a real position and it will return the floortile there.
        if vessel == None:
            for v in self.allvessels:
                blocks = self.findBlocksAt(pos, v)
                if blocks[0] != None or blocks[1] != None:
                    return blocks
            return [None,None]
        else:
            cIndex = self.findCellIndexOfPos(pos, vessel.position, Globals.CellSize)
            ent1 = self.findEntAtCellIndex(cIndex, vessel, 0)
            ent2 = self.findEntAtCellIndex(cIndex, vessel, 1)
            return [ent1, ent2]
    def adjacentBlocksAt(self, pos, vessel): #return if there are any wall blocks in the 3x3 square
        for i1 in range(3):
            for i2 in range(3):
                tile = self.findBlocksAt(vec.add_2(pos, (i1*32-32, i2*32-32)), vessel)
                if tile[1] != None: 
                    print("a")
                    return True
                    
        return False
    def setMenuHoldingObject(self, ent):
        self.MenuHoldingObject = ent
    def addInventoryEntity(self, ent, index):
        self.MenuContents[index] = ent
    def findMouseover(self):
        global Mouseover
        Mouseover = "Game"
        if Globals.ViewMode == "Editor":
            for v in self.allbuttons:
                if vec.collision(v.rect.center, 16, pg.mouse.get_pos()):
                    Mouseover = "EditorPanel"
    
    def SIDToEnt(self, SID):
        for sprite in self.allparticles:
            if sprite.getSID() == SID:
                return sprite
        return None
    def incrementEntCounter(self):
        self.entCount = self.entCount + 1
    def getAllTable(self):
        table = []
        for ent in self.allparticles:
            table.append(ent.getData())
        return table
    def deleteAll(self):
        self.allsprites.remove(self.allparticles)
        i = 0
        while i < len(self.AllParticleLayers):
            self.AllParticleLayers[i].empty()
            i += 1
        if self.MenuContents[0] != 0:
            self.MenuContents[0].remove()
        if self.MenuContents[1] != 0:
            self.MenuContents[1].remove()
        self.MenuHoldingObject = 0
        self.MenuContents = [0,0]
        self.allvessels = []
        self.CreatureControlLink = 0
        self.entCount = 0
        for ent in self.allparticles:
            del ent
        self.allparticles = []
    def remove(self, ent): #Don't use this to remove entities, use the entities' remove function instead.
        if ent in self.allsprites: self.allsprites.remove(ent)
        if ent in self.allparticles: self.allparticles.remove(ent)
        i = 0
        while i < len(self.AllParticleLayers):
            if ent in self.AllParticleLayers[i]: self.AllParticleLayers[i].remove(ent)
            i += 1
        if ent in self.allvessels: self.allvessels.remove(ent)
        if self.CreatureControlLink == ent: self.CreatureControlLink = 0
    def removeUI(self, ent):
        if ent in self.allsprites: self.allsprites.remove(ent)
        if ent in self.menulayer1: self.menulayer1.remove(ent)
        if ent in self.menulayer2: self.menulayer2.remove(ent)
        if ent in self.menulayer3: self.menulayer3.remove(ent)
        