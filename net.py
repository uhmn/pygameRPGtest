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
        i = 0
        while ents.getTick() < data["gametick"]:
            ents.update()
            i += 1
    def Network_newconnection(self, data):
        newplayer = ents.create("Creature")
        newplayer.setPosOffset(data["position"]) 
        Globals.ConnectedCreatures.append(newplayer)
    def Network_entmethod(self, data):
        ent = ents.SIDToEnt(data["eid"])
        parameter = data["parameter"]
        if ent != None:
            fdict = ent.NetworkingMethods
            fdict[parameter](ent)
    def Network_new_ent(self, data):
        eid = data["eid"]
        parameter = data["parameter"]
        myent = ents.create(parameter)
        Globals.NetEnts.append({myent.getSID() : eid})
    def Network_receive_ents(self, data):
        pass
    def entAction(self, action, eid, parameter):
        connection.Send({"action" : "entaction", "action2" : action, "eid" : eid, "parameter" : parameter})
    def getServerEnts(self, table):
        connection.Send({"action" : "getServerEnts", "table" : table})
     

def NetAction(action, sid, parameter):
    if sid != None:
        Server.entAction(action, sid, parameter)
        Client.entAction(action, sid, parameter)


class ClientChannel(PodSixNet.Channel.Channel):
    def Network_movement(self, data):
        curPlayerid = data["playerid"]
        curPos = data["position"]
        Globals.ConnectedsList[curPlayerid][0].setPosOffset(curPos)
        for k in Globals.ConnectedsList:
            if k[1] != curPlayerid:
                channel = k[2]
                if channel != False: channel.Send({"action" : "movement2", "position" : curPos, "playerid" : curPlayerid})
    def Network_entaction(self, data):
        action2 = data["action2"]
        eid = data["eid"]
        parameter = data["parameter"]
        NetAction(action2, eid, parameter)
        MultiplayerClient.__dict__["Network_" + action2](Client, data)
    def Network_getServerEnts(self, data):
        pass
        
class BoxesServer(PodSixNet.Server.Server):
 
    channelClass = ClientChannel
    def start(self):
        self.totalplayers = 0
        Globals.ConnectedsList.append((ents.getCreatureControlLink(), 0, False))
    def update(self):
        for k in Globals.ConnectedsList:
            channel = k[2]
            if channel != False: 
                channel.Send({"action" : "movement2", "position" : ents.getCreatureControlLink().posOffset, "playerid" : 0})
    def entAction(self, action, eid, parameter):
        for k in Globals.ConnectedsList:
            channel = k[2]
            if channel != False: 
                channel.Send({"action" : action, "eid" : eid, "parameter" : parameter})
    def Connected(self, channel, addr):
        print('new connection:', channel)
        self.totalplayers += 1
        savefile = slf.formatTiles(ents.getallparticles())
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