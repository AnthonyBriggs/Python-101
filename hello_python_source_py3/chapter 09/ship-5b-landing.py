#!/usr/bin/python

import pyglet
from pyglet.gl import *
from pyglet.window import key
import math

window = pyglet.window.Window(fullscreen=True)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

pyglet.resource.path.append('./images')
pyglet.resource.reindex()

def center_anchor(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

planet_image = pyglet.resource.image('mars.png')
center_anchor(planet_image)
ship_image = pyglet.resource.image('ship.png')
center_anchor(ship_image)
ship_image_on = pyglet.resource.image('ship_on.png')
center_anchor(ship_image_on)


def wrap(value, width):
    while value > width:
        value -= width
    while value < 0:
        value += width
    return value

radians_in_circle = math.pi * 2
def to_radians(degrees):
    return math.pi * degrees / 180.0

def to_degrees(radians):
    return (180 * radians) / math.pi

def xy_to_vec(x, y):
    """distance and angle from (0,0) to (x,y)"""
    distance = math.sqrt(x**2 + y**2)
    if distance == 0:
        return (0,0)
    angle = math.acos(float(x) / distance)
    if y < 0:
        angle = 2*math.pi - angle
    return (distance, angle)

def vec_to_xy(distance, angle):
    x = distance * math.cos(angle)
    y = distance * math.sin(angle)
    return (x,y)
    
def pyglet_to_math(degrees):
    x, y = vec_to_xy(1, to_radians(degrees))
    x = -x
    return xy_to_vec(x,y)[1]
    
def math_to_pyglet(radians):
    x, y = vec_to_xy(1, radians)
    x = -x
    return to_degrees(xy_to_vec(x,y)[1])
    
def degree_angle_diff(angle1, angle2):
    # assumes degrees
    diff = abs(wrap(angle1, 360.) - wrap(angle2, 360.))
    if diff > 180:
        diff = 360.0 - diff
    return diff

class Planet(pyglet.sprite.Sprite):
    def __init__(self, image, x=0, y=0, batch=None):
        super(Planet, self).__init__(image, x, y, batch=batch)
        self.x = x
        self.y = y
        self.mass = 5000000  # experiment!
        self.radius = (self.image.height + self.image.width) / 4
        
    # Planet pulls ship in with gravity
    def dist_vec_to(self, target):
        dx = self.x - target.x
        dy = self.y - target.y
        return xy_to_vec(dx, dy)
        
    def force_on(self, target):
        G = 1 # experiment!
        distance, angle = self.dist_vec_to(target)
        return ((G * self.mass) / (distance**2), angle)
        
    def update(self, dt):
        # Check collisions
        distance, angle = self.dist_vec_to(ship)
        #print "**", distance, '\t', ship.radius, self.radius
        if distance <= ship.radius + self.radius:
            if not ship.landed:
                velocity, ship_angle = xy_to_vec(ship.dx, ship.dy)
                if velocity > ship.max_speed:
                    ship.reset()
                    ship.alive = False
                elif degree_angle_diff(ship.rotation, math_to_pyglet(angle)) > 30:
                    ship.reset()
                    ship.alive = False
                else:
                    ship.dx = 0
                    ship.dy = 0
                    ship.landed = True
                    print("Landed v2! ship angle = %s (%s), actual angle = %s" % (to_degrees(ship_angle), ship.rotation, to_degrees(angle)))
        else:
            ship.landed = False
            
        if not ship.landed:
            # Gravity!
            force, angle = self.force_on(ship)
            force_x, force_y = vec_to_xy(force * dt, angle)
            ship.dx += force_x
            ship.dy += force_y

        
class Ship(pyglet.sprite.Sprite, key.KeyStateHandler):
    def __init__(self, image, x=0, y=0, dx=0, dy=0, rotv=0, batch=None):
        super(Ship, self).__init__(image, x, y, batch=batch)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rotation = rotv
        self.alive = True
        self.landed = False
        self.radius = self.image.width / 2
        
        self.thrust = 150.0
        self.rot_spd = 100.0
        self.max_speed = 100

    def reset(self):
        ship.life_timer = 2.0  # seconds until respawn
        self.x = center_x + 300; self.y = center_y
        self.dx = 0; self.dy = 150
        self.rotation = -90
                
    def update(self, dt):
        self.image = ship_image
        
        if not self.alive:
            # print "Dead! Respawn in %s" % self.life_timer
            self.life_timer -= dt
            if self.life_timer > 0:
                return
            else:
                self.reset()
                self.alive = True
                
        # Update rotation
        if not self.landed:
            if self[key.LEFT]:
                self.rotation -= self.rot_spd * dt
            if self[key.RIGHT]:
                self.rotation += self.rot_spd * dt
            self.rotation = wrap(self.rotation, 360.)
        
        # Get x/y components of orientation
        rotation_x = math.cos(to_radians(self.rotation))
        rotation_y = math.sin(to_radians(-self.rotation))

        # Update velocity
        if self[key.UP]:
            self.image = ship_image_on
            self.dx += self.thrust * rotation_x * dt
            self.dy += self.thrust * rotation_y * dt
        
        self.x += self.dx * dt
        self.y += self.dy * dt
    
        self.x = wrap(self.x, window.width)
        self.y = wrap(self.y, window.height)
        
        self.velocity, vel_angle = xy_to_vec(ship.dx, ship.dy)
        speedometer.text = "Speed: %.02f" % self.velocity
        distance, angle = planet.dist_vec_to(self)
        speedometer.text += " (rot: %.02f, angle: %.02f)" % (self.rotation, math_to_pyglet(angle))

        if self.velocity < self.max_speed * 0.8:
            speedometer.color = (0, 255, 0, 255)
        elif self.velocity < self.max_speed:
            speedometer.color = (255, 255, 0, 255)
        else:
            speedometer.color = (255, 0, 0, 255)
        
center_x = int(window.width/2)
center_y = int(window.height/2)

planet = Planet(planet_image, center_x, center_y)
ship = Ship(ship_image)
ship.reset()

speedometer = pyglet.text.Label('Speed: 0',
                 font_name='Arial',
                 font_size=36,
                 x=10, y=10,
                 anchor_x='left', anchor_y='bottom')


@window.event
def on_draw():
    window.clear()
    planet.draw()
    speedometer.draw()
    if ship.alive:
        ship.draw()

# Call update 60 times a second
def update(dt):
    planet.update(dt)
    ship.update(dt)

window.push_handlers(ship)
pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
