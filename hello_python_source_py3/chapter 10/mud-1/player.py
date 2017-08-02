
import random
import shlex

class Player(object):
    def __init__(self, location):
        self.name = "Player"
        self.description = "The Player"
        self.location = location
        self.location.here.append(self)
        self.playing = True
        self.hit_points = 3
        self.inventory = []
        self.events = []
        self.input_list = []
        self.result = []

    def get_input(self):
        #return raw_input(self.name+">")
        if self.input_list:
            return self.input_list.pop()
        else:
            return ''
    
    def send_results(self):
        for line in self.result:
            self.connection.msg_me(line)
        for line in self.events:
            self.connection.msg_me(line)

    def inv(self, player, noun):
        result = ["You have:"]
        if self.inventory:
            result += [x.name for x in self.inventory]
        else:
            result += ["nothing!"]
        return result
        
    def quit(self, player, noun):
        self.playing = False
        return ["bye bye!"]
        
    actions = ['quit', 'inv', 'get', 'drop', 'attack']
    
    def get(self, player, noun):
        return [noun + "? I can't see that here."]

    def drop(self, player, noun):
        return [noun + "? I don't have that!"]
        
    def find_handler(self, verb, noun):
        # Try and find the object
        if noun != "":
            object = [x for x in self.location.here + self.inventory
                      if x is not self and
                         x.name == noun and
                         verb in x.actions]
            if len(object) > 0:
                return getattr(object[0], verb)
                            
        # if that fails, look in location and self
        if verb.lower() in self.actions:
            return getattr(self, verb)
        elif verb.lower() in self.location.actions:
            return getattr(self.location, verb)

    def process_input(self, input):
        # print str(self) + " executing :" + input
        try:
            parts = shlex.split(input)
        except ValueError:
            parts = input.split()
        if len(parts) == 0:
            return []
        if len(parts) == 1:
            parts.append("")    # blank noun
        verb = parts[0]
        noun = ' '.join(parts[1:])
        
        handler = self.find_handler(verb, noun)
        if handler is None:
            return [input+"? I don't know how to do that!"]
        if '__call__' not in dir(handler):
            return handler
        return handler(self, noun)

    def update(self):
        self.result = self.process_input(self.input)
                
    def attack(self, player, noun):
        hit_chance = 2
        has_sword = [i for i in player.inventory 
                     if i.name == 'sword']
        if has_sword:
            hit_chance += 2
        roll = random.choice([1,2,3,4,5,6])
        if roll > hit_chance:
            self.events.append("The " + 
                player.name + " misses you!")
            return ["You miss the " + self.name]

        self.hit_points -= 1
        if self.hit_points <= 0:
            return_value = ["You kill the " + self.name]
            self.events.append("The " + 
                player.name + " has killed you!")
            self.die()
            return return_value
            
        self.events.append("The " + 
            player.name + " hits you!")
        return ["You hit the " + self.name]
        
    def die(self):
        self.playing = False
        self.input = ""
        self.name = "A dead " + self.name
        # self.location.here.remove(self)
        # self.location = None
