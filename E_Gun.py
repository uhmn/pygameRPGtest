import pygame as pg
from pygamefunctions import load_image
import ents
import Globals
import vec
from E_FloorItem import FloorItem
import sound

class Gun(FloorItem):
    def initialize(self):
        FloorItem.initialize(self)
        self.crosshaircolor = 2
        self.setSprite("gun.png")
        self.fire_sound = sound.load("pistol_fire.wav")
        self.click_sound = sound.load("click.wav")
        self.equip_sound = sound.load("gun_equip.wav")
        self.bullets = 7
    def use(self, target):
        if self.bullets > 0:
            bullet = ents.create("FloorItem")
            bullet.setSprite("shell.png")
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
            offset = vec.div(offset, (magnitude / 40))
            bullet.throw(offset)
            bullet.height = 1
            self.fire_sound.play()
            self.bullets -= 1
        else:
            self.click_sound.play()
    def itemActivate(self):
        self.equip_sound.play()