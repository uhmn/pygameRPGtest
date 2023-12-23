import Globals
import os
import ents

from E_Menu import Menu
import pygame as pg
import vec


class SaveLoadButton(Menu):
    def initialize(self):
        ents.menulayer2_add(self)
        ents.allbuttons_append(self)
        self.viewmode = "Editor"
    def pressed(self):
        pass
    def onTick(self):
        if Globals.ViewMode == "Editor":
            if vec.collision(self.rect.center, 16, pg.mouse.get_pos()):
                if Globals.keys[0] == True:
                    self.pressed()

def loadTiles(savestring):
    loadtilesfunction(savestring, True)
    
def loadTilesPID(savestring):
    loadtilesfunction(savestring, False)

def loadtilesfunction(savestring, useSID):
    if useSID: ents.clearSIDs()
    loadtablesuper = []
    loadtable = []
    loadtablesub = ""
    chunklen = 0
    chunklenstring = ""
    marker = 1
    submarker = 0
    for letter in savestring:
        if marker == 1:
            marker = 2
        elif marker == 2:
            if not letter == "}":
                if letter == "[":
                    marker = 3
                    chunklen = 0
                    chunklenstring = ""
            else:
                marker = 1
                loadtablesuper.append(loadtable)
                loadtable = []
        elif marker == 3:
            if not letter == "]":
                chunklenstring = chunklenstring + letter
            else:
                marker = 4
                submarker = 0
                chunklen = int(chunklenstring)
                loadtablesub = ""
        elif marker == 4:
            submarker = submarker + 1
            loadtablesub = loadtablesub + letter
            if submarker == chunklen:
                loadtable.append(loadtablesub)
                marker = 2
    #print(loadtablesuper)
    i = ents.getCount()
    replacements = {}
    for table in loadtablesuper:
        table[1] = int(table[1])
        if table[1] in replacements:
            table[1] = replacements[table[0]]
        else:
            i = i + 1
            replacements.update({table[1]: i})
            table[1] = i
            ents.incrementEntCounter()
    for table in loadtablesuper:
        i2 = 0
        for letter in table[5]:
            if letter == "1":
                table[i2] = int(table[i2])
                if table[i2] in replacements:
                    table[i2] = replacements[table[i2]]
            elif letter == "L":
                marker = 1
                tablelist = []
                chars = ""
                i = 0
                for char in table[i2]:
                    if marker == 0:
                        if char == ">":
                            tablelist.append(int(chars))
                            chars = ""
                        else:
                            i += 1
                            chars = chars + char
                    elif marker == 1:
                        marker = 0
                tablelist.append(int(chars))
                i3 = 0
                while i3 < len(tablelist):
                    if tablelist[i3] in replacements:
                        tablelist[i3] = replacements[tablelist[i3]]
                    i3 += 1
                table[i2] = tablelist
                    
            i2 += 1
    spawnedEnts = []
    
    for table in loadtablesuper:
        ent = ents.create(table[0])
        ent.calculatePosition()
        
        if useSID:
            ent.setSID(int(table[1]))
        #else:
        #    ent.setPID(int(table[1]))
        
        spawnedEnts.append(ent)
    i = 0
    while i < len(loadtablesuper):
        ent = spawnedEnts[i]
        table = loadtablesuper[i]
        
        deref = None
        if useSID: deref = ents.SIDToEnt
        else: deref = ents.PIDToEnt
        ent.enterData(table, deref)
        
        if ent.classname == "Creature":
            ents.setCreatureControlLink(ent)
        i += 1
    
    i = 0
    while i < len(loadtablesuper):
        ent = spawnedEnts[i]
        table = loadtablesuper[i]
        
        if useSID:
            ent.setparent_no_translation(ents.SIDToEnt(int(table[6])))
        else:
            ent.setparent_no_translation(ents.PIDToEnt(int(table[6])))
        
        i += 1

def LoadGame():
    print("Loading...")
    ents.deleteAll()
    
    f = open(os.path.join(Globals.data_dir, "savefile.txt"), "r")
    loadTiles(f.read())
    f.close()
    
    ents.GameTick = 0
    print("Loaded")


    
def formatTiles(table, SIDmode):
    savetable = ents.getAllInTable(table)
    print(savetable)
    savestring = ""
    for table in savetable:
        if table != None:
            tablestring = ""
            for var in table:
                chunk = str(var)
                chunklen = str(len(chunk))
                tablestring = tablestring + "[" + chunklen + "]" + chunk
            savestring = savestring + "{" + tablestring + "}"
        elif not SIDmode:
            savestring = savestring + ":"
    return savestring
    
def SaveGame():
    print("Saving...")
    savestring = formatTiles(ents.get_p_entity_array(), True)
    f = open(os.path.join(Globals.data_dir, "savefile.txt"), "w")
    f.write(savestring)
    f.close()
    print("Saved.")
