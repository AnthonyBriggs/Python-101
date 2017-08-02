#!/usr/bin/python

import pyglet
from pyglet.gl import *
from pyglet.window import key
import math

window = pyglet.window.Window(fullscreen=True)

pyglet.resource.path.append('./images')
pyglet.resource.reindex()

def center_anchor(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

def wrap(value, width):
    if width == 0:
        return 0
    if value > width:
        value -= width
    if value < 0:
        value += width
    return value

radians_in_circle = math.pi * 2
def to_radians(degrees):
    return math.pi * degrees / 180.0

planet_image = pyglet.resource.image('mars.png')
center_anchor(planet_image)
ship_image = pyglet.resource.image('ship.png')
center_anchor(ship_image)
ship_image_on = pyglet.resource.image('ship_on.png')
center_anchor(ship_image_on)

class Planet(pyglet.sprite.Sprite):
    def __init__(self, image, x=0, y=0, batch=None):
        super(Planet, self).__init__(image, x, y, batch=batch)
        self.x = x
        self.y = y
        
    def update(self, dt):
        pass

        
class Ship(pyglet.sprite.Sprite, key.KeyStateHandler):
    def __init__(self, image, x=0, y=0, dx=0, dy=0, rotv=0, batch=None):
        super(Ship, self).__init__(image, x, y, batch=batch)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rotation = rotv
        self.thrust = 200.0
        self.rot_spd = 100.0
        self.mass = 100.0
        
    def update(self, dt):
        # Update rotation
        if self[key.LEFT]:
            self.rotation -= self.rot_spd * dt
        if self[key.RIGHT]:
            self.rotation += self.rot_spd * dt
        self.rotation = wrap(self.rotation, 360.)
        
        # Update velocity
        if self[key.UP]:
            # Get x/y components of orientation
            rotation_x = math.cos(to_radians(self.rotation))
            rotation_y = math.sin(to_radians(-self.rotation))
            self.dx += self.thrust * rotation_x * dt
            self.dy += self.thrust * rotation_y * dt
        
        self.x += self.dx * dt
        self.y += self.dy * dt
    
        self.x = wrap(self.x, window.width)
        self.y = wrap(self.y, window.height)

center_x = int(window.width/2)
center_y = int(window.height/2)

planet = Planet(planet_image, center_x, center_y)
ship = Ship(ship_image, center_x + 300, center_y, 0, 150, -90)

@window.event
def on_draw():
    window.clear()
    planet.draw()
    ship.draw()

# Call update 60 times a second
def update(dt):
    ship.update(dt)
    planet.update(dt)

window.push_handlers(ship)
pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
