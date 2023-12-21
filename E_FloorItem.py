import pygame as pg
from pygamefunctions import load_image
import ents
import Globals
import vec
from E_Particle import Particle
import sound
import random

class FloorItem(Particle):
    def initialize(self):
        ents.midlayer_add(self)
        self.inside = None
        self.uiItem = None
        self.invIndex = 0
        self.onFloor = True
        self.velocity = (0,0)
        self.height = 0.5
        self.rotation = 0
        self.crosshaircolor = 1
        self.hitsound = sound.load("tink.wav")
    def pressed(self):
        space = None
        i = 0
        while i < len(ents.MenuContents):
            if ents.MenuContents[i] == 0: space = i
            i += 1
        if space != None:
            if vec.largest(vec.sub_2(ents.getCreatureControlLink().position, self.position)) < 48:
                self.putInside(ents.getCreatureControlLink(), space)
    poopbool = True
    def onTick(self):
        if Globals.ViewMode == "1st":
            if vec.collision(self.rect.center, 8, pg.mouse.get_pos()):
                if Globals.keys[0] == True:
                    Globals.keys[0] = False
                    self.pressed()
        if not self.onFloor:
            '''
            self.velocity = (0,0)
            self.setPosOffset(MousePosToVesselPos(self.parent.position[0], self.parent.position[1]))
            self.calculatePosition()
            tiles = ents.findBlocksAt(vec.add_2(self.position, self.velocity), self.parent)
            if tiles[1] != None:
                self.setSprite("redtarget.png")
            else:
                self.setSprite("yellowtarget.png")
            '''
            self.spin()
            
            #tiles = [None,None]
            tiles = ents.findBlocksAt(vec.add_2(self.position, self.velocity), self.parent)
            if tiles[1] != None:
                self.onWallHit(self.velocity)
                position1 = vec.mult(vec.round2(vec.div(self.posOffset, 32)), 32)
                position2 = tiles[1].posOffset
                direction = vec.round2(vec.div(vec.sub_2(position1, position2), 32))
                hitspeed = vec.distance(self.velocity, (0,0))
                if hitspeed > 3:
                    self.hitsound.set_volume(hitspeed / 100)
                    self.hitsound.play()
                adjacentside = 0
                if abs(direction[0]) + abs(direction[1]) > 1:
                    hitTilePos = tiles[1].position
                    quantized_vel = vec.mult(vec.div_2(self.velocity, vec.abs2(self.velocity)), -32)
                    tiles = ents.findBlocksAt(vec.add_2(hitTilePos, (quantized_vel[0],0)), self.parent)
                    if(tiles[1] == None):
                        adjacentside += 1
                    tiles = ents.findBlocksAt(vec.add_2(hitTilePos, (0,quantized_vel[1])), self.parent)
                    if(tiles[1] == None):
                        adjacentside -= 1
                if abs(direction[0]) + abs(direction[1]) > 1 and adjacentside == 0:
                    self.velocity = vec.mult(self.velocity, -0.05)
                elif (direction[0] != 0 and adjacentside == 0) or adjacentside == 1: 
                    self.velocity = (self.velocity[0]*(-0.35),self.velocity[1])
                elif (direction[1] != 0 and adjacentside == 0) or adjacentside == -1:
                    self.velocity = (self.velocity[0],self.velocity[1]*(-0.35))
            self.posOffset = vec.add_2(self.posOffset, self.velocity)
            if tiles[0] == None and tiles[1] == None and self.parent != None:
                self.unParent()
            self.height = self.height - Globals.Gravity/200
            if self.height < 0:
                self.setOnFloor(True)
        else:
            self.checkShipCollisions()
            if self.parent == None:
                self.remove()
            
    def putInside(self, ent, index):
        self.inside = ent
        self.setPos(ent.calculatePosition())
        self.setParent(ent)
        self.posOffset = (0,0)
        self.velocity = (0,0)
        self.setOnFloor(True)
        self.rotation = 0
        if ents.getCreatureControlLink() == ent:
            self.uiItem = ents.create("MenuItem")
            self.uiItem.setSprite(self.editsprite)
            self.uiItem.setInventoryIndex(index)
            self.uiItem.itemlink = self
            self.invIndex = index
        self.image.set_alpha(0)
    def isInside(self):
        if self.inside == None:
            return False
        else:
            return True
    def exitInventory(self):
        self.setParent(self.inside.parent)
        self.setPosOffset(self.inside.posOffset)
        self.inside = None
        self.uiItem.remove()
        self.uiItem = None
        self.image.set_alpha(255)
        self.rotation = 0
        self.spinSpeed = 0
        self.image = self.original
    def getData(self):
        ans = Particle.getData(self)
        inside = self.inside
        if inside == None: 
            inside = 0
        else:
            inside = self.inside.id
        ans.append(inside)
        ans.append(self.invIndex)
        ans[5] = ans[5] + "1" + "I"
        return ans
    def enterData(self, data):
        Particle.enterData(self, data)
        inside = ents.SIDToEnt(data[7])
        if inside == 0 or inside == None:
            self.inside = None
        else:
            self.putInside(inside, int(data[8]))
    def setOnFloor(self, boolean):
        self.onFloor = boolean
        if boolean == True:
            self.velocity = (0,0)
            self.height = 0
            self.posOffset = vec.round2(self.posOffset)
    def getAbsVelocity(self):
        return vec.distance(self.velocity, (0,0))
    def throw(self, vel):
        self.height = 0.5
        self.velocity = vel
        self.setOnFloor(False)
        self.spinSpeed = random.randint(-16, 16)
    def setSprite(self, image1):
        self.original = Particle.setSprite(self, image1)
    def spin(self):
        center = self.rect.center
        self.rotation = self.rotation + self.spinSpeed
        self.rotation = self.rotation % 360
        rotate = pg.transform.rotate
        self.image = rotate(self.original, self.rotation)
        self.rect = self.image.get_rect(center=center)
    def use(self, target):
        pass
    def onWallHit(self, velocity):
        pass
    def itemActivate(self):
        pass