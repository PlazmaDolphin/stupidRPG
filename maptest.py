#test if the map script works
import map
import player
MOVEMENT = ['w', 'd', 'a', 's']
start = map.Map('map1', 6, 1 , map.WEST)
brian = player.Player("Brian")
while True:
    start.display()
    dir = input()
    if dir in MOVEMENT:
        start.move(MOVEMENT.index(dir))
    elif not dir:
        start.interact(brian)