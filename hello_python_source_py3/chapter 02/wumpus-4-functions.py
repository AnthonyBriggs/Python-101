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

def update_player_location():
    """ Change the player's location based on their input """
    print("Which cave next?")
    player_input = input(">")
    if (not player_input.isdigit() or 
        int(player_input) not in caves[player_location]):
        print(player_input + "? That's not a direction that I can see!")
        return False
    else:
        return int(player_input)


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
    new_location = update_player_location()
    if new_location != False:
        player_location = new_location
    if player_location == wumpus_location:
        print("Aargh! You got eaten by a wumpus!")
        break

