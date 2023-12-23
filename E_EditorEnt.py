from pygamefunctions import MousePosToGridPos
import ents
import Globals
import net
import E_Particle
import sound

class EditorEnt(E_Particle.Particle):
    NetworkingMethods = {}
    def initialize(self): 
        ents.editlayer_add(self)
        self.image.set_alpha(128)
        self.whiff_sound = sound.load("Crank.wav")
        Globals.EditBrush = self
    def onTick(self):
        if Globals.ViewMode == "Editor" and Globals.Mouseover == "Game" and ents.getTick() > 5:
            self.image.set_alpha(128)
            self.posOffset = MousePosToGridPos(self.parent.position[0], self.parent.position[1])
            #if Globals.keysHeld[0] == True:
            if Globals.keys[0] == True:
                entlayer = Globals.TileSprites[Globals.EditorTileOffset][2]
                previous = ents.findBlocksAt(self.position, self.parent)
                
                lastsprite = None
                if previous[entlayer] != None: lastsprite = previous[entlayer].editsprite
                
                if lastsprite != Globals.EditorType or (entlayer == 0 and previous[1] != None):
                    '''
                    if previous[entlayer] != None: previous[entlayer].remove()
                    if entlayer == 0:
                        if previous[1] != None: previous[1].remove()
                    if Globals.EditorEntType != "DeleteBrush": self.whiff_sound.play()
                    placed = ents.create(Globals.EditorEntType)
                    placed.setTileType(Globals.EditorTileOffset)
                    placed.setSprite(Globals.EditorType)
                    placed.setPos(self.position)
                    placed.setParent(self.parent)
                    '''
                    parameters = ("placeblock", entlayer, Globals.EditorEntType, Globals.EditorTileOffset, Globals.EditorType, self.position, self.parent.pid)
                    if Globals.GameServer:
                        self.placeBlock(parameters)
                    else:
                        net.NetAction("entmethod2", self.pid, parameters)
                    
                    
                    

        else:
            self.image.set_alpha(0)
            
    def placeBlock(self, parameter):
        #if ents.PIDTOEnt()
        xy = parameter[5]
        enttype = parameter[2]
        tileoffset = parameter[3]
        editortype = parameter[4]
        parent = ents.PIDToEnt(parameter[6])
        entlayer = parameter[1]
        
        previous = ents.findBlocksAt(xy, parent)
        if previous[entlayer] != None: previous[entlayer].remove()
        if entlayer == 0:
            if previous[1] != None: previous[1].remove()
        if Globals.EditorEntType != "DeleteBrush": self.whiff_sound.play()
        placed = ents.create(enttype)
        placed.setTileType(tileoffset)
        placed.setSprite(editortype)
        placed.setPos(xy)
        placed.setParent(parent)
    NetworkingMethods.update({"placeblock" : placeBlock})
    