import pygame as pg
from pygamefunctions import load_image
import ents
import Globals
import vec
import E_Particle

class Vessel(E_Particle.Particle):
    def initialize(self):
        ents.allvessels_append(self)
        self.cellTiles = []
        self.cellListLength = (Globals.CellSize*Globals.CellSize*5)
        i = 0
        while self.cellListLength > i: #2601-25
            self.cellTiles.append([None,None])
            i = i + 1
        self.velocity = (-0.1, -0.1)
    def onTick(self):
        self.posOffset = vec.add_2(self.posOffset, self.velocity)
    def enterData(self, data): #will break if deleted
        pass