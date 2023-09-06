import os
import pygame as pg
import vec
import random
import sound

from PodSixNet.Connection import ConnectionListener, connection
import PodSixNet.Channel
import PodSixNet.Server
 
if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        #if colorkey == -1:
        #    colorkey = image.get_at((0, 0))
        colorkey = pg.Color(0, 0, 255, 255)
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()



Connecteds = []
TileSprites = [("strawberry.png","Tile",0), 
               ("wall.png","Tile",1), 
               ("wall2.png","Tile",1), 
               ("wall3.png","Tile",1),
               ("grate.png","Tile",0), 
               ("girderwallLR.png","Tile",1), 
               ("girderwallUD.png","Tile",1), 
               ("girderwallLRUD.png","Tile",1), 
               ("deletebrush.png","DeleteBrush",0),
               ("thrusterL.png","Thruster",1),
               ("thrusterR.png","Thruster",1),
               ("thrusterU.png","Thruster",1),
               ("thrusterD.png","Thruster",1)]
keys = [False,False,False,False,False,False]
keysHeld = [False,False,False,False,False,False]
keysPressed = 0
CamX = 0
CamY = 0
ViewMode = "Editor"
ScreenX = 1080
ScreenY = 480
Mouseover = "Game"
Gravity = 9.8
ActiveMenuItem = None
GameServer = False
    
def InputEvents(keys, CreatureControlLink):
    going = True
    global CamX, CamY, keysPressed, ViewMode
    for v in keys:
        keys[v] = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            going = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                going = False
            elif event.key == pg.K_UP:
                keysPressed = keysPressed + 1
                keys[1] = True
                keysHeld[1] = True
            elif event.key == pg.K_DOWN:
                keysPressed = keysPressed + 1
                keys[2] = True
                keysHeld[2] = True
            elif event.key == pg.K_LEFT:
                keysPressed = keysPressed + 1
                keys[3] = True
                keysHeld[3] = True
            elif event.key == pg.K_RIGHT:
                keysPressed = keysPressed + 1
                keys[4] = True
                keysHeld[4] = True
            elif event.key == pg.K_RETURN:
                keys[5] = True
                if ViewMode == "Editor":
                    ViewMode = "1st"
                else:
                    ViewMode = "Editor"
        elif event.type == pg.MOUSEBUTTONDOWN:
            keys[0] = True
            keysHeld[0] = True
        elif event.type == pg.MOUSEBUTTONUP:
            keysHeld[0] = False
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                keysHeld[1] = False
                keysPressed = keysPressed - 1
            elif event.key == pg.K_DOWN:
                keysHeld[2] = False
                keysPressed = keysPressed - 1
            elif event.key == pg.K_LEFT:
                keysHeld[3] = False
                keysPressed = keysPressed - 1
            elif event.key == pg.K_RIGHT:
                keysHeld[4] = False
                keysPressed = keysPressed - 1
    if keysPressed != 0:
        if ViewMode == "Editor":
            if keysHeld[1] == True:
                CamY = CamY - (16/(keysPressed/(keysPressed/1.5)))
        
            if keysHeld[2] == True:
                CamY = CamY + (16/(keysPressed/(keysPressed/1.5)))
        
            if keysHeld[3] == True:
                CamX = CamX - (16/(keysPressed/(keysPressed/1.5)))
        
            if keysHeld[4] == True:
                CamX = CamX + (16/(keysPressed/(keysPressed/1.5)))
    if ViewMode == "1st" and CreatureControlLink != 0:
        windowSize = pg.display.get_window_size()
        if CreatureControlLink.moveCooldown > 0:
            slider = CreatureControlLink.moveCooldown / CreatureControlLink.lastMoveCooldown
            CamX = slider*(CreatureControlLink.lastPosition[0]-windowSize[0]/2)+(1-slider)*(CreatureControlLink.position[0]-windowSize[0]/2)
            CamY = slider*(CreatureControlLink.lastPosition[1]-windowSize[1]/2)+(1-slider)*(CreatureControlLink.position[1]-windowSize[1]/2)
        else:
            CamX = CreatureControlLink.position[0]-windowSize[0]/2
            CamY = CreatureControlLink.position[1]-windowSize[1]/2
    return going

def MousePosToGridPos(parentX, parentY):
    return vec.mult(vec.round2(vec.div(vec.sub_2(vec.add_2(pg.mouse.get_pos(), (CamX,CamY) ), (parentX,parentY)), 32)), 32)
def MousePosToVesselPos(parentX, parentY):
    return vec.round2(vec.sub_2(vec.add_2(pg.mouse.get_pos(), (CamX,CamY) ), (parentX,parentY)))
def MousePosToPosition(parent):
    if parent == None:
        return MousePosToVesselPos(0, 0)
    else:
        return MousePosToVesselPos(parent.position[0], parent.position[1])


class Ents():
    
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
        
    def getEntityTypes(self):
        return ({
          "Particle": Particle(),
          "EditorEnt": EditorEnt(),
          "Vessel": Vessel(),
          "Creature": Creature(),
          "Menu": Menu(),
          "MenuB": MenuB(),
          "MenuItem": MenuItem(),
          "MousePointer": MousePointer(),
          "EditorIcon": EditorIcon(),
          "SaveButton": SaveButton(),
          "LoadButton": LoadButton(),
          "StartButton": StartButton(),
          "Tile": Tile(),
          "DeleteBrush": DeleteBrush(),
          "FloorItem": FloorItem(),
          "Gun": Gun(),
          "Thruster": Thruster()
        })
        
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
            cIndex = self.findCellIndexOfPos(pos, vessel.position, 25)
            ent1 = self.findEntAtCellIndex(cIndex, vessel, 0)
            ent2 = self.findEntAtCellIndex(cIndex, vessel, 1)
            return [ent1, ent2]
    def setMenuHoldingObject(self, ent):
        self.MenuHoldingObject = ent
    def addInventoryEntity(self, ent, index):
        self.MenuContents[index] = ent
    def findMouseover(self):
        global Mouseover
        Mouseover = "Game"
        if ViewMode == "Editor":
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
        
class MultiplayerClient(ConnectionListener):
    def __init__(self):
        pass
    def update(self):
        connection.Pump()
        self.Pump()
        connection.Send({"action" : "movement", "position" : ents.CreatureControlLink.position})
    def connectToServer(self, Adress):
        self.Connect(Adress)
    def Network_NiggaBalls():
        #smash
        pass
    
Client = MultiplayerClient()
ents = Ents()


class ClientChannel(PodSixNet.Channel.Channel):
    def Network(self, data):
        pass
    def Network_movement(self, data):
        Connecteds[0].setPos(data["position"])
 
class BoxesServer(PodSixNet.Server.Server):
 
    channelClass = ClientChannel
 
    def Connected(self, channel, addr):
        print('new connection:', channel)
        newplayer = ents.create("Creature")
        newplayer.setPos((200, 200)) 
        Connecteds.append(newplayer)
        


#Use control F to find specific entities lol
class Particle(pg.sprite.Sprite):
    
    def start(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("strawberry.png", 0)
        self.editsprite = "strawberry.png"
        self.rect.center = (9000,9000)
        self.posOffset = (0, 0)
        self.parent = None
        ents.incrementEntCounter()
        self.id = ents.entCount
        ents.allparticles.append(self)
        self.childs = []
        self.position = (0,0) 
        self.lastVessel = None
        self.vesselCell = None
        self.cellLayer = None
        
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
                self.vesselCell = ents.findCellIndexOfPos(self.position, self.parent.position, 25)
                self.parent.cellTiles[self.vesselCell].append(self)
            else: 
                if self.lastVessel != None:
                    self.removeCellListReference()
                self.vesselCell = self.parent.vesselCell
        
    def update(self):
        self.calculatePosition()
        self.calculateVesselCell()
        self.onTick()
        self.rect.center = vec.sub_2(self.position, (CamX, CamY))
        self.calculatePosition()
        
    def fixPos(self):
        self.calculatePosition()
        self.rect.center = vec.sub_2(self.position, (CamX, CamY))
        self.calculatePosition()
        
    def setPos(self, pos):
        self.posOffset = pos
        self.calculatePosition()
        self.rect.center = vec.sub_2(self.position, (CamX, CamY))
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
        ents.remove(self)
        for ent in self.childs:
            ent.unParent()
            if ent.classname == "FloorItem":
                print("1")
                print(self.classname)
        if self.parent != None:
            self.parent.childs.remove(self)
            if self.parent.classname == "Vessel": self.removeCellListReference()
    
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
        pass
    
    def initialize(self):
        ents.floorlayer.add(self)
        
class Tile(Particle):
    
    def applyparent(self, parent):
        Particle.applyparent(self, parent)
        i = ents.findCellIndexOfPos(self.position, parent.position, 25)
        parent.cellTiles[i][TileSprites[self.tileoffset][2]] = self
        self.vesselCell = i
        self.cellLayer = TileSprites[self.tileoffset][2]
            
    def setTileType(self, offset):
        self.tileoffset = offset
        self.setSprite(TileSprites[offset][0])
        if TileSprites[offset][2] == 0:
            ents.floorlayer.add(self)
        else:
            ents.walllayer.add(self)
        
    def getTileType(self):
        return self.tileoffset
    
    def initialize(self):
        self.tileoffset = 0
    def getData(self):
        ans = Particle.getData(self)
        ans.append(self.tileoffset)
        ans[5] = ans[5] + "i"
        return ans
    def enterData(self, data):
        Particle.enterData(self, data)
        self.setTileType(int(data[7]))
        
class DeleteBrush(Tile):
    
    def onTick(self):
        ent = ents.findBlocksAt(self.position, self.parent)[1]
        if ent != None: ent.remove()
        self.remove()
        
class Thruster(Tile):
    
    def onTick(self):
        pass

class EditorEnt(Particle):
    def initialize(self):
        ents.editlayer.add(self)
        self.image.set_alpha(128)
        self.whiff_sound = sound.load("Crank.wav")
        ents.EditBrush = self
    def onTick(self):
        if ViewMode == "Editor" and Mouseover == "Game":
            self.image.set_alpha(128)
            self.posOffset = MousePosToGridPos(self.parent.position[0], self.parent.position[1])
            if keys[0] == True:
                self.whiff_sound.play()
                entlayer = TileSprites[ents.EditorTileOffset][2]
                previous = ents.findBlocksAt(self.position, self.parent)
                if previous[entlayer] != None: previous[entlayer].remove()
                if entlayer == 0:
                    if previous[1] != None: previous[1].remove()
                placed = ents.create(ents.EditorEntType)
                placed.setTileType(ents.EditorTileOffset)
                placed.setSprite(ents.EditorType)
                placed.setPos(self.position)
                placed.setParent(self.parent)
        else:
            self.image.set_alpha(0)

class Vessel(Particle):
    def initialize(self):
        ents.allvessels.append(self)
        self.cellTiles = []
        i = 0
        while 2601 > i:
            self.cellTiles.append([None,None])
            i = i + 1
        self.velocity = (-0.1,-0.1)
    def onTick(self):
        self.posOffset = vec.add_2(self.posOffset, self.velocity)
    def enterData(self, data): #will break if deleted
        pass
        
class Creature(Particle):
    def WalkableCheck(self, pX, pY):
        ent = ents.findBlocksAt(vec.add_2(self.position, (pX,pY)), self.parent)
        if ent[1] == None or self.parent == None:
            return True
        else:
            return False
    def initialize(self):
        ents.playerlayer.add(self)
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
        if ents.CreatureControlLink == self and ViewMode == "1st":
            if self.moveCooldown <= 0:
                self.stepcounter = self.stepcounter + 1
                if keysHeld[1]:
                    Ymove = Ymove - 1
                if keysHeld[2]:
                    Ymove = Ymove + 1
                if keysHeld[3]:
                    Xmove = Xmove - 1
                if keysHeld[4]:
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
            self.position = (CamX + windowSize[0]/2,CamY + windowSize[1]/2)
    def remove(self):
        Particle.remove(self)
        for ent in self.inventory:
            ent.exitInventory()

class Menu(pg.sprite.Sprite):
    
    def start(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("strawberry.png", -1)
        self.editsprite = "strawberry.png"
        self.rect.center = (9000,9000)
        self.viewmode = "Editor"
        
    def setPos(self, pos):
        self.rect.center = pos
        
    def setPosDimensionless(self, pos):
        self.rect.center = vec.mult_2(pos, (ScreenX,ScreenY))
        
    def setViewMode(self, mode):
        self.viewmode = mode
    
    def setSprite(self, image1):
        prev_center = self.rect.center
        prev_alpha = self.image.get_alpha()
        self.image, self.rect = load_image(image1, 0)
        self.editsprite = image1
        self.rect.center = prev_center
        self.image.set_alpha(prev_alpha)
        
    def update(self):
        if self.viewmode == ViewMode or self.viewmode == "all":
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)
        self.onTick()
        
    def remove(self):
        ents.removeUI(self)
        
    def onTick(self):
        pass
    
    def initialize(self):
        ents.menulayer1.add(self)
        
class MenuB(Menu):
    
    def initialize(self):
        ents.menulayer2.add(self)
        
class EditorIcon(Menu):
    
    def initialize(self):
        ents.menulayer2.add(self)
        ents.allbuttons.append(self)
        self.viewmode = "Editor"
        self.editsprite = "strawberry"
        
    def setSprite(self, image1):
        self.image, self.rect = load_image(image1, -1)
        self.editsprite = image1
    def setproperties(self, offset):
        self.tileoffset = offset
        self.enttype = TileSprites[offset][1]
        self.setSprite(TileSprites[offset][0])
        
    def onTick(self):
        if self.viewmode == "Editor":
            if vec.collision(self.rect.center, 16, pg.mouse.get_pos()):
                if keys[0] == True:
                    ents.EditorType = self.editsprite
                    ents.EditorEntType = self.enttype
                    ents.EditorTileOffset = self.tileoffset
                    ents.EditBrush.setSprite(ents.EditorType)
                    
class SaveLoadButton(Menu):
    def initialize(self):
        ents.menulayer2.add(self)
        ents.allbuttons.append(self)
        self.viewmode = "Editor"
    def pressed(self):
        pass
    def onTick(self):
        if ViewMode == "Editor":
            if vec.collision(self.rect.center, 16, pg.mouse.get_pos()):
                if keys[0] == True:
                    self.pressed()
class SaveButton(SaveLoadButton):
    def pressed(self):
        print("Saving...")
        savetable = ents.getAllTable()
        savestring = ""
        for table in savetable:
            tablestring = ""
            for var in table:
                chunk = str(var)
                chunklen = str(len(chunk))
                tablestring = tablestring + "[" + chunklen + "]" + chunk
            savestring = savestring + "{" + tablestring + "}"
        f = open(os.path.join(data_dir, "savefile.txt"), "w")
        f.write(savestring)
        f.close()
        print("Saved.")
class LoadButton(SaveLoadButton):
    def pressed(self):
        print("Loading...")
        ents.deleteAll()
        f = open(os.path.join(data_dir, "savefile.txt"), "r")
        
        savestring = f.read()
        loadtablesuper = []
        loadtable = []
        loadtablesub = ""
        chunklen = 0
        chunklenstring = ""
        marker = 1
        submarker = 0
        for letter in savestring:
            if marker == 1:
                marker = 2
            elif marker == 2:
                if not letter == "}":
                    if letter == "[":
                        marker = 3
                        chunklen = 0
                        chunklenstring = ""
                else:
                    marker = 1
                    loadtablesuper.append(loadtable)
                    loadtable = []
            elif marker == 3:
                if not letter == "]":
                    chunklenstring = chunklenstring + letter
                else:
                    marker = 4
                    submarker = 0
                    chunklen = int(chunklenstring)
                    loadtablesub = ""
            elif marker == 4:
                submarker = submarker + 1
                loadtablesub = loadtablesub + letter
                if submarker == chunklen:
                    loadtable.append(loadtablesub)
                    marker = 2
        i = ents.entCount
        replacements = {}
        for table in loadtablesuper:
            table[1] = int(table[1])
            if table[1] in replacements:
                table[1] = replacements[table[0]]
            else:
                i = i + 1
                replacements.update({table[1]: i})
                table[1] = i
                ents.incrementEntCounter()
        for table in loadtablesuper:
            i2 = 0
            for letter in table[5]:
                if letter == "1":
                    table[i2] = int(table[i2])
                    if table[i2] in replacements:
                        table[i2] = replacements[table[i2]]
                elif letter == "L":
                    marker = 1
                    tablelist = []
                    chars = ""
                    i = 0
                    for char in table[i2]:
                        if marker == 0:
                            if char == ">":
                                tablelist.append(int(chars))
                                chars = ""
                            else:
                                i += 1
                                chars = chars + char
                        elif marker == 1:
                            marker = 0
                    tablelist.append(int(chars))
                    i3 = 0
                    while i3 < len(tablelist):
                        if tablelist[i3] in replacements:
                            tablelist[i3] = replacements[tablelist[i3]]
                        i3 += 1
                    table[i2] = tablelist
                        
                i2 += 1
        spawnedEnts = []
        for table in loadtablesuper:
            ent = ents.create(table[0])
            ent.calculatePosition()
            ent.setSID(int(table[1]))
            spawnedEnts.append(ent)
        i = 0
        while i < len(loadtablesuper):
            ent = spawnedEnts[i]
            table = loadtablesuper[i]
            ent.enterData(table)
            if ent.classname == "Creature":
                ents.CreatureControlLink = ent
            i += 1
        
        i = 0
        while i < len(loadtablesuper):
            ent = spawnedEnts[i]
            table = loadtablesuper[i]
            ent.setParent(ents.SIDToEnt(int(table[6])))
            i += 1
        
        f.close()
        print("Loaded")
class StartButton(Menu):
    def initialize(self):
        ents.menulayer1.add(self)
        self.pressed = False
    def isPressed(self):
        return self.pressed
    def onTick(self):
        if keys[0] == True:
            if (self.rect.collidepoint(pg.mouse.get_pos())):
                self.pressed = True
        
class MenuItem(Menu):
    def onTick(self):
        if self.viewmode == ViewMode:
            if self.itemActive == True and keys[0] == True:
                collision = False
                for v in ents.HotbarSprites:
                    if v.rect.collidepoint(pg.mouse.get_pos()) == True:
                        collision = True
                if collision == False:
                    self.use()
            if ents.MenuHoldingObject == self and keysHeld[0] == True:
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
                    ents.MenuHoldingObject = 0
                    i2 = 0
                    i = 0
                    while len(ents.MenuPositions) > i:
                        v = ents.MenuPositions[i]
                        if vec.collision(v, 26, self.rect.center):
                            if ents.MenuContents[i] != 0:
                                ents.addInventoryEntity(ents.MenuContents[i], self.inventoryIndex)
                                ents.MenuContents[i].setInventoryIndex(self.inventoryIndex)
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
                        destination = MousePosToPosition(ents.CreatureControlLink.parent)
                        realdestination = 0
                        if ents.CreatureControlLink.parent == None:
                            realdestination = destination
                        else:
                            realdestination = vec.add_2(destination, ents.CreatureControlLink.parent.posOffset)
                        throwspeed = vec.div(vec.sub_2(destination, self.itemlink.posOffset), Gravity)
                        throwmagnitude = vec.distance(throwspeed, (0,0))
                        if throwmagnitude > 25:
                            throwspeed = vec.div(throwspeed, throwmagnitude / 25)
                        if vec.largest(vec.sub_2(destination, self.itemlink.posOffset)) > 48 or ents.findBlocksAt(realdestination, ents.CreatureControlLink.parent)[1] != None:
                            self.itemlink.throw(throwspeed)
                        else:
                            self.itemlink.setPosOffset(destination)
                        ents.addInventoryEntity(0, self.inventoryIndex)
                        self.remove()
                    self.rect.center = ents.MenuPositions[self.inventoryIndex]
                if keys[0] == True:
                    if vec.collision(self.rect.center, 26, pg.mouse.get_pos()):
                        ents.setMenuHoldingObject(self)
                        #self.held = 1
                self.mouseHasLeftButton = False
                
    def initialize(self):
        ents.menulayer1.add(self)
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
        global ActiveMenuItem
        if boolean == True:
            self.crosshaircolor = self.itemlink.crosshaircolor
            ents.HotbarSprites[self.inventoryIndex].setSprite("smallmenuboxactive.png")
            self.itemActive = True
            if ActiveMenuItem != None: ActiveMenuItem.setActive(False)
            ActiveMenuItem = self
            self.itemActivate()
        else:
            ents.HotbarSprites[self.inventoryIndex].setSprite("smallmenubox.png")
            self.itemActive = False
            if ActiveMenuItem == self: ActiveMenuItem = None
    def use(self):
        self.itemlink.use(MousePosToPosition(ents.CreatureControlLink.parent))
    def itemActivate(self):
        self.itemlink.itemActivate()
        
class FloorItem(Particle):
    def initialize(self):
        ents.midlayer.add(self)
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
            if vec.largest(vec.sub_2(ents.CreatureControlLink.position, self.position)) < 48:
                self.putInside(ents.CreatureControlLink, space)
        
    def onTick(self):
        if ViewMode == "1st":
            if vec.collision(self.rect.center, 8, pg.mouse.get_pos()):
                if keys[0] == True:
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
                if abs(direction[0]) + abs(direction[1]) > 1:
                    if hitspeed > 30:
                        self.remove()
                    self.velocity = vec.mult(self.velocity, -0.05)
                elif direction[0] != 0: 
                    self.velocity = (self.velocity[0]*(-0.35),self.velocity[1])
                elif direction[1] != 0:
                    self.velocity = (self.velocity[0],self.velocity[1]*(-0.35))
            self.posOffset = vec.add_2(self.posOffset, self.velocity)
            if tiles[0] == None and tiles[1] == None and self.parent != None:
                self.unParent()
            self.height = self.height - Gravity/200
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
        if ents.CreatureControlLink == ent:
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
        #return abs(self.velocity[1]) + abs(self.velocity[2])
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
        
class MousePointer(Menu):
    
    def initialize(self):
        ents.menulayer3.add(self)
        self.setSprite("greenpointer.png")
        self.viewmode = "all"
        
    def onTick(self):
        self.rect.center = pg.mouse.get_pos()
        if ActiveMenuItem != None and ViewMode == "1st":
            if ActiveMenuItem.crosshaircolor == 1 and self.editsprite != "yellowtarget.png":
                self.setSprite("yellowtarget.png")
            elif ActiveMenuItem.crosshaircolor == 2 and self.editsprite != "redtarget.png":
                self.setSprite("redtarget.png")
        else:
            if self.editsprite != "greenpointer.png":
                self.setSprite("greenpointer.png")
        

def main():
            
    pg.init()
    screen = pg.display.set_mode((ScreenX, ScreenY), pg.SCALED)
    pg.display.set_caption("2D Game Test")
    icon, iconrect = load_image("door7.png", 0)
    pg.display.set_icon(icon)
    pg.mouse.set_visible(False)

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((245, 245, 245))

    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("2D RPG Demo", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)

    screen.blit(background, (0, 0))
    pg.display.flip()
    
    ents.create("MousePointer")
    clock = pg.time.Clock()
    
    serverbutton = ents.create("StartButton")
    serverbutton.setSprite("startserver.png")
    serverbutton.setPosDimensionless((0.5,0.2))
    
    clientbutton = ents.create("StartButton")
    clientbutton.setSprite("startclient.png")
    clientbutton.setPosDimensionless((0.5,0.3))
    
    setserver = False
    
    going = True
    introrunning = True
    while introrunning and going:
        clock.tick(60)
        
        if serverbutton.isPressed():
            introrunning = False
            setserver = True
        elif clientbutton.isPressed():
            introrunning = False
            setserver = False
        going = InputEvents(keys, ents.CreatureControlLink)
        
        ents.findMouseover()
        ents.update()
        
        screen.blit(background, (0, 0))
        ents.draw(screen)
        pg.display.flip()
        
    serverbutton.remove()
    clientbutton.remove()
    
    
    background.fill((0, 0, 0))

    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("v0.0.1", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)

    screen.blit(background, (0, 0))
    pg.display.flip()

    pt1 = ents.create("Vessel")
    pt1.setPos((500,400))
    pt2 = ents.create("EditorEnt")
    pt2.setPos((400,300))
    pt2.setParent(pt1)
    plytest = ents.create("Creature")
    plytest.setPos((532,400))
    plytest.setParent(pt1)
    ents.CreatureControlLink = plytest

    panel1 = ents.create("Menu")
    panel1.setSprite("smallmenubox.png")
    panel1.setViewMode("1st")
    panel1.setPosDimensionless((0.5-(40/ScreenX),0.9))
    panel1text = ents.create("MenuB")
    panel1text.setSprite("lefthandText.png")
    panel1text.setViewMode("1st")
    panel1text.setPosDimensionless((0.5-(40/ScreenX),0.9))
    
    panel2 = ents.create("Menu")
    panel2.setSprite("smallmenubox.png")
    panel2.setViewMode("1st")
    panel2.setPos(vec.add_2(panel1.rect.center,(80,0)))
    panel2text = ents.create("MenuB")
    panel2text.setSprite("righthandText.png")
    panel2text.setViewMode("1st")
    panel2text.setPos(vec.add_2(panel1.rect.center,(80,0)))
    
    load_iter = 0
    for chunk in TileSprites:
        ico = ents.create("EditorIcon")
        ico.setproperties(load_iter)
        ico.setPosDimensionless((0.55+(load_iter*0.035), 0.85))
        load_iter += 1
    
    sbutton = ents.create("SaveButton")
    sbutton.setSprite("save.png")
    sbutton.setPosDimensionless((0.1,0.05))
    
    lbutton = ents.create("LoadButton")
    lbutton.setSprite("load.png")
    lbutton.setPosDimensionless((0.15,0.05))
    
    ents.MenuPositions = [panel1.rect.center,panel2.rect.center]
    ents.HotbarSprites = [panel1, panel2]
    
    testitem = ents.create("FloorItem")
    testitem.setSprite("woodbox.png")
    testitem.putInside(plytest, 0)
    
    testitem2 = ents.create("Gun")
    testitem2.putInside(plytest, 1)
    
    host, port="localhost", 8000
    boxesServe = BoxesServer(localaddr=(host, int(port)))
    
    if (setserver): 
        GameServer = True
    else: 
        GameServer = False
        Client.connectToServer(("localhost", 8000))
    
    while going:
        clock.tick(60)
        if (GameServer): 
            boxesServe.Pump()
        
        going = InputEvents(keys, ents.CreatureControlLink)
        
        ents.findMouseover()
        ents.update()
        Client.update()
        
        screen.blit(background, (0, 0))
        ents.draw(screen)
        pg.display.flip()
        
    pg.quit()


if __name__ == "__main__":
    main()