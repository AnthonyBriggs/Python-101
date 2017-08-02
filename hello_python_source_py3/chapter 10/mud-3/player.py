
import random
import shlex

help_text = """
------------------------
Welcome to Anthony's MUD
------------------------

This text is intended to help you play the game, such as it is right now.
Most of the usual MUD-type commands should work, including:

name:           set your name
describe:       describe yourself
n,s,e,w:        move around!
look:           look at things!
say:            you can say things
shout:          you can shout stuff so that everyone can hear it.
get/drop/inv:   you can pick stuff up. There are two items in the game -
                whoever has the coin is the current winner.
attack:         you can attack pretty much any other mobile in the game. Watch
                out for the orc though, or anyone carrying a sword.

If there are any major bugs, let me know at anthony.briggs@gmail.com.

""".split('\n')

class Player(object):
    def __init__(self, game, location):
        self.game = game
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
        self.angry_list = []

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
       
    def find_handler(self, verb, noun):
        if verb == 'name':
            verb = 'name_'
        if verb == "'":
            verb = 'say'

        if noun in ['me', 'self']:
            return getattr(self, verb, None)
        
        elif noun and verb not in self.no_noun_verbs:
            # Try and find the object
            object = [x for x in self.location.here + self.inventory
                      if x is not self and
                         x.name == noun and
                         verb in x.actions]
            if len(object) > 0:
                return getattr(object[0], verb)
            else:
                return False

        # if that fails, look in location and self
        if verb.lower() in self.location.actions:
            return getattr(self.location, verb)
        elif verb.lower() in self.actions:
            return getattr(self, verb)

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
        elif handler is False:
            return ["I can't see the "+noun+"!"]
        if '__call__' not in dir(handler):
            return handler
        return handler(self, noun)

    def update(self):
        self.result = self.process_input(self.input)
        
        # if we're not doing anything important, see if we can attack something on our angry_list
        if (self.playing and
            self.input == "" and
            self.angry_list):
            bad_guys = [x for x in self.location.here
                        if 'attack' in dir(x) and x.name in self.angry_list]
            if bad_guys:
                bad_guy = random.choice(bad_guys)
                self.events += bad_guy.do_attack(self)

    def die(self):
        self.playing = False
        self.input = ""
        self.name = "dead " + self.name
        self.angry_list = []

        # drop all our stuff
        for item in self.inventory:
            self.location.here.append(item)
            item.location = self.location
        self.inventory = []
        
        self.events.append("You have died! Better luck next time!")
        # self.connection.transport.loseConnection()

    actions = ['quit', 'inv', 'get', 'drop', 'attack',
               'name_', 'describe', 'look', 'help', 'say', 'shout', 'stop']
    no_noun_verbs = ['quit', 'inv', 'name_', 'describe', 'help', 'say', 'shout', 'go']

    def help(self, player, noun):
        return help_text
            
    def inv(self, player, noun):
        result = ["You have:"]
        if self.inventory:
            result += [x.name for x in self.inventory]
        else:
            result += ["nothing!"]
        return result
        
    def quit(self, player, noun):
        self.playing = False
        self.die()
        return ["bye bye!"]
    
    def get(self, player, noun):
        return [noun + "? I can't see that here."]

    def drop(self, player, noun):
        return [noun + "? I don't have that!"]

    def name_(self, player, noun):
        self.name = noun
        return ["You changed your name to '%s'" % self.name]

    def describe(self, player, noun):
        self.description = noun
        return ["You changed your description to '%s'" % self.description]

    def look(self, player, noun):
        return ["You see %s." % self.name, self.description]

    def say(self, player, noun):
        for object in self.location.here:
            if ('events' in dir(object) and
                object != self):
                object.events.append(self.name + " says: " + noun)
        return ["You say: " + noun]

    def shout(self, player, noun):
        noun = noun.upper()
        for location in self.game.caves:
            for object in location.here:
                if ('events' in dir(object) and
                    object != self):
                    object.events.append(self.name + " shouts: " + noun)
        return ["You shout: " + noun]
                
    
    def stop(self, player, noun):
        self.angry_list = [x for x in self.angry_list if x.name != noun]
        return ["Stopped attacking " + noun]

    def attack(self, player, noun):
        player.angry_list.append(self.name)
        self.angry_list.append(player.name)
        result = ["You attack the " + self.name]
        result += self.do_attack(player)
        return result

    def do_attack(self, player):
        """Called when <player> is attacking us (self)"""
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
        

