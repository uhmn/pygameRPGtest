import ents

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

def initialize():
    ents.initialize(GetEntityTypes)