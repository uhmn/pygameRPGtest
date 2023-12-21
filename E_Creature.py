import pygame as pg
from pygamefunctions import load_image
import ents
import Globals
import vec
from E_Particle import Particle
import sound
import random

class Creature(Particle):
    def WalkableCheck(self, pX, pY):
        ent = ents.findBlocksAt(vec.add_2(self.position, (pX,pY)), self.parent)
        if ent[1] == None or self.parent == None:
            return True
        else:
            return False
    def initialize(self):
        ents.playerlayer_add(self)
        self.moveCooldown = 0
        self.lastMoveCooldown = 0
        self.lastPosition = (0,0)
        self.image, self.rect = load_image("man2.png", -1)
        self.editsprite = "man2.png"
        self.stepcounter = 0
        self.stepcounter2 = 0
        self.stepsounds = [sound.load("FR1.wav"),sound.load("FR2.wav"),sound.load("FR3.wav"),sound.load("FL1.wav"),sound.load("FL2.wav"),sound.load("FL3.wav")]
        self.inventory = [None,None]
    def onTick(self):
        self.checkShipCollisions()
        if self.moveCooldown > 0:
            self.moveCooldown = self.moveCooldown - 1
        Xmove = 0
        Ymove = 0
        if ents.getCreatureControlLink() == self and Globals.ViewMode == "1st":
            if self.moveCooldown <= 0:
                self.stepcounter = self.stepcounter + 1
                if Globals.keysHeld[1]:
                    Ymove = Ymove - 1
                if Globals.keysHeld[2]:
                    Ymove = Ymove + 1
                if Globals.keysHeld[3]:
                    Xmove = Xmove - 1
                if Globals.keysHeld[4]:
                    Xmove = Xmove + 1
                movement = abs(Xmove) + abs(Ymove)
                if movement != 0:
                    if movement == 1:
                        self.moveCooldown = 10
                        self.lastMoveCooldown = 10
                        self.lastPosition = self.position
                    else:
                        self.moveCooldown = 14
                        self.lastMoveCooldown = 14
                        self.lastPosition = self.position
                        
                        if self.WalkableCheck(Xmove*32,Ymove*32) == False:
                            if self.WalkableCheck(Xmove*32,0) == False:
                                Xmove = 0
                                
                            elif self.WalkableCheck(0,Ymove*32) == False:
                                Ymove = 0
                            else:
                                Xmove = 0
                                Ymove = 0
                        
                    if self.WalkableCheck(Xmove*32,0) != False:
                        self.posOffset = vec.add_2(self.posOffset,(Xmove*32,0))
                        
                    if self.WalkableCheck(0,Ymove*32) != False:
                        self.posOffset = vec.add_2(self.posOffset,(0,Ymove*32))
                    if self.stepcounter > self.lastMoveCooldown/8:
                        if random.random() > (1/3):
                            if random.random() > (1/2):
                                self.stepsounds[0+self.stepcounter2*3].play()
                            else:
                                self.stepsounds[1+self.stepcounter2*3].play()
                        else:
                            self.stepsounds[2+self.stepcounter2*3].play()
                        self.stepcounter = 0
                        self.stepcounter2 = (self.stepcounter2 + 1) % 2
            windowSize = pg.display.get_window_size()
            self.position = (Globals.CamX + windowSize[0]/2,Globals.CamY + windowSize[1]/2)
    def remove(self):
        Particle.remove(self)
        for ent in self.inventory:
            ent.exitInventory()