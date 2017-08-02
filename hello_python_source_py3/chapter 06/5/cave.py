
from random import choice, shuffle

class Cave(object):

    directions = {
        'north' : 'south',
        'east'  : 'west',
        'south' : 'north',
        'west'  : 'east',
    }
    def __init__(self, name="Cave", description=""):
        self.name = name
        self.description = description
        self.tunnels = {}
        for direction in list(self.directions.keys()):
            self.tunnels[direction] = None
        self.here = []
        self.visited = False
    
    def tunnel_to(self, direction, cave):
        """Create a two-way tunnel"""
        if direction not in self.directions:
            raise ValueError(direction + " is not a valid direction!")
        reverse_direction = self.directions[direction]
        if cave.tunnels[reverse_direction] is not None:
            raise ValueError("Cave " + str(cave) + " already has a cave to the " + reverse_direction + "!")
        self.tunnels[direction] = cave
        cave.tunnels[reverse_direction] = self
    
    def can_tunnel_to(self):
        return [v for v in list(self.tunnels.values())
                if v is None] != []
        
    def __repr__(self):
        return "<Cave: " + self.name + ">"

    def exits(self):
        return [direction for direction, cave 
                      in list(self.tunnels.items())
                      if cave is not None]
        
    def look(self, player, noun):
        if noun == "":
            result = [self.name,
                      self.description] 
            if len(self.here) > 0:
                result += ["Items here:"]
                result += [x.name for x in self.here
                           if 'name' in dir(x)]
            if len(self.exits()) >  0:
                result += ['Exits:']
                for direction in self.exits():
                    result += [direction + ": " + self.tunnels[direction].name]
            else:
                result += ['Exits:', 'none.']
        else:
            result = [noun + "? I can't see that."]
        return result
    l = look
    
    actions = ['look', 'l', 'go',
               'north', 'east', 'south', 'west',
               'n', 'e', 's', 'w']
    
    def go(self, player, noun):
        if noun not in self.directions:
            return [noun + "? I don't know that direction!"]
        if self.tunnels[noun] is None:
            return ["Can't go " + noun + " from here!"]
        self.here.remove(player)
        self.tunnels[noun].here.append(player)
        player.location = self.tunnels[noun]
        return ['You go ' + noun] + self.tunnels[noun].look(player, '')
    
    def north(self, player, noun):
        return self.go(player, 'north')
    n = north
    def east(self, player, noun):
        return self.go(player, 'east')
    e = east
    def south(self, player, noun):
        return self.go(player, 'south')
    s = south
    def west(self, player, noun):
        return self.go(player, 'west')
    w = west
    
    
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
        print(caves)
        eligible_caves = [cave for cave in caves
                          if cave.can_tunnel_to()]
        old_cave = choice(eligible_caves)
        directions = [direction for direction, cave 
                      in list(old_cave.tunnels.items())
                      if cave is None]
        direction = choice(directions)
        old_cave.tunnel_to(direction, new_cave)
        caves.append(new_cave)
    return caves
    
if __name__ == '__main__':
    #first_cave = Cave(name="Gloomy Cave")
    #second_cave = Cave(name="Sunlit Cave")
    #first_cave.tunnel_to(second_cave)
    #for cave in [first_cave, second_cave]:
    #    print cave.name, "=>", cave.tunnels
    #print "====="
    
    for cave in create_caves():
        print(cave.name, "=>", cave.tunnels)
        
