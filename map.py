#handles functions related to displaying and moving around the map
'''Need to:
Read Maps [X]
Display Maps [X]
Move Player [X]
Interact with objects [X]
Random enemy encounters
Handle Loading zones'''
import json
import player
import fight
import save
from os import path
NORTH = 0
EAST = 1
WEST = 2
SOUTH = 3
POINTING = ['^', '>', '<', 'v']
class Map:
    #read map from txt file, store in 2d character array
    def __init__(self, mapName: str, entranceX: int, entranceY: int, direction: int):
        self.level = mapName
        self.exits, self.objs = self.getLevelInfo()
        self.map = self.loadMap()
        self.x = entranceX
        self.y = entranceY
        self.facing = direction
    #gives coordinates of the object in front of the player
    def inFrontCoords(self, facing) -> tuple:
        if facing == NORTH:
            return self.x, self.y-1
        elif facing == EAST:
            return self.x+1, self.y
        elif facing == WEST:
            return self.x-1, self.y
        else:
            return self.x, self.y+1
    #gives the character of the object in front of the player
    def inFront(self, facing):
        return self.map[self.inFrontCoords(facing)[1]][self.inFrontCoords(facing)[0]]

    def getLevelInfo(self):
        #read exits and objs from json file
        exits = []
        objs = []
        with open(path.join('temp', 'maps', self.level + '.json')) as f:
            data = json.load(f)
            for i in data['exits']:
                exits.append(i)
            for i in data['objs']:
                objs.append(i)
        return exits, objs
    def loadMap(self):
        #read map from txt file as 2d array
        map = []
        with open('maps/' + self.level + '.txt') as f:
            for line in f:
                map.append(list(line.strip()))
        return map
    def display(self):
        for i, line in enumerate(self.map):
            for j, char in enumerate(line):
                if i == self.y and j == self.x:
                    print(POINTING[self.facing], end="")
                elif ord(char) in range(0x30, 0x3A): #if char is a number, it's an object
                    kind = self.objs[int(char)]["type"]
                    if kind == "treasure":
                        print("T" if not self.objs[int(char)]["open"] else '-', end="")
                    elif kind == "sign":
                        print("I", end="")
                    elif kind == "door":
                        print("D" if not self.objs[int(char)]["open"] else ' ', end="")
                    elif kind == "monster":
                        print("M" if not self.objs[int(char)]["dead"] else ' ', end="")
                    elif kind == 'npc':
                        print("P", end="")
                else:
                    print(char, end="")
                print(end=" ") #make the map seem more square
            print()
    def dump(self):
        return {"objs": self.objs, "exits": self.exits}
    def dumpcoords(self):
        return {"map": self.level, "x": self.x, "y": self.y, "facing": self.facing}
    def checkspace(self, x, y):
        if self.map[y][x] in [chr(i) for i in range(0x30, 0x3A)]:
            if self.objs[int(self.map[y][x])]["type"] in ["door", "treasure"]:
                return self.objs[int(self.map[y][x])]["open"]
            elif self.objs[int(self.map[y][x])]["type"] == "monster":
                return self.objs[int(self.map[y][x])]["dead"]
        else:
            return self.map[y][x] != '#'
    def move(self, direction, brian: player.Player):
        self.facing = direction
        if direction == NORTH: #if heading to object, 
            if self.checkspace(self.x, self.y-1):
                self.y -= 1
            else:
                print("Something is blocking your way!")
        elif direction == EAST:
            if self.checkspace(self.x+1, self.y):
                self.x += 1
            else:
                print("Something is blocking your way!")
        elif direction == WEST:
            if self.checkspace(self.x-1, self.y):
                self.x -= 1
            else:
                print("Something is blocking your way!")
        elif direction == SOUTH:
            if self.checkspace(self.x, self.y+1):
                self.y += 1
            else:
                print("Something is blocking your way!")
        #check if player is on an exit
        if self.map[self.y][self.x] in ['<' , '>' , '^' , 'v']:
            tele = self.exits[POINTING.index(self.map[self.y][self.x])]
            self.tempsave(brian)
            self.__init__(tele["map"], tele["x"], tele["y"], self.facing)
    #interact with the object in front of the player
    def interact(self, brian: player.Player):
        if self.inFront(self.facing) in [chr(i) for i in range(0x30, 0x3A)]:
            obj = self.objs[int(self.inFront(self.facing))]
            if obj["type"] == "treasure":
                if not obj["open"]:
                    print("You found a " + obj["held"] + "!")
                    brian.addItem(obj["held"])
                    obj["open"] = True
                else:
                    print("This treasure chest is empty.")
            elif obj["type"] == "sign":
                print(obj["text"])
            elif obj["type"] == "door":
                if not obj["open"]:
                    if brian.removeItem("key"):
                        print("You opened the door!")
                        obj["open"] = True
                    else:
                        print("You need a key to unlock this door.")
                else:
                    print("This door is already open.")
            elif obj["type"] == "monster":
                if not obj["dead"]:
                    print("You found a " + obj["species"] + "!")
                    with open('monsters/' + obj["species"] + '.json') as f:
                        data = json.load(f)
                        fight.Fight(brian, fight.Enemy(data))
                    obj["dead"] = True
                else:
                    print("There's nothing here.")
            elif obj["type"] == "npc":
                print(obj["text"]) #TODO: add advanced dialogue system
        elif self.inFront(self.facing) == 'S': #save block
            #1. Ask to heal, 2. Ask to save
            if input("Heal up? (y/n) ").lower() == 'y':
                brian.hp = brian.maxhp
                print("All better!")
            if input("Save? (y/n) ").lower() == 'y':
                self.save(brian)
                print("Game saved!")
        else: #TODO: Add saving system
            print("There's nothing here.")
    def tempsave(self, brian: player.Player):
        #tempsaves performed at every loading zone
        temp = save.Save("", True)
        themap = self.dump()
        temp.savefile(path.join("maps",self.level+".json"), themap)

    def save(self, brian: player.Player):
        #saves performed at save blocks
        safe = save.Save(brian.name)
        temp = save.Save("", True)
        temp.copy(safe)
        play = brian.dump()
        play["new"] = False
        play["coords"] = self.dumpcoords()
        safe.savefile("player.json", play)
        themap = self.dump()
        safe.savefile(path.join("maps",self.level+".json"), themap)
