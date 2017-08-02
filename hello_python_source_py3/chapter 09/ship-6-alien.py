#!/usr/bin/python

import pyglet
from pyglet.gl import *
from pyglet.window import key
import math
import random

window = pyglet.window.Window(fullscreen=True)

pyglet.resource.path.append('./images')
pyglet.resource.reindex()

center_x = int(window.width/2)
center_y = int(window.height/2)


def center_anchor(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

def wrap(value, width):
    if width == 0:
        return 0
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

def make_vec(xxx_todo_changeme, xxx_todo_changeme1):
    """distance and angle from (x1,y1) to (x2,y2)"""
    (x1, y1) = xxx_todo_changeme
    (x2, y2) = xxx_todo_changeme1
    dx = x1 - x2
    dy = y1 - y2
    distance = math.sqrt(dx**2 + dy**2)
    if distance == 0:
        return (0,0)
    angle = math.acos(float(dx) / distance)
    if dy < 0:
        angle = 2*math.pi - angle
    return (distance, angle)

def vec_to_xy(distance, angle):
    x = distance * math.cos(angle)
    y = distance * math.sin(angle)
    return (x,y)

def dist_vec_to(source, target):
    return make_vec(
        (source.x, source.y),
        (target.x, target.y))

def degree_angle_diff(angle1, angle2):
    # assumes degrees
    diff = wrap(angle1 - angle2, 360.)
    if diff > 180:
        diff = 360.0 - diff
    return diff

planet_image = pyglet.resource.image('mars.png')
center_anchor(planet_image)
ship_image = pyglet.resource.image('ship.png')
center_anchor(ship_image)
ship_image_on = pyglet.resource.image('ship_on.png')
center_anchor(ship_image_on)
bullet_image = pyglet.resource.image('bullet.png')
center_anchor(bullet_image)
alien_image = pyglet.resource.image('alien.png')
center_anchor(alien_image)

class Planet(pyglet.sprite.Sprite):
    def __init__(self, image, x=0, y=0, batch=None):
        super(Planet, self).__init__(image, x, y, batch=batch)
        self.x = x
        self.y = y
        self.mass = 5000000  # experiment!
        self.scale = 1.0
        self.radius = self.scale * (self.image.height + self.image.width) / 4
        
    def force_on(self, target):
        G = 1 # experiment!
        distance, angle = dist_vec_to(self, target)
        return ((G * self.mass) / (distance**2), angle)
        
    def update(self, dt):
        # Check collisions
        distance, angle = dist_vec_to(self, ship)
        if distance <= ship.radius + self.radius:
            ship.reset()
            ship.alive = False
 
        # Gravity!
        force, angle = self.force_on(ship)
        force_x = force * math.cos(angle) * dt
        force_y = force * math.sin(angle) * dt
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
        self.thrust = 150.0
        self.rot_spd = 100.0
        self.alive = True
        self.radius = self.image.width / 2
        self.max_speed = 100
        self.shot_timer = 0.2
        self.reload_timer = self.shot_timer
        self.bullets = []
        self.score = 0
        
    def reset(self):
        ship.life_timer = 2.0  # seconds until respawn
        self.x = center_x + 300; self.y = center_y
        self.dx = 0; self.dy = 150
        self.rotation = -90
                
    def update(self, dt):
        self.image = ship_image
        score.text = "Score: %d" % self.score
        
        if not self.alive:
            #print "Dead! Respawn in %s" % self.life_timer
            self.life_timer -= dt
            if self.life_timer > 0:
                return
            else:
                self.reset()
                self.score -= 100
                self.alive = True
                
        # Update rotation
        if self[key.LEFT]:
            self.rotation -= self.rot_spd * dt
        if self[key.RIGHT]:
            self.rotation += self.rot_spd * dt
        self.rotation = wrap(self.rotation, 360.)
        
        # Get x/y components of orientation
        # Pyglet and python math angles don't correspond, but reversing the x axis fixes that
        rotation_x = math.cos(to_radians(self.rotation))
        rotation_y = math.sin(to_radians(-self.rotation))

        # Update velocity
        if self[key.UP]:
            self.image = ship_image_on
            self.dx += self.thrust * rotation_x * dt
            self.dy += self.thrust * rotation_y * dt
        
        # Shoot bullets
        if self.reload_timer > 0:
            self.reload_timer -= dt
        if self[key.SPACE]:
            if self.reload_timer <= 0:
                self.bullets.append(Bullet(self.x, self.y, rotation_x*500+self.dx, rotation_y*500+self.dy, bullets))
                self.reload_timer = self.shot_timer
        
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.x = wrap(self.x, window.width)
        self.y = wrap(self.y, window.height)
        


class Bullet(pyglet.sprite.Sprite):

    def __init__(self, x=0, y=0, dx=0, dy=0, batch=None):
        super(Bullet, self).__init__(bullet_image, x, y, batch=batch)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = self.image.width / 2
        self.timer = 1.5
        
    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.x = wrap(self.x, window.width)
        self.y = wrap(self.y, window.height)
        
        self.timer -= dt
        # collide with planet, or remove after 5 seconds
        distance, angle = dist_vec_to(planet, self)
        if distance <= planet.radius or self.timer < 0:
            ship.bullets.remove(self)
            return
            
        # check collision with Alien
        dist, angle = dist_vec_to(self, alien)
        if dist < alien.radius:
            # hit alien
            alien.reset()
            alien.alive = False
            ship.bullets.remove(self)
            ship.score += 100
            return
            
class Alien(pyglet.sprite.Sprite):

    def __init__(self, image, x=0, y=0, dx=0, dy=0, batch=None):
        super(Alien, self).__init__(image, x, y, batch=batch)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = self.image.width / 2
        self.life_timer = 2.0
        self.accel_spd = 200.0
        self.max_spd = 400.0
        self.alive = True
        self.AI = "FTANG!"
        
    def reset(self):
        self.alive = True
        self.life_timer = 2.0  # seconds until respawn
        self.x = random.random() * window.width
        self.y = random.random() * window.height
        self.dx = random.random() * (self.max_spd/2)
        self.dy = random.random() * (self.max_spd/2)
        
    def update(self, dt):
        if not self.alive:
            self.life_timer -= dt
            if self.life_timer > 0:
                return
            else:
                self.reset()
                
        # movement - random acceleration
        if random.random() < 0.2:
            accel_dir = random.random() * math.pi*2
            accel_amt = random.random() * self.accel_spd
            accel_x, accel_y = vec_to_xy(accel_amt, accel_dir)
            self.dx += accel_x
            self.dy += accel_y
        
        # limit the alien's speed to max_spd
        self.dx = min(self.dx, self.max_spd)
        self.dx = max(self.dx, -self.max_spd)
        self.dy = min(self.dy, self.max_spd)
        self.dy = max(self.dy, -self.max_spd)
                
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.x = wrap(self.x, window.width)
        self.y = wrap(self.y, window.height)
        
        # check collisions with the player
        player_dist, player_angle = dist_vec_to(self, ship)
        if player_dist < (ship.radius + self.radius) * 0.75:
            # BANG! got the player
            self.reset()
            self.alive = False
            ship.reset()
            ship.alive = False
                
        # take potshots at the player
        
        # Ship is not affected by gravity, doesn't hit the planet
        # TODO: lead the target, ie. calculate where the player is going to be and shoot there
        
planet = Planet(planet_image, center_x, center_y)

bullets = pyglet.graphics.Batch()
ship = Ship(ship_image)
ship.reset()

alien = Alien(alien_image)
alien.reset()

score = pyglet.text.Label('Speed: 0',
                 font_name='Arial',
                 font_size=36,
                 x=10, y=10,
                 anchor_x='left', anchor_y='bottom')
score.color = (255, 255, 255, 255)

@window.event
def on_draw():
    window.clear()
    planet.draw()
    if alien.alive:
        alien.draw()
    bullets.draw()
    if ship.alive:
        ship.draw()
    score.draw()

# Call update 60 times a second
def update(dt):
    planet.update(dt)
    alien.update(dt)
    for bullet in ship.bullets:
        bullet.update(dt)
    ship.update(dt)

window.push_handlers(ship)
pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
