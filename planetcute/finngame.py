#!/usr/bin/python

import math
import random

import pyglet
from pyglet.window import key
from lib import center_anchor, load_images, to_radians


class Girl(pyglet.sprite.Sprite):
    def __init__(self, x, y, image, batch=None):
        super(Girl, self).__init__(image, x, y, batch=batch)
        center_anchor(self.image)
        self.x = x
        self.y = y
        self.move_to = (x,y)
        self.move_x = 0
        self.move_y = 0
        self.speed = 500
        self.beetles_whacked = 0
        self.playing = True

    def update(self, dt):
        if not self.playing:
            if self.rotation != 90:
                self.rotation = 90
                self.x += 25
                self.y -= 25
            return
        
        self.rotation = 0
        self.x -= self.move_x * dt
        self.y -= self.move_y * dt
        to_x, to_y = self.move_to
        if abs(self.x - to_x) < abs(self.move_x * dt):
            self.x = to_x
            self.move_x = 0
        if abs(self.y - to_y) < abs(self.move_y * dt):
            self.y = to_y
            self.move_y = 0
        
        for beetle in beetles:
            if beetle.whacked:
                continue
            if self.close_to(beetle.x, beetle.y):
                beetle.whack()
                self.beetles_whacked += 1
                break

    def dist_vec_to(self, to_x, to_y):
        dx = self.x - to_x
        dy = self.y - to_y        
        sqr_distance = dx**2 + dy**2
        distance = math.sqrt(sqr_distance)
        if distance == 0:
            return (0,0)
        angle = math.acos(float(dx) / distance)
        if dy < 0:
            angle = 2*math.pi - angle
        return (distance, angle)

    def set_move_to(self, x, y):
        self.move_to = (x,y)
        distance, angle = self.dist_vec_to(x,y)
        self.move_x = math.cos(angle) * self.speed
        self.move_y = math.sin(angle) * self.speed

    def close_to(self, x, y):
       return (abs(x - self.x) < self.image.width // 2 and 
               abs(y - self.y) < self.image.width // 2)


class NaughtyBeetle(pyglet.sprite.Sprite):
    def __init__(self, x, y, image, batch=None):
        super(NaughtyBeetle, self).__init__(image, x, y, batch=batch)
        center_anchor(self.image)
        self.x = x
        self.y = y
        self.move_to = (x,y)
        self.move_x = 0
        self.move_y = 0
        self.speed = 100
        self.whacked = False
        self.looting = False
        self.direction_timer = 0
        self.directions = [
            ('north', (0,1), 270),
            ('east', (1,0), 0),
            ('south', (0,-1), 90),
            ('west', (-1,0), 180),
        ]
        self.direction = random.choice(self.directions)

    def close_to(self, x, y):
       return (abs(x - self.x) < self.image.width // 2 and 
               abs(y - self.y) < self.image.width // 2)

    def whack(self):
        # whackage by player
        self.whacked = True
        self.timer = 3
        self.rotation = 180

        # create a little star here to show that we've been whacked
        stars.append(Star(self.x, self.y, star_image))
        
    def update(self, dt):
        if self.whacked:
            self.timer -= dt
            if self.timer < 0:
                beetles.remove(self)
            return

        # if we're close to the treasure, then we loot it!
        if self.close_to(treasure.x, treasure.y):
            if not self.looting:
                stars.append(Star(self.x, self.y, heart_image))
                self.looting = True
                #self.timer = 3
                treasure.open = True
                #treasure.timer = 3
            return

        # make beetles run around
        self.direction_timer -= dt
        if self.direction_timer < 0:
            # change direction
            #  should really be trying to move toward the centre/treasure...
            if self.y < treasure.y:
                if self.x < treasure.x:
                    choices = [0,1]
                else:
                    choices = [0,3]
            else:
                if self.x < treasure.x:
                    choices = [2,1]
                else:
                    choices = [2,3]
            self.direction = random.choice([self.directions[i] for i in choices])
            self.direction_timer = random.choice((0.25, 0.5, 0.5, 0.5, 1))
        
        self.x += self.direction[1][0] * self.speed * dt
        self.y += self.direction[1][1] * self.speed * dt
        self.rotation = self.direction[2]

        # turn around if we get offscreen?
        if (self.x < 0 or self.x > window.width or
            self.y < 0 or self.y > window.height):
            dir_index = self.directions.index(self.direction)
            self.direction =  self.directions[(dir_index + 2) % 4]


    def random_pos(self):
        self.x = int(window.width * random.random())
        self.y = int(window.height * random.random())


class Star(pyglet.sprite.Sprite):
    def __init__(self, x, y, image, batch=None):
        super(Star, self).__init__(image, x, y, batch=batch)
        center_anchor(self.image)
        self.x = x
        self.y = y
        #self.scale = 1
        self.timer = 1.0

    def update(self, dt):
        self.timer -= dt
        if self.timer < 0:
            stars.remove(self)
            return

        self.y += 10
        self.scale = 1 + 0.5/self.timer


class Treasure(pyglet.sprite.Sprite):
    def __init__(self, x, y, image, batch=None):
        super(Treasure, self).__init__(image, x, y, batch=batch)
        center_anchor(self.image)
        self.x = x
        self.y = y
        self.scale = 0.75
        self.open = False
        self.timer = 5

    def update(self, dt):
        if self.open:
            self.image = images['Chest Open.png']
            center_anchor(self.image)

            if [_f for _f in [(beetle.close_to(self.x, self.y) and not beetle.whacked) for beetle in beetles] if _f]:
                self.timer -= dt
            else:
                self.timer += dt

            if self.timer < 0:
                # beetles win!
                stars.append(Star(self.x, self.y, gem_image))
                self.open = False
                #for beetle in beetles:
                #    beetle.random_pos()
                girl.playing = False

            if self.timer >= 5:
                print("Closing chest!")
                self.open = False
        else:
            self.image = images['Chest Closed.png']
            self.timer = min(self.timer+dt, 5)


window = pyglet.window.Window(fullscreen=True)
center_x = int(window.width//2)
center_y = int(window.height//2)
images = load_images()

girl = Girl(center_x-100, center_y, images['Character Princess Girl.png'])
treasure = Treasure(center_x, center_y, images['Chest Closed.png'])

beetle_image = images['Beetle Centred.png']
beetles = []
stars = []
star_image = images['Star.png']
heart_image = images['Heart.png']
gem_image = images['Gem Blue.png']

def make_beetle():
    # TODO: randomly add beetles from the edge of the screen?
    beetle = NaughtyBeetle(0,0,beetle_image)
    beetle.random_pos()
    beetles.append(beetle)
make_beetle()

@window.event
def on_mouse_press(x, y, button, modifiers):
    print("Mouse clicked at (%s, %s) -> %s, %s" % (x, y, button, modifiers))
    girl.set_move_to(x,y)

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        for beetle in beetles:
            beetles.remove(beetle)
        treasure.open = False
        treasure.timer = 5
        girl.playing = True
        girl.beetles_whacked = 0

@window.event
def on_draw():
    window.clear()
    if girl.y > treasure.y:
        girl.draw()
    treasure.draw()
    for beetle in beetles:
        beetle.draw()
    if girl.y <= treasure.y:
        girl.draw()
    for star in stars:
        star.draw()

# Call update 60 times a second
def update(dt):
    #print girl.playing, girl.beetles_whacked, beetles, treasure.timer
    girl.update(dt)
    if girl.playing:
        treasure.update(dt)
        for beetle in beetles:
            beetle.update(dt)
        if len(beetles) < 1 + girl.beetles_whacked / 5:
            make_beetle()
        #print beetles, girl.beetles_whacked, 1 + girl.beetles_whacked / 5
            
    for star in stars:
        star.update(dt)
                
pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()

