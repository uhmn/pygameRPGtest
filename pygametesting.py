import pygame as pg
import vec
import Globals
import ents
import net
from pygamefunctions import load_image, InputEvents

import initialize_ents
initialize_ents.initialize()

def main():
            
    pg.init()
    screen = pg.display.set_mode((Globals.ScreenX, Globals.ScreenY), pg.SCALED)
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
        going = InputEvents(Globals.keys, Globals.keysHeld, ents.getCreatureControlLink())
        
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
    ents.setCreatureControlLink(plytest)

    panel1 = ents.create("Menu")
    panel1.setSprite("smallmenubox.png")
    panel1.setViewMode("1st")
    panel1.setPosDimensionless((0.5-(40/Globals.ScreenX),0.9))
    panel1text = ents.create("MenuB")
    panel1text.setSprite("lefthandText.png")
    panel1text.setViewMode("1st")
    panel1text.setPosDimensionless((0.5-(40/Globals.ScreenX),0.9))
    
    panel2 = ents.create("Menu")
    panel2.setSprite("smallmenubox.png")
    panel2.setViewMode("1st")
    panel2.setPos(vec.add_2(panel1.rect.center,(80,0)))
    panel2text = ents.create("MenuB")
    panel2text.setSprite("righthandText.png")
    panel2text.setViewMode("1st")
    panel2text.setPos(vec.add_2(panel1.rect.center,(80,0)))
    
    load_iter = 0
    for chunk in Globals.TileSprites:
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
    
    net.Server.start()
    
    if (setserver): 
        Globals.GameServer = True
        net.Client.connectToServer(("localhost", 1)) #I have no idea why but for some reason if this doesn't run first when the server is starting it will cause it to break.
        print("Server")
    else: 
        Globals.GameServer = False
        
        net.Client.connectToServer((net.host, net.port))
        print("Client")
    
    while going:
        clock.tick(60)
        if (Globals.GameServer): 
            net.Server.update()
            net.Server.Pump()
        
        going = InputEvents(Globals.keys, Globals.keysHeld, ents.getCreatureControlLink())
        
        ents.findMouseover()
        ents.update()
        
        net.Client.update()
        
        screen.blit(background, (0, 0))
        ents.draw(screen)
        pg.display.flip()
        ents.incrementGameTick()
    pg.quit()


if __name__ == "__main__":
    main()