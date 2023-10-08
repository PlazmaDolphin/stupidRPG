import json
from player import Player
from fight import Enemy, Fight, YouSuck
import map
from save import *
'''
Steps 1-3 roughly completed
1. Get player's info [X]
2. Encounter Enemy [X]
3. Fight Enemy [X]
4. Get XP and Monies (or die) [X]
5. Go to town
6. Fight Boss
7. Win

To add:
Inventory
Text boxes
Randomized encounters
Save System [X]
'''
MOVEMENT = ['w', 'd', 'a', 's']
name = saveselect()
save = Save(name)
temp = Save("", True)  # TODO: load from pre-existing temp
brian = Player(name, save.loadfile("player.json"))
start = None
save.copy(temp)
if save.isnew():
    print("New game, yadda yadda fill in later")
    data = save.loadfile("player.json")
    data["name"] = name  # make the name what the player chose
    save.savefile("player.json", data)
    with open("monsters/slime.json", "r") as file:
        slime = Enemy(json.load(file), 3)
    Fight(brian, slime)
    start = map.Map('map1', 6, 1, map.WEST)
else:
    coords = save.loadfile("player.json")["coords"]
    start = map.Map(coords["map"], coords["x"], coords["y"], coords["facing"])
    save.copy(temp)
while True:
    try:
        start.display()
        dir = input()
        if dir in MOVEMENT:
            start.move(MOVEMENT.index(dir), brian)
        elif not dir:
            start.interact(brian)
    except YouSuck:
        print("You died!")
        break