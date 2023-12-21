import os

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")
LastCreatedEnts = []
ConnectedCreatures = []
ConnectedsList = []
NetEnts = []

TileSprites = [("strawberry.png","Tile",0), 
               ("wall.png","Tile",1), 
               ("wall2.png","Tile",1), 
               ("wall3.png","Tile",1),
               ("grate.png","Tile",0), 
               ("girderwallLR.png","Tile",1), 
               ("girderwallUD.png","Tile",1), 
               ("girderwallLRUD.png","Tile",1), 
               ("deletebrush.png","DeleteBrush",0),
               ("thrusterL.png","Thruster",1),
               ("thrusterR.png","Thruster",1),
               ("thrusterU.png","Thruster",1),
               ("thrusterD.png","Thruster",1)]
keys = [False,False,False,False,False,False]
keysHeld = [False,False,False,False,False,False]
keysPressed = 0
CamX = 0
CamY = 0
ViewMode = "Editor"
ScreenX = 1080
ScreenY = 480
Mouseover = "Game"
Gravity = 9.8
ActiveMenuItem = None
GameServer = False
CellSize = 50

GetEntityTypes = None

EditorType = "strawberry.png"
EditorTileOffset = 0
EditorEntType = "Tile"
EditBrush = None

debug = 0