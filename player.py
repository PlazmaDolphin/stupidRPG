import fight
class Player:  #replace header by loading from saves
    def __init__(self, name, data):
        self.name = name
        self.lvl = data["level"]
        self.maxhp = fight.gethp(data["maxhp"], self.lvl)
        self.hp = self.maxhp
        self.pow = fight.getstat(data["pow"], self.lvl)
        self.defense = fight.getstat(data["def"], self.lvl)
        self.xp = data["xp"]
        self.monies = data["monies"]
        self.weapon = data["weapon"]
        self.inventory = list()
        self.defending = False
    def attack(self, foe):
        dmg = fight.damage(self.lvl, self.pow, self.weapon["pow"], foe.defense, self.weapon["acc"])
        foe.hp -= dmg
        return dmg
    def addItem(self, item):
        self.inventory.append(item)
    def removeItem(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        else:
            return False
    def dump(self):
        return {"name": self.name, "level": self.lvl, "maxhp": self.maxhp, "pow": self.pow, "def": self.defense, "xp": self.xp, "monies": self.monies, "weapon": self.weapon}