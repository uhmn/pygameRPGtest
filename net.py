from PodSixNet.Connection import ConnectionListener, connection
import PodSixNet.Channel
import PodSixNet.Server
import ents
import Globals
import saveloadfunctions as slf
  
class MultiplayerClient(ConnectionListener):
    def __init__(self):
        self.playerid = 0
    def update(self):
        connection.Pump()
        self.Pump()
        connection.Send({"action" : "movement", "position" : ents.getCreatureControlLink().posOffset, "playerid" : self.playerid})
            
    def connectToServer(self, Address):
        self.Connect(Address)
    def Network_movement2(self, data):
        if len(Globals.ConnectedCreatures) > 0:
            Globals.ConnectedCreatures[data["playerid"]].setPosOffset(data["position"])
    def Network_connectsuccess(self, data):
        print("Loading...")
        ents.deleteAll()
        slf.loadTiles(data["savefile"])        #Loading the server's savefile
        ents.GameTick = 0
        print("Loaded")
        
        self.playerid = data["playerid"]
        i = 0
        while i < self.playerid:
            newplayer = ents.create("Creature")
            newplayer.setPosOffset((0,0)) 
            Globals.ConnectedCreatures.append(newplayer)
            i += 1
        Globals.ConnectedCreatures.append(ents.getCreatureControlLink())
        #i = 0
        #while ents.getTick() < data["gametick"]:
        #    ents.update()
        #    i += 1
    def Network_newconnection(self, data):
        newplayer = ents.create("Creature")
        newplayer.setPosOffset(data["position"]) 
        Globals.ConnectedCreatures.append(newplayer)
    def Network_entmethod(self, data):
        ent = ents.PIDToEnt(data["pid"])
        funcindex = data["parameter"]
        if ent != None:
            fdict = ent.NetworkingMethods
            fdict[funcindex](ent)
    def Network_entmethod2(self, data):
        ent = ents.PIDToEnt(data["pid"])
        funcindex = data["parameter"][0]
        funcparams = data["parameter"]
        if ent != None:
            fdict = ent.NetworkingMethods
            fdict[funcindex](ent, funcparams)
    #def Network_new_ent(self, data):
    #    pid = data["pid"]
    #    parameter = data["parameter"]
    #    myent = ents.create(parameter)
    #    Globals.NetEnts.append({myent.getID() : pid})
    #def Network_receive_ents(self, data):
    #    pass
    def Network_newent(self, data):
        savestring = data["ents_string"]
        #check = ents.PIDToEnt(pid)
        #if check != None:
        #    check.remove()
        slf.loadTilesPID(savestring)
    def entAction(self, action, pid, parameter):
        connection.Send({"action" : "entaction", "action2" : action, "pid" : pid, "parameter" : parameter, "playerid" : self.playerid}) #2
    def getServerEnts(self, table):
        connection.Send({"action" : "getServerEnts", "table" : table})
   

def NetAction(action, pid, parameter, *argv):
    if pid != None:
        origClient = 0
        if len(argv) != 0:
            origClient = argv[0]
        Server.entAction(action, pid, parameter, origClient) #4
        Client.entAction(action, pid, parameter) #1, starts here
       


'''
       
def ActionCreateEnt(action, pid, entity):
    entitystring = slf.formatTiles([entity])
    if pid != None:
        Server.entAction(action, pid, entitystring)
        #Client.entAction(action, pid, entitystring)
'''
class ClientChannel(PodSixNet.Channel.Channel):
    def Network_movement(self, data):
        curPlayerid = data["playerid"]
        curPos = data["position"]
        Globals.ConnectedsList[curPlayerid][0].setPosOffset(curPos)
        for k in Globals.ConnectedsList:
            if k[1] != curPlayerid:
                channel = k[2]
                if channel != False: channel.Send({"action" : "movement2", "position" : curPos, "playerid" : curPlayerid})
    def Network_entaction(self, data): #3
        action2 = data["action2"]
        pid = data["pid"]
        parameter = data["parameter"]
        playerid = data["playerid"]
        NetAction(action2, pid, parameter, playerid)
        MultiplayerClient.__dict__["Network_" + action2](Client, data)
    def Network_getServerEnts(self, data):
        pass
        
class BoxesServer(PodSixNet.Server.Server):
 
    channelClass = ClientChannel
    def start(self):
        self.totalplayers = 0
        Globals.ConnectedsList.append((ents.getCreatureControlLink(), 0, False))
    def update(self):
        send_ents = Globals.ServerLastCreatedEnts
        ents_string = None
        if len(send_ents) != 0: ents_string = slf.formatTiles(send_ents, False)
        
        Globals.ServerLastCreatedEnts.clear()
        for k in Globals.ConnectedsList:
            channel = k[2]
            if channel != False: 
                channel.Send({"action" : "movement2", "position" : ents.getCreatureControlLink().posOffset, "playerid" : 0})
                if ents_string != None:
                    channel.Send({"action" : "newent", "ents_string" : ents_string})
    def entAction(self, action, pid, parameter, origClient): #5, broadcasted to clients here
        for k in Globals.ConnectedsList:
            channel = k[2]
            if channel != False and k[1] != origClient: 
                channel.Send({"action" : action, "pid" : pid, "parameter" : parameter})
    def Connected(self, channel, addr):
        print('new connection:', channel)
        self.totalplayers += 1
        savefile = slf.formatTiles(ents.get_p_entity_array(), False)
        channel.Send({"action" : "connectsuccess", "position" : ents.getCreatureControlLink().posOffset, "playerid" : self.totalplayers, "gametick" : ents.getTick(), "savefile" : savefile})
        newplayer = ents.create("Creature")
        newplayer.setPosOffset((200, 200))
        Globals.ConnectedsList.append((newplayer, self.totalplayers, channel))
        for k in Globals.ConnectedsList:
            if k[1] != self.totalplayers:
                channel2 = k[2]
                if channel2 != False: channel2.Send({"action" : "newconnection", "position" : ents.getCreatureControlLink().posOffset, "playerid" : self.totalplayers})
                
Client = MultiplayerClient()

host, port="localhost", 8000
#host = input("Input the server's IP")
#port = int(input("Input the server's port"))
Server = BoxesServer(localaddr=(host, int(port)))