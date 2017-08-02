
import player
import random

class Monster(player.Player):

    def __init__(self, game, location, name, description):
        player.Player.__init__(self, game, location)
        self.name = name
        self.description = description
        # print self.actions
    
    def get_input(self):
        # print "I am in", self.location.name
        if not self.playing:
            return ""
        player_present = [x for x in self.location.here 
                          if x.__class__ == player.Player and x.playing]
        if player_present:
            return "attack " + player_present[0].name

        if random.choice((0, 1)):
            direction  = random.choice(self.location.exits())
            # print "Moving", direction
            return "go " + direction
        else:
            return ""
            
    # actions = ['look', 'get', 'attack']
    
    def look(self, player, noun):
        return [self.name, self.description]
    
    def get(self, player, noun):
        return ["The " + self.name + " growls at you."]

    def send_results(self):
        pass

if __name__ == '__main__':
    import cave
    cave1 = cave.Cave('Empty cave')
    orc = Monster(cave1, 'orc', 'A generic dungeon monster')
    print(orc.actions)
    print(orc.update_debug())
    print(orc.find_handler('go', 'north'))
    
    input("Hit enter to continue...")
