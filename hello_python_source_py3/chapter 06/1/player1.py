
import shlex

class Player(object):
    def __init__(self, location):
        self.location = location
        self.location.here.append(self)
        self.playing = True
        
    def get_input(self):
        return input(">")
        
    def look(self, player, noun):
        return [self.location.name,
                self.location.description]
        
    def quit(self, player, noun):
        self.playing = False
        return ["bye bye!"]
        
    actions = ['look', 'quit']
    
    def find_handler(self, verb, noun):
        # First try and find the object
        if noun != "":
            object = [x for x in self.location.here
                      if x is not self and
                         x.name == noun and
                         verb in x.actions]
            if len(object) > 0:
                return getattr(object[0], verb)
                
        # if that fails, look in location and self
        if verb.lower() in self.actions:
            return getattr(self, verb)
        elif verb.lower() in self.location.actions:
            return getattr(self, verb)

    def process_input(self, input):
        parts = shlex.split(input)
        if len(parts) == 0:
            return []
        if len(parts) == 1:
            parts.append("")    # blank noun
        verb = parts[0]
        noun = ' '.join(parts[1:])
            
        handler = self.find_handler(verb, noun)
        if handler is None:
            return [input+"? I don't know how to do that!"]
        return handler(self, noun)

def test():
    import cave
    empty_cave = cave.Cave(
        "Empty Cave",
        "A desolate, empty cave, waiting for someone to fill it.")    
    player = Player(empty_cave)
    
    print(player.location.name)
    print(player.location.description)
    while player.playing:
        input = player.get_input()
        result = player.process_input(input)
        print("\n".join(result))


if __name__ == '__main__':
    test()