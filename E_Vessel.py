import ents
import Globals
import vec
import net
import E_Particle

class Vessel(E_Particle.Particle):
    
    NetworkingMethods = {}
    
    def initialize(self):
        ents.allvessels_append(self)
        self.cellTiles = []
        self.cellListLength = (Globals.CellSize*Globals.CellSize*5)
        i = 0
        while self.cellListLength > i: #2601-25
            self.cellTiles.append([None,None])
            i = i + 1
        self.velocity = (-0.05, -0.05)
        #self.velocity = (0, 0)
    def onTick(self):
        self.posOffset = vec.add_2(self.posOffset, self.velocity)
        if Globals.GameServer:
            net.NetAction("entmethod2", self.pid, ("netsetpos", self.posOffset))
    def netSetPos(self, parameter):
        self.posOffset = parameter[1]
    def enterData(self, data, deref): #will break if deleted
        #self.classname = data[0]
        #self.setSprite(data[2])
        #self.posOffset = (float(data[3]), float(data[4]))
        #self.calculatePosition()
        pass  
    NetworkingMethods.update({"netsetpos" : netSetPos})