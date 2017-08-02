
import player
import random

class Monster(player.Player):

    def __init__(self, location, name, description):
        player.Player.__init__(self, location)
        self.name = name
        self.description = description
        print(self.actions)
    
    def get_input(self):
        if not self.playing:
            return ""
        player_present = [x for x in self.location.here
                          if x.name == "Player"]
        if player_present:
            return "attack " + player_present[0].name
        if random.choice((0, 1)):
            return "go " + random.choice(self.location.exits())
        else:
            return ""
            
    # actions = ['look', 'get', 'attack']
    
    def look(self, player, noun):
        return [self.name, self.description]
    
    def get(self, player, noun):
        return ["The " + self.name + " growls at you."]


if __name__ == '__main__':
    import cave
    cave1 = cave.Cave('Empty cave')
    orc = Monster(cave1, 'orc', 'A generic dungeon monster')
    print(orc.actions)
    print(orc.update_debug())
    print(orc.find_handler('go', 'north'))
    
    input("Hit enter to continue...")