import random
class YouSuck(Exception):
    pass #if you lose, this will instantly kick you out of the game
#in the future, this will kick you to file selection after telling you how much you suck
def damage(lvl, pow, atk, defense, accuracy=100):
    #i stole this from pokemon
    if random.randint(1, 100) > accuracy:
        return 0
    dmg = (((2 * lvl / 5 + 2) * pow * atk / defense) / 50) + 2
    #now roll for crits and random
    dmg *= random.randint(85, 100) / 100
    if random.randint(1, 16) == 1:
        dmg *= 2
        print("Critical hit!")
    return dmg
def gethp(base, lvl):
    #i also stole this from pokemon
    hp = ((2 * base) * lvl / 100) + lvl + 10
    return int(hp)
def getstat(base, lvl):
    #i also stole this from pokemon
    stat = ((2 * base) * lvl / 100) + 5
    return int(stat)
def xpgain(basexp, lvl):
    #i also stole this from pokemon
    xp = basexp * lvl / 7
    return int(xp)
def getlvl(xp):
    #assume player has fast xp gain
    return int(((xp) ** (1 / 3)) * 5/4)
def tonextlvl(xp):
    current = getlvl(xp)
    threshold = (current + 1) ** 3 /5 *4
    return int(threshold - xp)
def getmonies(basemonies, lvl):
    #i have to make this one up
    monies = basemonies * lvl
    return monies * random.randrange(90, 110) / 100


class Enemy:
    def __init__(self, data, lvl=-1):
        self.name = data["name"]
        self.lvl = data["level"] if lvl == -1 else lvl
        self.maxhp = gethp(data["maxhp"], self.lvl)
        self.hp = self.maxhp
        self.pow = getstat(data["pow"], self.lvl)
        self.defense = getstat(data["def"], self.lvl)
        self.xp = data["xp"]
        self.monies = data["monies"]
        self.attacks = data["attacks"]
    def choose(self, hero):
        #make this randomized later, and add other options
        attack = random.choice(self.attacks)
        dmg = self.attack(hero, attack)
        if dmg == 0:
            print("{} missed!".format(self.name))
        else:
            print("{} used {}, dealing {} damage to {}.".format(self.name, attack["name"], dmg, hero.name))
    def attack(self, hero, move):
        if hero.defending:
            dmg = damage(self.lvl, self.pow, move["pow"], hero.defense*2, move["acc"])
        else:
            dmg = damage(self.lvl, self.pow, move["pow"], hero.defense, move["acc"])
        hero.hp -= dmg
        return dmg
'''
Fight phases:
1. Show field and actions
2. Player chooses action
3. Enemy chooses action
4. Repeat until someone dies'''
class Fight:
    def __init__(self, hero, foe: Enemy):
        self.hero = hero
        self.foe = foe
        #as soon as fight is created, start the fight
        self.fight()
    def fight(self):
        input(">>> Encountered {} <<<".format(self.foe.name))
        while not any([self.hero.hp <= 0, self.foe.hp <= 0]):
            print(self.field())
            print('''Take action!
[A] Attack
[B] Defend''')
            choice = input().upper()
            if choice not in ["A", "B"]:
                print("Invalid choice")
                continue
            if choice == "A":
                dmg = self.hero.attack(self.foe)
                print("{} hit {} for {} damage.".format(
                    self.hero.name, self.foe.name, dmg),
                      end='')
            elif choice == "B":
                self.hero.defending = True
                print(self.hero.name, "braces for it...", end='')
            input()
            self.foe.choose(self.hero)
            input()
            self.hero.defending = False
        if self.hero.hp <= 0:
            print("you suck")
            raise YouSuck
        else:  #add drops later
            exp = xpgain(self.foe.xp, self.foe.lvl)
            if self.hero.xp + exp >= tonextlvl(self.hero.xp):
                print('''{} leveled up to level {}!
HP : {} -> {}
POW: {} -> {}
DEF: {} -> {}'''.format(self.hero.name, getlvl(self.hero.xp + exp), self.hero.maxhp, gethp(self.hero.maxhp, getlvl(self.hero.xp + exp)), self.hero.pow, getstat(self.hero.pow, getlvl(self.hero.xp + exp)), self.hero.defense, getstat(self.hero.defense, getlvl(self.hero.xp + exp))))
                self.hero.xp += exp
                self.hero.lvl = getlvl(self.hero.xp)
            monies = getmonies(self.foe.monies, self.foe.lvl)
            self.hero.monies += monies
            print('''{} was defeated.
>>> YOU WON! <<<
got {} xp and {} monies.'''.format(self.foe.name, exp, monies))
        return

    def field(self):
        form = '''{0:<16} HP: {1:>3}|{2:>3}
{3:<16} HP: {4:>3}|{5:>3}'''
        return form.format(self.hero.name, self.hero.hp, self.hero.maxhp, self.foe.name, self.foe.hp,
                           self.foe.maxhp)