
import os
import pygame as pg
import vec
import random

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
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)

    return sound
     

keys = [False,False,False,False,False,False]
keysHeld = [False,False,False,False,False,False]
keysPressed = 0
CamX = 0
CamY = 0
ViewMode = "Editor"
    
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






class Ents():
    
    def __init__(self):
        self.allsprites = pg.sprite.RenderPlain()
        self.floorlayer = pg.sprite.RenderPlain()
        self.midlayer = pg.sprite.RenderPlain()
        self.playerlayer = pg.sprite.RenderPlain()
        self.allvessels = []
        self.CreatureControlLink = 0
        
    def create(self, etype):
        entitytypes = {
          "Particle": Particle(),
          "EditorEnt": EditorEnt(),
          "Vessel": Vessel(),
          "Creature": Creature()
        }
        ent = entitytypes[etype]
        self.allsprites.add(ent)
        if etype == "Vessel": self.allvessels.append(ent)
        if etype == "Particle": self.floorlayer.add(ent)
        if etype == "Creature": self.midlayer.add(ent)
        if etype == "EditorEnt": self.playerlayer.add(ent)
        return ent
    
    def update(self):
        self.allsprites.update()
        
    def draw(self, screen):
        self.floorlayer.draw(screen)
        self.midlayer.draw(screen)
        self.playerlayer.draw(screen)
        
    def findCellIndexOfPos(self, pos, vesselPos, cellSize):
        rowLength = (cellSize*2)+1
        Offset = vec.sub_2(vec.round2(vec.div(pos,32)), vec.round2(vec.div(vesselPos,32)))
        Xo = Offset[0]+cellSize
        Yo = Offset[1]+cellSize
        lis = Xo + (Yo * rowLength)
        return lis
    def findEntAtCellIndex(self, cellIndex, vessel):
        if len(vessel.cellTiles) < cellIndex:
            return False
        return vessel.cellTiles[cellIndex]
        
    def findBlockAt(self, pos, vessel):
        cIndex = self.findCellIndexOfPos(pos, vessel.position, 25)
        return self.findEntAtCellIndex(cIndex, vessel)
        #for v in self.allvessels:
        #    pass

ents = Ents()

class Particle(pg.sprite.Sprite):
    
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("strawberry.png", -1)
        self.posOffset = (0, 0)
        self.initialize()
        self.parent = 0
        
    def calculatePosition(self):
        if self.parent != 0:
            self.position = vec.add_2(self.posOffset, self.parent.posOffset)
        else:
            self.position = self.posOffset
        
    def update(self):
        self.calculatePosition()
        self.onTick()
        self.rect.center = vec.sub_2(self.position, (CamX, CamY))
        self.calculatePosition()
        
    def setPos(self, pos):
        self.posOffset = pos
        self.calculatePosition()
        
    def setParent(self, parent):
        self.parent = parent
        
        self.posOffset = vec.sub_2(self.position, self.parent.position)
        i = ents.findCellIndexOfPos(self.position, parent.position, 25)
        parent.cellTiles[i] = self
        
    def onTick(self):
        pass
    
    def initialize(self):
        pass

class EditorEnt(Particle):
    def initialize(self):
        self.image.set_alpha(128)
        self.whiff_sound = load_sound("Crank.wav")
    def onTick(self):
        self.posOffset = vec.mult(vec.round2(vec.div(vec.sub_2(vec.add_2(pg.mouse.get_pos(), (CamX,CamY) ), self.parent.position), 32)), 32)
        if keys[0] == True:
            self.whiff_sound.play()
            placed = ents.create("Particle")
            placed.setPos(self.position)
            placed.setParent(self.parent)

class Vessel(Particle):
    def initialize(self):
        self.cellTiles = []
        i = 0
        while 2601 > i:
            self.cellTiles.append(0)
            i = i + 1
    def onTick(self):
        self.posOffset = vec.sub(self.posOffset, 0.1)
        
class Creature(Particle):
    def initialize(self):
        self.moveCooldown = 0
        self.lastMoveCooldown = 0
        self.lastPosition = (0,0)
        self.image, self.rect = load_image("man2.png", -1)
        self.stepcounter = 0
        self.stepcounter2 = 0
        self.stepsounds = [load_sound("FR1.wav"),load_sound("FR2.wav"),load_sound("FR3.wav"),load_sound("FL1.wav"),load_sound("FL2.wav"),load_sound("FL3.wav")]
    def onTick(self):
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
                        if ents.findBlockAt(vec.add_2(self.position, (Xmove*32,Ymove*32)), self.parent) == False:
                            if ents.findBlockAt(vec.add_2(self.position, (Xmove*32,0)), self.parent) != False:
                                Ymove = 0
                                
                            elif ents.findBlockAt(vec.add_2(self.position, (0,Ymove*32)), self.parent) != False:
                                Xmove = 0
                        
                    if ents.findBlockAt(vec.add_2(self.position, (Xmove*32,0)), self.parent) != False:
                        self.posOffset = vec.add_2(self.posOffset,(Xmove*32,0))
                        
                    if ents.findBlockAt(vec.add_2(self.position, (0,Ymove*32)), self.parent) != False:
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
        


def main():
    pg.init()
    screen = pg.display.set_mode((1280, 480), pg.SCALED)
    pg.display.set_caption("2D Game Test")
    pg.mouse.set_visible(False)

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("Test", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)

    screen.blit(background, (0, 0))
    pg.display.flip()

    clock = pg.time.Clock()
    pt1 = ents.create("Vessel")
    pt1.setPos((500,400))
    pt2 = ents.create("EditorEnt")
    pt2.setPos((400,300))
    pt2.setParent(pt1)
    plytest = ents.create("Creature")
    plytest.setPos((532,400))
    plytest.setParent(pt1)
    ents.CreatureControlLink = plytest

    
    going = True
    while going:
        clock.tick(60)

        going = InputEvents(keys, ents.CreatureControlLink)
        
        ents.update()

        screen.blit(background, (0, 0))
        ents.draw(screen)
        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
