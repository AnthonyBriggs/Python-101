#!/usr/bin/python2.5

""" Hunt the wumpus! """

from random import choice

def create_tunnel(cave_from, cave_to):
    """ Create a tunnel between cave_from and cave_to """
    caves[cave_from].append(cave_to)
    caves[cave_to].append(cave_from)
    
def visit_cave(cave_number):
    """ Mark a cave as visited """
    visited_caves.append(cave_number)
    unvisited_caves.remove(cave_number)

def choose_cave(cave_list):
    """ Pick a cave from a list, provided
        that the cave has less than 3 tunnels."""
    cave_number = choice(cave_list)
    while len(caves[cave_number]) >= 3:
        cave_number = choice(cave_list)
    return cave_number

def setup_caves(cave_numbers):
    """ Create the starting list of caves """
    caves = []
    for i in cave_numbers:
        caves.append([])
    return caves

def link_caves():
    """ Make sure all of the caves are connected
        with two-way tunnels """
    while unvisited_caves != []:
        this_cave = choose_cave(visited_caves)
        next_cave = choose_cave(unvisited_caves)
        create_tunnel(this_cave, next_cave)
        visit_cave(next_cave)

def finish_caves():
    """ Link the rest of the caves with one-way tunnels """
    for i in cave_numbers:
        while len(caves[i]) < 3:
            passage_to = choose_cave(cave_numbers)
            caves[i].append(passage_to)

def print_caves():
    """ Print out the current cave structure """
    for number in cave_numbers:
        print(number, ":", caves[number])
    print('----------')


def print_location(player_location):
    """ Tell the player about where they are """
    print("You are in cave", player_location)
    print("From here, you can see caves:", caves[player_location])
    if wumpus_location in caves[player_location]:
        print("I smell a wumpus!")

def ask_for_cave():
    """ Ask the player to choose a cave from
    their current_location."""
    player_input = input("Which cave? ")
    if (player_input.isdigit() and
        int(player_input) in caves[player_location]):
        return int(player_input)
    else:
        print(player_input + "?")
        print("That's not a direction that I can see!")
        return False

def get_action():
    """ Find out what the player wants to do next. """
    print("What do you do next?")
    print("   m) move")
    print("   a) fire an arrow")
    action = input("> ")
    if action == "m" or action == "a":
        return action
    else:
        print(action + "?")
        print("That's not an action that I know about")
        return False

def do_movement():
    print("Moving...")
    new_location = ask_for_cave()
    if new_location == False:
        return player_location
    else:
        return new_location

def do_shooting():
    print("Firing...")
    shoot_at = ask_for_cave()
    if shoot_at == False:
        return False
        
    if shoot_at == wumpus_location:
        print("Twang ... Aargh! You shot the wumpus!")
        print("Well done, mighty wumpus hunter!")
    else:
        print("Twang ... clatter, clatter!")
        print("You wasted your arrow!")
        print("Empty handed, you begin the ")
        print("long trek back to your village...")
    return False


cave_numbers = list(range(0,20))
unvisited_caves = list(range(0,20))
visited_caves = []
visit_cave(0)

caves = setup_caves(cave_numbers)
print_caves()
link_caves()
print_caves()
finish_caves()

wumpus_location = choice(cave_numbers)
player_location = choice(cave_numbers)
while player_location == wumpus_location:
    player_location = choice(cave_numbers)
    
while 1:
    print_location(player_location)
    
    action = get_action()
    if action == False:
        continue
        
    if action == "m":
        player_location = do_movement()
        if player_location == wumpus_location:
            print("Aargh! You got eaten by a wumpus!")
            break
            
    if action == "a":
        game_over = do_shooting()
        if game_over:
            break
