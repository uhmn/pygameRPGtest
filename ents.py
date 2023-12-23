import pygame as pg
import vec
import Globals

class Entss():
    
    def __init__(self):
        self.allsprites = pg.sprite.RenderPlain()
        self.menulayer1 = pg.sprite.RenderPlain()
        self.menulayer2 = pg.sprite.RenderPlain()
        self.menulayer3 = pg.sprite.RenderPlain()
        self.allvessels = []
        self.allbuttons = []
        self.allparticles = []
        self.AllParticleLayers = []
        self.p_entity_array = []
        #self.p_entity_list = []
        self.CreatureControlLink = 0
        self.MenuHoldingObject = 0
        self.MenuPositions = [(0,0),(0,0)]
        self.HotbarSprites = [None,None]
        self.MenuContents = [0,0]
        self.entCount = 0
        self.GameTick = 0
        
        self.floorlayer = None
        self.walllayer = None
        self.midlayer = None
        self.playerlayer = None
        self.playercosmeticlayer = None
        self.editlayer = None
        
        self.entTable = None
    def makeLayer(self):
        layer = pg.sprite.RenderPlain()
        self.AllParticleLayers.append(layer)
        return layer
    
self = Entss()
    
def initialize(entlist):
    self.floorlayer = self.makeLayer()
    self.walllayer = self.makeLayer()
    self.midlayer = self.makeLayer()
    self.playerlayer = self.makeLayer()
    self.playercosmeticlayer = self.makeLayer()
    self.editlayer = self.makeLayer()
    #for x in range (8000):
    #    self.entity_array.append(None)
    self.entTable = entlist
    
def getmenulayer1():
    return self.menulayer1

def getmenulayer2():
    return self.menulayer2

def getmenulayer3():
    return self.menulayer3

def getallparticles():
    return self.allparticles

def allparticles_append(inp):
    self.allparticles.append(inp)
def allvessels_append(inp):
    self.allvessels.append(inp)
def allbuttons_append(inp):
    self.allbuttons.append(inp)
    
def editlayer_add(inp):
    self.editlayer.add(inp)
def playerlayer_add(inp):
    self.playerlayer.add(inp)
def floorlayer_add(inp):
    self.floorlayer.add(inp)
def walllayer_add(inp):
    self.walllayer.add(inp)
def midlayer_add(inp):
    self.midlayer.add(inp)
def playercosmeticlayer_add(inp):
    self.playercosmeticlayer.add(inp)
def menulayer1_add(inp): self.menulayer1.add(inp)
def menulayer2_add(inp): self.menulayer2.add(inp)
def menulayer3_add(inp): self.menulayer3.add(inp)

def getCreatureControlLink():
    return self.CreatureControlLink

def setCreatureControlLink(inp):
    self.CreatureControlLink = inp
    
def getEntityTypes():
    return self.entTable(self)

def getCount():
    return self.entCount

def getTick():
    return self.GameTick

def getMenuHoldingObject():
    return self.MenuHoldingObject

def getMenuContents():
    return self.MenuContents

def incrementGameTick():
    self.GameTick += 1
    
def setGameTick(inp):
    self.GameTick = inp
    
def get_p_entity_array():
    return self.p_entity_array
    
def p_entity_array_add(ent):
    for x in range(len(self.p_entity_array)):
        if self.p_entity_array[x] == None:
            self.p_entity_array[x] = ent
            ent.pid = x+1
            return
    ent.pid = len(self.p_entity_array)+1
    self.p_entity_array.append(ent)
    
def create(etype):
    entitytypes = getEntityTypes()
    ent = entitytypes[etype]
    ent.classname = etype
    ent.start()
    ent.initialize()
    self.allsprites.add(ent)
    return ent

def update():
    self.allsprites.update()
    self.GameTick += 1
    
def draw(screen):
    for layer in self.AllParticleLayers:
        layer.draw(screen)
    self.menulayer1.draw(screen)
    self.menulayer2.draw(screen)
    self.menulayer3.draw(screen)
    
def findCellIndexOfPos(pos, vesselPos, cellSize):
    rowLength = (cellSize*2)+1
    Offset = vec.round2(vec.div(vec.sub_2(pos, vesselPos), 32))
    Xo = Offset[0]+cellSize
    Yo = Offset[1]+cellSize
    lis = Xo + (Yo * rowLength)
    return lis
def findEntAtCellIndex(cellIndex, vessel, layer):
    if len(vessel.cellTiles) < cellIndex:
        return None
    return vessel.cellTiles[cellIndex][layer]
    
def findBlocksAt(pos, vessel): #Enter a real position and it will return the floortile there.
    if vessel == None:
        for v in self.allvessels:
            blocks = findBlocksAt(pos, v)
            if blocks[0] != None or blocks[1] != None:
                return blocks
        return [None,None]
    else:
        cIndex = findCellIndexOfPos(pos, vessel.position, Globals.CellSize)
        ent1 = findEntAtCellIndex(cIndex, vessel, 0)
        ent2 = findEntAtCellIndex(cIndex, vessel, 1)
        return [ent1, ent2]
def adjacentBlocksAt(pos, vessel): #return if there are any wall blocks in the 3x3 square
    for i1 in range(3):
        for i2 in range(3):
            tile = self.findBlocksAt(vec.add_2(pos, (i1*32-32, i2*32-32)), vessel)
            if tile[1] != None: 
                return True
                
    return False
def setMenuHoldingObject(ent):
    self.MenuHoldingObject = ent
def addInventoryEntity(ent, index):
    self.MenuContents[index] = ent
def findMouseover():
    Globals.Mouseover = "Game"
    if Globals.ViewMode == "Editor":
        for v in self.allbuttons:
            if vec.collision(v.rect.center, 16, pg.mouse.get_pos()):
                Globals.Mouseover = "EditorPanel"

def SIDToEnt(SID):
    for sprite in self.allparticles:
        if sprite.getSID() == SID:
            return sprite
    return None
def EIDToEnt(EID):
    for sprite in self.allparticles:
        if sprite.getID() == EID:
            return sprite
    return None
def PIDToEnt(PID):
    return self.p_entity_array[PID-1]
    '''
    for sprite in self.allparticles:
        if sprite.getPID() == PID:
            return sprite
    return None
    '''
def clearSIDs():
    for sprite in self.allparticles:
        sprite.setSID(None)
def incrementEntCounter():
    self.entCount = self.entCount + 1
def getAllInTable(thetable):
    table = []
    for ent in thetable:
        if ent != None:
            table.append(ent.getData())
        else:
            table.append(None)
    return table
def deleteAll():
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
    self.p_entity_array = []
def remove(ent): #Don't use this to remove entities, use the entities' remove function instead.
    if ent in self.allsprites: self.allsprites.remove(ent)
    if ent in self.allparticles: self.allparticles.remove(ent)
    try:
        if ent in self.p_entity_array: self.p_entity_array[ent.pid-1] = None
    except:
        print(str(len(self.p_entity_array)) + " " + str(ent.pid-1))
    i = 0
    while i < len(self.AllParticleLayers):
        if ent in self.AllParticleLayers[i]: self.AllParticleLayers[i].remove(ent)
        i += 1
    if ent in self.allvessels: self.allvessels.remove(ent)
    if self.CreatureControlLink == ent: self.CreatureControlLink = 0
def removeUI(ent):
    if ent in self.allsprites: self.allsprites.remove(ent)
    if ent in self.menulayer1: self.menulayer1.remove(ent)
    if ent in self.menulayer2: self.menulayer2.remove(ent)
    if ent in self.menulayer3: self.menulayer3.remove(ent)
    
