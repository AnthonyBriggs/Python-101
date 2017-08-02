
class Item(object):
    def __init__(self, name, description, location):
        self.name = name
        self.description = description
        self.location = location
        location.here.append(self)
        
    actions = ['look', 'get', 'drop']
    
    def look(self, player, noun):
        """ Looking at the object """
        return [self.description]
        
    def get(self, player, noun):
        if self.location is player:
            return ["You already have the " + self.name]
        self.location.here.remove(self)
        self.location = player
        player.inventory.append(self)
        return ["You get the " + self.name]
    
    def drop(self, player, noun):
        if self not in player.inventory:
            return ["You don't have the " + self.name]
        player.inventory.remove(self)
        player.location.here.append(self)
        self.location = player.location
        return ["You drop the " + self.name]
        