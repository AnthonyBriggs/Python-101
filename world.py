#!/usr/bin/python

"""
Random world generator.

Very slow :\
"""

import random
import sys

import pygame
from pygame.locals import *

WIDTH = 640
HEIGHT = 480
START_HEIGHT = 128

def init_world():
    world = [[START_HEIGHT for width in range(WIDTH)] for height in range(HEIGHT)]
    assert len(world) == HEIGHT
    assert len(world[0]) == WIDTH
    return world

# and access is fast
def reset_world(world):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            world[y][x] = 0
    return world


def split_horizontal(world):
    # pick two random points on left and right borders
    y1 = random.randint(0, HEIGHT-1)
    y2 = random.randint(0, HEIGHT-1)
    
    gradient = float(y2 - y1) / WIDTH
    sign = random.choice((2, 1, -1, -2))

    for x in range(WIDTH):
        cutoff = y1 + x * gradient
        for y in range(HEIGHT):
            if y >= cutoff:
                # below
                world[y][x] += sign
            else:
                # above
                world[y][x] -= sign
            world[y][x] = max(0, min(255, world[y][x]))

    #return world

def split_vertical(world):
    # pick two random points on top and bottom borders
    x1 = random.randint(0, WIDTH-1)
    x2 = random.randint(0, WIDTH-1)
    while x1 == x2:
        x2 = random.randint(0, WIDTH-1)

    gradient = float(x2 - x1) / HEIGHT
    sign = random.choice((2, 1, -1, -2))

    for y in range(HEIGHT):
        cutoff = x1 + y * gradient
        for x in range(WIDTH):
            if x >= cutoff:
                # below
                world[y][x] += sign
            else:
                # above
                world[y][x] -= sign
            world[y][x] = max(0, min(255, world[y][x]))


def iter_world(world, iterations=1):
    for i in range(iterations):
        method = random.choice((split_horizontal, split_vertical))
        print (". ", end="")
        sys.stdout.flush()
        #world = method(world)
        method(world)
    print()
    #return world


def draw_world(world, screen, water_level=32):
    screen.fill((0, 0, 0))
    for x in range(WIDTH):
        for y in range(HEIGHT):
            height = world[y][x]
            if height > water_level:
                screen.set_at((x, y), (height, height, height))
            else:
                screen.set_at((x, y), (86, 165, 236)) # steel blue
    pygame.display.flip()


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF)
    clock = pygame.time.Clock()
    world = init_world()
    quitting = False
    continuous = False
    water_level = START_HEIGHT - 2

    while 1:
        if continuous:
            iterations = 1
        else:
            iterations = 0

        # keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                quitting = True
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    continuous = not continuous
                    iterations = 1

                if event.key == K_1:
                    continuous = False
                    iterations = 1
                if event.key == K_2:
                    continuous = False
                    iterations = 10
                if event.key == K_3:
                    continuous = False
                    iterations = 50
                if event.key == K_4:
                    continuous = False
                    iterations = 100

                if event.key == K_EQUALS:
                    water_level += 1
                    print ("water level:", water_level)
                    draw_world(world, screen, water_level)

                if event.key == K_MINUS:
                    water_level -= 1
                    print ("water level:", water_level)
                    draw_world(world, screen, water_level)

                if event.key == K_ESCAPE:
                    quitting = True

        if iterations > 0:
            if not continuous:
                print (iterations, "iterations")
            sys.stdout.flush()
            iter_world(world, iterations)
            draw_world(world, screen, water_level)
            
        #clock.tick(30)
        if quitting:
            break


if __name__ == '__main__':
    main()

