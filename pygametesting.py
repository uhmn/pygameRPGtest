import pygame as pg
import vec
import Globals
import ents
import net
from pygamefunctions import load_image

import E_Particle
import E_EditorEnt
import E_Vessel
import E_Creature
import E_Menu
import E_MenuB
import E_MenuItem
import E_MousePointer
import E_EditorIcon
import E_SaveButton
import E_LoadButton
import E_StartButton
import E_Tile
import E_DeleteBrush
import E_FloorItem
import E_Gun
import E_WaterGun
import E_Thruster

def GetEntityTypes(self):
    return ({
      "Particle"        :    E_Particle.Particle(),
      "EditorEnt"       :    E_EditorEnt.EditorEnt(),
      "Vessel"          :    E_Vessel.Vessel(),
      "Creature"        :    E_Creature.Creature(),
      "Menu"            :    E_Menu.Menu(),
      "MenuB"           :    E_MenuB.MenuB(),
      "MenuItem"        :    E_MenuItem.MenuItem(),
      "MousePointer"    :    E_MousePointer.MousePointer(),
      "EditorIcon"      :    E_EditorIcon.EditorIcon(),
      "SaveButton"      :    E_SaveButton.SaveButton(),
      "LoadButton"      :    E_LoadButton.LoadButton(),
      "StartButton"     :    E_StartButton.StartButton(),
      "Tile"            :    E_Tile.Tile(),
      "DeleteBrush"     :    E_DeleteBrush.DeleteBrush(),
      "FloorItem"       :    E_FloorItem.FloorItem(),
      "Gun"             :    E_Gun.Gun(),
      "WaterGun"        :    E_WaterGun.WaterGun(),
      "Thruster"        :    E_Thruster.Thruster()
    })

ents.initialize(GetEntityTypes)

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
            elif event.key == pg.K_s:
                Globals.debug -= 1
                print(Globals.debug)
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





#Use control F to find specific entities lol

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
        GameServer = True
        net.Client.connectToServer(("localhost", 1)) #I have no idea why but for some reason if this doesn't run first when the server is starting it will cause it to break.
        print("Server")
    else: 
        GameServer = False
        
        net.Client.connectToServer((net.host, net.port))
        print("Client")
    
    while going:
        clock.tick(60)
        if (GameServer): 
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