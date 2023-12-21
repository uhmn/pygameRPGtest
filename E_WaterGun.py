import pygame as pg
from pygamefunctions import load_image
import ents
import Globals
import vec
from E_Gun import Gun
import sound
from E_FloorItem import FloorItem

class WaterGun(Gun):
    def initialize(self):
        FloorItem.initialize(self)
        self.crosshaircolor = 2
        self.setSprite("watergun.png")
        self.fire_sound = sound.load("flowing.mp3")
        self.click_sound = sound.load("bubbles.wav")
        self.equip_sound = sound.load("bubbles.wav")
        self.bullets = 70
    def use(self, target):
        if self.bullets > 0:
            bullet = ents.create("FloorItem")
            bullet.setSprite("water.png")
            bullet.setParent(self.getVessel())
            posoffset = (0,0)
            if self.isInside: 
                bullet.setPosOffset(self.parent.posOffset)
                posoffset = (self.parent.posOffset)
            else:
                bullet.setPosOffset(self.posOffset)
                posoffset = (self.posOffset)
            offset = vec.sub_2(target, posoffset)
            magnitude = vec.distance(offset, (0,0))
            offset = vec.div(offset, (magnitude / 20))
            bullet.throw(offset)
            bullet.height = 1
            self.fire_sound.play()
            self.bullets -= 1
        else:
            self.click_sound.play()