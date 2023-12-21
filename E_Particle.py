import pygame as pg
from pygamefunctions import load_image
import ents
import Globals
import vec
import net

class Particle(pg.sprite.Sprite):
    
    NetworkingMethods = {}
    
    def start(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("strawberry.png", 0)
        self.editsprite = "strawberry.png"
        self.rect.center = (9000,9000)
        self.posOffset = (0, 0)
        self.parent = None
        ents.incrementEntCounter()
        self.id = ents.getCount()
        ents.allparticles_append(self)
        Globals.LastCreatedEnts.append(self)
        self.childs = []
        self.position = (0,0) 
        self.lastVessel = None
        self.vesselCell = None
        self.cellLayer = None
        self.sid = None
        
    def calculatePosition(self):
        if self.parent != 0 and not self.parent == None:
            self.position = vec.add_2(self.posOffset, self.parent.calculatePosition())
            return self.position
        else:
            self.position = self.posOffset
            return self.position
        
    def removeCellListReference(self):
        if not self.cellLayer == None:
            if self.cellLayer > 1:
                self.parent.cellTiles[self.vesselCell].pop(self.cellLayer)
            else:
                self.parent.cellTiles[self.vesselCell][self.cellLayer] = None
            
    
    def calculateVesselCell(self):
        if self.parent != None and self.classname != "Tile":
            if self.parent.classname == "Vessel": 
                if self.lastVessel != None:
                    self.removeCellListReference()
                self.vesselCell = ents.findCellIndexOfPos(self.position, self.parent.position, Globals.CellSize)
                self.parent.cellTiles[self.vesselCell].append(self)
            else: 
                if self.lastVessel != None:
                    self.removeCellListReference()
                self.vesselCell = self.parent.vesselCell
        
    def update(self):
        self.calculatePosition()
        self.calculateVesselCell()
        self.onTick()
        self.rect.center = vec.sub_2(self.position, (Globals.CamX, Globals.CamY))
        self.calculatePosition()
        
    def fixPos(self):
        self.calculatePosition()
        self.rect.center = vec.sub_2(self.position, (Globals.CamX, Globals.CamY))
        self.calculatePosition()
        
    def setPos(self, pos):
        self.posOffset = pos
        self.calculatePosition()
        self.rect.center = vec.sub_2(self.position, (Globals.CamX, Globals.CamY))
        self.calculateVesselCell()
        
    def setPosOffset(self, pos):
        self.posOffset = pos
        self.fixPos()
        
    def applyparent(self, parent):
        self.parent = parent
        parent.childs.append(self)
        self.posOffset = vec.round2(vec.sub_2(self.position, self.parent.position))
    def setParent(self, parent):
        if parent != None:
            self.applyparent(parent)
        else:
            self.parent = None
    def unParent(self):
        if not self.parent == None:
            newparent = self.parent.parent
            self.setParent(newparent)
            self.calculateVesselCell()
        self.posOffset = self.position
        
    def setSprite(self, image1):
        prev_center = self.rect.center
        prev_alpha = self.image.get_alpha()
        self.image, self.rect = load_image(image1, 0)
        self.editsprite = image1
        self.rect.center = prev_center
        self.image.set_alpha(prev_alpha)
        return self.image
        
    def getID(self):
        return self.id
    
    def setSID(self, sid):
        self.sid = sid
    
    def getSID(self):
        return self.sid
        
    def getData(self):
        if self.parent != None:
            parent = self.parent.getID()
        else:
            parent = 0
        return ([self.classname, 
                 self.id,
                 self.editsprite, 
                 self.posOffset[0], 
                 self.posOffset[1], 
                 "S1SIIS1",
                 parent,])
        
    def enterData(self, data):
        self.classname = data[0]
        self.setSprite(data[2])
        self.posOffset = (float(data[3]), float(data[4]))
        self.calculatePosition()
        
    def remove(self):
        net.NetAction("entmethod", self.sid, "remove")
        self.removef()
    def removef(self):
        ents.remove(self)
        for ent in self.childs:
            ent.unParent()
        if self.parent != None:
            if self in self.parent.childs:
                self.parent.childs.remove(self)
                if self.parent.classname == "Vessel": self.removeCellListReference()
                
    def remove_client(self):
        self.removef()
    NetworkingMethods.update({"remove" : remove_client})
    
    def checkShipCollisions(self):
        if self.parent == None:
            block = ents.findBlocksAt(self.position, None)[0]
            if self.parent == None and block != None:
                self.setParent(block.parent)
                if self.classname == "Creature": self.setPosOffset(block.posOffset)
        else:
            if self.parent.classname == "Vessel" and ents.findBlocksAt(self.position, self.parent)[0] == None:
                self.unParent()
                
    def getVessel(self):
        if self.classname == "Vessel":
            return self
        else:
            if self.parent == None:
                return None
            else:
                return self.parent.getVessel()
    def onTick(self):
        #if Globals.debug == self.sid: self.image.set_alpha(64)
        #else: self.image.set_alpha(255)
        pass
    
    def initialize(self):
        ents.floorlayer.add(self)