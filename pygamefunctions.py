import pygame as pg
import os
import Globals
import vec
import ents

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")



def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(Globals.data_dir, name)
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


def MousePosToGridPos(parentX, parentY):
    return vec.mult(vec.round2(vec.div(vec.sub_2(vec.add_2(pg.mouse.get_pos(), (Globals.CamX,Globals.CamY) ), (parentX,parentY)), 32)), 32)
def MousePosToVesselPos(parentX, parentY):
    return vec.round2(vec.sub_2(vec.add_2(pg.mouse.get_pos(), (Globals.CamX,Globals.CamY) ), (parentX,parentY)))
def MousePosToPosition(parent):
    if parent == None:
        return MousePosToVesselPos(0, 0)
    else:
        return MousePosToVesselPos(parent.position[0], parent.position[1])
    
def InputEvents(keys, keysHeld, CreatureControlLink):
    going = True
    for v in keys:
        keys[v] = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            going = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                going = False
            elif event.key == pg.K_UP:
                Globals.keysPressed += 1
                keys[1] = True
                keysHeld[1] = True
            elif event.key == pg.K_DOWN:
                Globals.keysPressed += 1
                keys[2] = True
                keysHeld[2] = True
            elif event.key == pg.K_LEFT:
                Globals.keysPressed += 1
                keys[3] = True
                keysHeld[3] = True
            elif event.key == pg.K_RIGHT:
                Globals.keysPressed += 1
                keys[4] = True
                keysHeld[4] = True
            elif event.key == pg.K_RETURN:
                keys[5] = True
                if Globals.ViewMode == "Editor":
                    Globals.ViewMode = "1st"
                else:
                    Globals.ViewMode = "Editor"
            elif event.key == pg.K_q:
                testitem2 = ents.create(input("Input itemtype:"))
                testitem2.putInside(ents.getCreatureControlLink(), 1)
            elif event.key == pg.K_w:
                Globals.debug += 1
                print(Globals.debug)
                #print(ents.self.p_entity_array)
            elif event.key == pg.K_s:
                Globals.debug -= 1
                print(Globals.debug)
            elif event.key == pg.K_d:
                print(ents.self.p_entity_array)
            elif event.key == pg.K_a:
                print(ents.getCreatureControlLink().position)
        elif event.type == pg.MOUSEBUTTONDOWN:
            keys[0] = True
            keysHeld[0] = True
        elif event.type == pg.MOUSEBUTTONUP:
            keysHeld[0] = False
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                keysHeld[1] = False
                Globals.keysPressed = Globals.keysPressed - 1
            elif event.key == pg.K_DOWN:
                keysHeld[2] = False
                Globals.keysPressed = Globals.keysPressed - 1
            elif event.key == pg.K_LEFT:
                keysHeld[3] = False
                Globals.keysPressed = Globals.keysPressed - 1
            elif event.key == pg.K_RIGHT:
                keysHeld[4] = False
                Globals.keysPressed = Globals.keysPressed - 1
    if Globals.keysPressed != 0:
        if Globals.ViewMode == "Editor":
            if keysHeld[1] == True:
                Globals.CamY = Globals.CamY - (16/(Globals.keysPressed/(Globals.keysPressed/1.5)))
        
            if keysHeld[2] == True:
                Globals.CamY = Globals.CamY + (16/(Globals.keysPressed/(Globals.keysPressed/1.5)))
        
            if keysHeld[3] == True:
                Globals.CamX = Globals.CamX - (16/(Globals.keysPressed/(Globals.keysPressed/1.5)))
        
            if keysHeld[4] == True:
                Globals.CamX = Globals.CamX + (16/(Globals.keysPressed/(Globals.keysPressed/1.5)))
    if Globals.ViewMode == "1st" and CreatureControlLink != 0:
        Globals.windowSize = pg.display.get_window_size()
        if CreatureControlLink.moveCooldown > 0:
            slider = CreatureControlLink.moveCooldown / CreatureControlLink.lastMoveCooldown
            Globals.CamX = slider*(CreatureControlLink.lastPosition[0]-Globals.windowSize[0]/2)+(1-slider)*(CreatureControlLink.position[0]-Globals.windowSize[0]/2)
            Globals.CamY = slider*(CreatureControlLink.lastPosition[1]-Globals.windowSize[1]/2)+(1-slider)*(CreatureControlLink.position[1]-Globals.windowSize[1]/2)
        else:
            Globals.CamX = CreatureControlLink.position[0]-Globals.windowSize[0]/2
            Globals.CamY = CreatureControlLink.position[1]-Globals.windowSize[1]/2
    return going