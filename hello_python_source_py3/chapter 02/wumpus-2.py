#!/usr/bin/python2.5

""" Hunt the wumpus! """

from random import choice

cave_numbers = range(0,20)
caves = []
for i in cave_numbers:
    caves.append([])
print(caves)

# create passages
# NB: one way only!
for i in cave_numbers:
    print("creating cave", i)
    for j in range(3):
        passage_to = choice(cave_numbers)
        caves[i].append(passage_to)
print(caves)

wumpus_location = choice(cave_numbers)
player_location = choice(cave_numbers)
while player_location == wumpus_location:
    player_location = choice(cave_numbers)

while 1:
    print("You are in cave", player_location)
    print("From here, you can see caves:", caves[player_location])
    if wumpus_location in caves[player_location]:
        print("I smell a wumpus!")

    print("Which cave next?")
    player_input = input(">")
    if (not player_input.isdigit() or 
        int(player_input) not in caves[player_location]):
        print(player_input + "? That's not a direction that I can see!")
        continue

    player_location = int(player_input)
    if player_location == wumpus_location:
        print("Aargh! You got eaten by a wumpus!")
        break

