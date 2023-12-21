import pygame as pg
from pygamefunctions import load_image, MousePosToPosition
import ents
import Globals
import vec
from E_Menu import Menu

class MenuItem(Menu):
    def onTick(self):
        if self.viewmode == Globals.ViewMode:
            if self.itemActive == True and Globals.keys[0] == True:
                collision = False
                for v in ents.HotbarSprites:
                    if v.rect.collidepoint(pg.mouse.get_pos()) == True:
                        collision = True
                if collision == False:
                    self.use()
            if ents.getMenuHoldingObject() == self and Globals.keysHeld[0] == True:
                self.rect.center = pg.mouse.get_pos()
                v = ents.MenuPositions[self.inventoryIndex]
                if not vec.collision(v, 26, self.rect.center):
                    self.mouseHasLeftButton = True
                if self.held == 0:
                    self.held = 1
                    if self.itemActive == True:
                        self.mouseHasLeftButton = True
                    self.setActive(False)
            else:
                if self.held == 1:
                    self.held = 0
                    ents.setMenuHoldingObject(0)
                    i2 = 0
                    i = 0
                    while len(ents.MenuPositions) > i:
                        v = ents.MenuPositions[i]
                        if vec.collision(v, 26, self.rect.center):
                            if ents.getMenuContents()[i] != 0:
                                ents.addInventoryEntity(ents.getMenuContents()[i], self.inventoryIndex)
                                ents.getMenuContents()[i].setInventoryIndex(self.inventoryIndex)
                                if self.mouseHasLeftButton == False:
                                    self.setActive(True)
                            else:
                                ents.addInventoryEntity(0, self.inventoryIndex)
                            ents.addInventoryEntity(self, i)
                            self.inventoryIndex = i
                            i2 += 1
                        i = i + 1
                    if i2 == 0:
                        self.itemlink.exitInventory()
                        destination = MousePosToPosition(ents.getCreatureControlLink().parent)
                        realdestination = 0
                        if ents.getCreatureControlLink().parent == None:
                            realdestination = destination
                        else:
                            realdestination = vec.add_2(destination, ents.getCreatureControlLink().parent.posOffset)
                        throwspeed = vec.div(vec.sub_2(destination, self.itemlink.posOffset), Globals.Gravity)
                        throwmagnitude = vec.distance(throwspeed, (0,0))
                        if throwmagnitude > 25:
                            throwspeed = vec.div(throwspeed, throwmagnitude / 25)
                        if vec.largest(vec.sub_2(destination, self.itemlink.posOffset)) > 48 or ents.findBlocksAt(realdestination, ents.getCreatureControlLink().parent)[1] != None:
                            self.itemlink.throw(throwspeed)
                        else:
                            self.itemlink.setPosOffset(destination)
                        ents.addInventoryEntity(0, self.inventoryIndex)
                        self.remove()
                    self.rect.center = ents.MenuPositions[self.inventoryIndex]
                if Globals.keys[0] == True:
                    if vec.collision(self.rect.center, 26, pg.mouse.get_pos()):
                        ents.setMenuHoldingObject(self)
                        #self.held = 1
                self.mouseHasLeftButton = False
                
    def initialize(self):
        ents.menulayer1_add(self)
        self.held = 0
        self.inventoryIndex = -1
        self.internalIndex = -1
        self.insideEnt = 0
        self.image, self.rect = load_image("woodbox.png", 0)
        self.viewmode = "1st"
        self.itemlink = None
        self.mouseHasLeftButton = False
        self.itemActive = False
        self.crosshaircolor = 2
    def setInventoryIndex(self, index):
        self.inventoryIndex = index
        ents.addInventoryEntity(self, index)
        self.rect.center = ents.MenuPositions[index]
    def setActive(self, boolean):
        if boolean == True:
            self.crosshaircolor = self.itemlink.crosshaircolor
            ents.HotbarSprites[self.inventoryIndex].setSprite("smallmenuboxactive.png")
            self.itemActive = True
            if Globals.ActiveMenuItem != None: Globals.ActiveMenuItem.setActive(False)
            Globals.ActiveMenuItem = self
            self.itemActivate()
        else:
            ents.HotbarSprites[self.inventoryIndex].setSprite("smallmenubox.png")
            self.itemActive = False
            if Globals.ActiveMenuItem == self: Globals.ActiveMenuItem = None
    def use(self):
        self.itemlink.use(MousePosToPosition(ents.getCreatureControlLink().parent))
    def itemActivate(self):
        self.itemlink.itemActivate()