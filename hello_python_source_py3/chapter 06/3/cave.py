
from random import choice, shuffle

class Cave(object):
    def __init__(self, name="Cave", description=""):
        self.name = name
        self.description = description
        self.tunnels = []
        self.here = []
        self.visited = False
    
    def tunnel_to(self, cave):
        """Create a two-way tunnel"""
        self.tunnels.append(cave)
        cave.tunnels.append(self)
    
    def __repr__(self):
        return "<Cave: " + self.name + ">"

    def look(self, player, noun):
        if noun == "":
            result = [self.name,
                      self.description] 
            if len(self.here) > 0:
                result += ["Items here:"]
                result += [x.name for x in self.here
                           if 'name' in dir(x)]
        else:
            result = [noun + "? I can't see that."]
        return result
        
    actions = ['look']
    

cave_names = [
    "Arched cavern",
    "Twisty passages",
    "Dripping cave",
    "Dusty crawlspace",
    "Underground lake",
    "Black pit",
    "Fallen cave",
    "Shallow pool",
    "Icy underground river",
    "Sandy hollow",
    "Old firepit",
    "Tree root cave",
    "Narrow ledge",
    "Winding steps",
    "Echoing chamber",
    "Musty cave",
    "Gloomy cave",
    "Low ceilinged cave",
    "Wumpus lair",
    "Spooky Chasm",
]

def create_caves():
    shuffle(cave_names)
    caves = [Cave(cave_names[0])]
    for name in cave_names[1:]:
        new_cave = Cave(name)
        eligible_caves = [cave for cave in caves if len(cave.tunnels) < 3]
        new_cave.tunnel_to(choice(eligible_caves))
        caves.append(new_cave)
    return caves
    
if __name__ == '__main__':
    first_cave = Cave(name="Gloomy Cave")
    second_cave = Cave(name="Sunlit Cave")
    first_cave.tunnel_to(second_cave)
    for cave in [first_cave, second_cave]:
        print(cave.name, "=>", cave.tunnels)
    print("=====")
    
    for cave in create_caves():
        print(cave.name, "=>", cave.tunnels)
        
    