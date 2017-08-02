
class Item(object):
    def __init__(self, name, description, location):
        self.name = name
        self.description = description
        self.location = location
        location.here.append(self)
        
    actions = ['look']
    
    def look(self, player, noun):
        """ Looking at the object """
        return [self.description]
        