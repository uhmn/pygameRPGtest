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
                if Globals.ViewMode == "Editor" and CreatureControlLink != None:
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
                DrawShadows()
            elif event.key == pg.K_a:
                print(ents.getCreatureControlLink().pid)
                print(Globals.ConnectedCreatures)
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
    if Globals.ViewMode == "1st" and CreatureControlLink != 0 and CreatureControlLink != None:
        Globals.windowSize = pg.display.get_window_size()
        if CreatureControlLink.moveCooldown > 0:
            slider = CreatureControlLink.moveCooldown / CreatureControlLink.lastMoveCooldown
            Globals.CamX = slider*(CreatureControlLink.lastPosition[0]-Globals.windowSize[0]/2)+(1-slider)*(CreatureControlLink.position[0]-Globals.windowSize[0]/2)
            Globals.CamY = slider*(CreatureControlLink.lastPosition[1]-Globals.windowSize[1]/2)+(1-slider)*(CreatureControlLink.position[1]-Globals.windowSize[1]/2)
        else:
            Globals.CamX = CreatureControlLink.position[0]-Globals.windowSize[0]/2
            Globals.CamY = CreatureControlLink.position[1]-Globals.windowSize[1]/2
    return going

def greatest(vector1, vector2):
    x = vector1[0]
    if vector2[0] > x: x = vector2[0]
    y = vector1[1]
    if vector2[1] > y: y = vector2[1]
    return (x,y)

def smallest(vector1, vector2):
    x = vector1[0]
    if vector2[0] < x: x = vector2[0]
    y = vector1[1]
    if vector2[1] < y: y = vector2[1]
    return (x,y)

def intersect_rect(l1, l2, rect_center):
    rr = 16
    r_right  = vec.add_2(rect_center, (rr,0))[0]
    r_left   = vec.add_2(rect_center, (-rr,0))[0]
    r_top    = vec.add_2(rect_center, (0,rr))[1]
    r_bottom = vec.add_2(rect_center, (0,-rr))[1]
    l_right  = greatest(l1, l2)[0]
    l_left   = smallest(l1, l2)[0]
    l_top    = greatest(l1, l2)[1]
    l_bottom = smallest(l1, l2)[1]
    linewidth = abs(l_right-l_left)
    def xty(middleX):
        if linewidth == 0:  ratio = 1
        else:               ratio = (middleX-l_left) / linewidth
        return (l_top*(1-ratio))+(l_bottom*ratio)
    linepointY_left  = xty(r_left)
    linepointY_right = xty(r_right)
    if (linepointY_left > r_bottom and linepointY_left < r_top) or (linepointY_right > r_bottom and linepointY_right < r_top):
        return True
    else:
        return False
    
def draw2(point1, point2, surface, illumPoint):
    pd1 = vec.sub_2(point1, illumPoint)
    pd2 = vec.sub_2(point2, illumPoint)
    pd1 = vec.mult(pd1, 8)
    pd2 = vec.mult(pd2, 8)
    pd1 = vec.add_2(pd1, point1)
    pd2 = vec.add_2(pd2, point2)
    points = []
    points.append(point1)
    points.append(point2)
    points.append(pd2)
    points.append(pd1)
    
    pg.draw.polygon(surface, pg.Color(0,0,0, 128), points)
repeatcount = 0
#allpoints = []
def DrawShadows():
    global repeatcount
    #global allpoints
    

    
    illumPoint = ents.getCreatureControlLink()
    if illumPoint != None:
        illumPoint = illumPoint.rect.center
            
        repeatcount += 1
        if repeatcount > 2:
            repeatcount = 0
            
            surface = Globals.ShadowSurface
            Globals.ShadowSurface.fill((0, 0, 0, 0))
            #allpoints = []
            vessel_list = ents.getallvessels()
            wall_list = []
            exemptWallList = []
            visWallList = []
            for vessel in vessel_list:
                for ent in vessel.childs:
                    if ent.classname == "Tile":
                        if ent.tileSpriteData(2) == 1:
                            wall_list.append(ent)
            for wall in wall_list:
                rect_center = wall.rect.center
                TL = vec.add_2(rect_center, (-16,-16))
                TR = vec.add_2(rect_center, (16,-16))
                BL = vec.add_2(rect_center, (-16,16))
                BR = vec.add_2(rect_center, (16,16))
                
                def checkall(startpoint):
                    for wall2 in wall_list:
                        rect2_center = wall2.rect.center
                        if intersect_rect(startpoint, illumPoint, rect2_center):
                            return 1
                    return 0
                TLO = checkall(TL)
                TRO = checkall(TR)
                BLO = checkall(BL)
                BRO = checkall(BR)
                
                obstructions = TLO+TRO+BLO+BRO
                if obstructions < 4:
                    visWallList.append(wall)
                def draw(point1, point2):
                    #allpoints.append((point1, point2))
                    
                    pd1 = vec.sub_2(point1, illumPoint)
                    pd2 = vec.sub_2(point2, illumPoint)
                    pd1 = vec.mult(pd1, 8)
                    pd2 = vec.mult(pd2, 8)
                    pd1 = vec.add_2(pd1, point1)
                    pd2 = vec.add_2(pd2, point2)
                    
                    points = []
                    points.append(point1)
                    points.append(point2)
                    points.append(pd2)
                    points.append(pd1)
                    #allpoints.append(points)
                    
                    pg.draw.polygon(surface, pg.Color(0,0,0, 128), points)
                if TLO+TRO != 3: draw(TL, TR)
                if TRO+BRO != 3: draw(TR, BR)
                if BLO+BRO != 3: draw(BL, BR)
                if BLO+TLO != 3: draw(BL, TL)
            #if len(points) > 2:
            #    pg.draw.polygon(surface, pg.Color(0,0,0, 128), points)
       # for points in allpoints:
        #    draw2(points[0], points[1], surface, illumPoint)
            #pg.draw.polygon(surface, pg.Color(0,0,0, 128), points)

            
    '''
    wall_list = ents.getwalllayer().sprites()
    for item in wall_list:
        rect_center = item.rect.center
        TL = vec.add_2(rect_center, (-16,-16))
        TR = vec.add_2(rect_center, (16,-16))
        BL = vec.add_2(rect_center, (-16,16))
        BR = vec.add_2(rect_center, (16,16))
        points = []
        points.append(TL)
        points.append(TR)
        points.append(BL)
        pg.draw.polygon(layer, pg.Color(0,0,0), points)
    '''