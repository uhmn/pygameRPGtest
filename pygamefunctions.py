import pygame as pg
import os
import Globals
import vec

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