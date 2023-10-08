import os
import json
def saveselect() -> str:
    print("Select a save slot:")
    end = len(os.listdir("saves"))
    for i, slot in enumerate(os.listdir("saves")):
        if os.path.isdir(os.path.join("saves", slot)):
            print("[{}]: {}".format(i, saveinfo(slot)))
    print("[{}]: New save".format(end))
    print("[{}]: Delete save".format(end+1))
    while True:
        try:
            choice = int(input())
            if choice == end:
                return newsave()
            elif choice == end+1:
                deletesave()
                out = saveselect()
                return out
            elif 0 <= choice < end:
                return os.listdir("saves")[choice]
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid choice")

def newsave() -> str:
    while True:
        name = input('''Hello warrior, and welcome to pain!
Choose your character's name >> ''')
        if name.strip() == "":
            print("That's not a name!")
        elif os.path.exists(os.path.join("saves", name)):
            print("That name is already taken!")
        else:
            break
    a = Save(name)
    a.create()
    return name

def deletesave() -> None:
    if len(os.listdir("saves")) == 0:
        print("There are no save slots to delete!")
        return
    print("Delete a save slot:")
    end = len(os.listdir("saves"))
    for i, slot in enumerate(os.listdir("saves")):
        if os.path.isdir(os.path.join("saves", slot)):
            print("[{}]: {}".format(i, saveinfo(slot)))
    while True:
        try:
            choice = int(input())
            if 0 <= choice < end:
                die = Save(os.listdir("saves")[choice])
                die.delete()
                return
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid choice")

def saveinfo(slot: str) -> str:
    with open(os.path.join("saves", slot, "player.json"), "r") as file:
        data = json.load(file)
    return format("{name}: Level {level}  {monies}G".format(**data))

class Save:
    def __init__(self, slot: str, temp=False) -> None:
        if temp and slot != "":
            self.path = os.path.join("temp", slot)
        elif temp:
            self.path = "temp"
        else:
            self.path = os.path.join("saves", slot)
        self.slot = slot
        self.temp = temp
    def savefile(self, filepath, data) -> None:
        with open(os.path.join(self.path, filepath), "w") as file:
        #this will work even if the file doesn't exist
            json.dump(data, file)
    def loadfile(self, filepath) -> dict:
        with open(os.path.join(self.path, filepath), "r") as file:
            return json.load(file)
    def create(self) -> None:
        #copy all default jsons from maps, but not monsters, into the save slot. Also include player.json
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        if not os.path.exists(os.path.join(self.path, "maps")):
            os.mkdir(os.path.join(self.path, "maps"))
        for file in (os.listdir(os.path.join("saves",self.slot,"maps")) if self.temp else os.listdir("maps")):
            if file.endswith(".json"):
                with open(os.path.join("maps", file), "r") as f:
                    self.savefile(os.path.join("maps", file), json.load(f))
        with open("player.json", "r") as f:
            self.savefile("player.json", json.load(f))
    def delete(self, path="") -> None:
        for file in os.listdir(os.path.join(self.path,path)):
            if os.path.isdir(os.path.join(self.path, file)):
                self.delete(os.path.join(path, file)) #oh yeah this is recursive
            else:
                os.remove(os.path.join(self.path, path, file))
        os.rmdir(os.path.join(self.path, path))
    def isnew(self) -> bool:
        with open(os.path.join(self.path, "player.json"), "r") as file:
            data = json.load(file)
            return data["new"]
    def copy(self, target, suffix="") -> None:
        #target is a Save object, not a string
        if not os.path.exists(os.path.join(target.path, suffix)):
            os.mkdir(os.path.join(target.path,suffix))
        for file in os.listdir(os.path.join(self.path, suffix)):
            if os.path.isdir(os.path.join(self.path, file)):
                self.copy(target, os.path.join(suffix, file))
            else:
                with open(os.path.join(self.path, suffix, file), "r") as f:
                    target.savefile(os.path.join(suffix, file), json.load(f))