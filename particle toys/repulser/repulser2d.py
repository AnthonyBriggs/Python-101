#!/usr/bin/python

import pyglet
import math
import sys
import random
from collections import namedtuple


window = pyglet.window.Window(1024, 768) # or: fullscreen=True)
pyglet.resource.path.append('./images')
pyglet.resource.reindex()

key = pyglet.window.key

# Gravity constant - no relation to normal G
G = 15000

# Particles shouldn't go off the edge of the screen?
# OR: could attract them all towards the center
MAX_DIST = int(0.9 * min(window.height, window.width) / 2)
CENTER = (window.width / 2, window.height / 2)
center = namedtuple("Point", ['x','y'])(*CENTER)

print("MAX_DIST:", MAX_DIST)
print("CENTER:", CENTER)
print(center)


def center_anchor(img):
    """Center an image's 'anchor' in the middle of the image
        (not top left or whatever it normally is"""
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2
    # assume that images are roughly spherical
    # / by 8 : half height+width = avg length,
    # then /2 for half length = /4, then 
    # scale factor of 0.5 is another /2
    img.radius = int((img.width + img.height) / 8)

images = []
for i in range(1,4):
    image = pyglet.resource.image('asteroid%d.png' % i)
    center_anchor(image)
    images.append(image)


class Particle(pyglet.sprite.Sprite):

    def __init__(self, image, x=0, y=0, vx=0, vy=0, mass=1, batch=None):
        super(Particle, self).__init__(image, x, y, batch=batch)
        center_anchor(self.image)
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.scale = 0.5
        self.opacity = random.randint(100,255)
        
    def __str__(self):
        return "<Particle, x=%d, y=%d, vx=%d, vy=%d>" % (self.x, self.y, self.vx, self.vy)
            
    def dist_vec_to(self, target=None, x=0, y=0):
        if target:
            dx = self.x - target.x
            dy = self.y - target.y
        else:
            dx = self.x - x
            dy = self.y - y
        sqr_distance = dx**2 + dy**2
        distance = math.sqrt(sqr_distance)
        
        # try and reduce weird non-linear behaviour
        # when particles are close
        if distance < self.image.radius:
            distance = self.image.radius

        angle = math.acos(float(dx) / distance)
        if dy < 0:
            angle = 2*math.pi - angle
        return (distance, angle)

    def force_from(self, target):
        distance, angle = self.dist_vec_to(target)
        if distance:
            return ((G * target.mass) / (distance**2), angle)
        else:
            return (0, 0)
            
    def update_vel(self, dt, particles):
        # friction
        self.vx *= 0.98
        self.vy *= 0.98

        ax = 0
        ay = 0
        for particle in particles:
            if particle is self:
                continue
            force = self.force_from(particle)
            if force[0] != 0:
                force_x = force[0] * math.cos(force[1]) * dt
                force_y = force[0] * math.sin(force[1]) * dt
                ax += force_x
                ay += force_y

        # BUG: Should be divided by our mass... (?)
        self.vx += ax
        self.vy += ay
        
        # enforce max speed
        if self.vx > 50 or self.vy > 50:    # optimisation
            speed = self.vx ** 2 + self.vy ** 2
            if speed > 50 ** 2: # speed = pixels per second
                print(math.sqrt(speed))
                ratio = float(50 ** 2) / speed
                self.vx = self.vx * ratio
                self.vy = self.vy * ratio
            
    def update(self, dt):
        #self.enforce_max_speed()
        
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # use constrain and/or constrain_center for different effects
        self.constrain()
        #self.constrain_center(dt)
        
        # one jiggle per second
        if random.random() < 0.0001:  # 1 / (len(particles) * 60):
            self.jiggle()
    
    def enforce_max_speed(self):
        """This is a bit of a hack to try and work around a weird bug
        with (I think) fast moving particles on the wall of the border.
        
        UPDATE: I can see particles being speed checked doing 1500 px/sec
        at high densities, so I'm pretty sure this is right :)"""
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed > 50:   # pixels per second?
            print(speed, self.vx, self.vy, self.x, self.y)
            ratio = 50 / speed
            self.vx = self.vx * ratio
            self.vy = self.vy * ratio
            
            new_speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
            print(new_speed, self.vx, self.vy)
            print()
            
    def constrain(self):
        """Keep within a certain distance of the center of the screen.
        If too far away, then move back towards the center."""
        correction_vector = self.dist_vec_to(center)
        distance = correction_vector[0]
        if distance > MAX_DIST:
            correction_vector = self.dist_vec_to(center)
            correct_x = (distance - MAX_DIST) * math.cos(correction_vector[1])
            correct_y = (distance - MAX_DIST) * math.sin(correction_vector[1])
            self.x -= correct_x
            self.y -= correct_y
            self.vx = 0; self.vy = 0
        self.opacity = 100 + 155 * (MAX_DIST - min(distance, MAX_DIST)) / MAX_DIST

    def constrain_center(self, dt):
        """Apply a slight force towards the center of the screen,
            growing larger the further the distance."""
        center_d = self.dist_vec_to(target=center)
        
        # reduce force by some amount
        force = (-center_d[0] / 2, center_d[1])
        
        force_x = force[0] * math.cos(force[1]) * dt
        force_y = force[0] * math.sin(force[1]) * dt
        ax = force_x
        ay = force_y
        
        # BUG: Should be divided by our mass... (?)
        self.vx += ax
        self.vy += ay

    def jiggle(self):
        """Brownian motion, to try and find stable configurations."""
        #self.x += random.choice((-2, -1, -1, 0, 1, 1, 2))
        #self.y += random.choice((-2, -1, -1, 0, 1, 1, 2))
        self.x += random.choice((-1, 0, 1))
        self.y += random.choice((-1, 0, 1))
        
        
@window.event
def on_draw():
    window.clear()
    #label.draw()
    particles_batch.draw()

def update(dt):
    for particle in particles:
        particle.update_vel(dt, particles)
    
    for particle in particles:
        particle.update(0.05)
        
    for particle in particles:
        particle.collide_checked = False
        if particle.mass == 0:
            particles.remove(particle)


def make_particle(batch):
    x = int(random.random() * window.width)
    y = int(random.random() * window.height)
    vx = random.random()*6 - 3
    vy = random.random()*6 - 3
    particle = Particle(images[0], x, y, 0, 0, mass=10, batch=particles_batch)
    return particle

def add_particle():
    x = random.randint(center.x - 100, center.x + 100)
    y = random.randint(center.y - 100, center.y + 100)
    new_particle = Particle(images[0], x, y, 0, 0, mass=10, batch=particles_batch)
    particles.append(new_particle)

def del_particle():
    if particles:
        pick = random.choice(particles)
        pick.delete()   # Sprite delete from batch
        particles.remove(pick)

def distance(point1, point2):
    return math.sqrt( (point1.x - point2.x) ** 2 +
                      (point1.y - point2.y) ** 2)

def del_wall_particle():
    """delete a 'wall' particle, ie. one close to MAX_DIST from the center"""
    wall_particles = [p for p in particles
                        if distance(p, center) >= MAX_DIST - 2]
    pick = random.choice(wall_particles)
    pick.delete()
    particles.remove(pick)

def stop_wall_particles():
    """zero out the motion of wall particles. Hack to fix a weird crowding bug"""
    wall_particles = [p for p in particles
                    if distance(p, center) >= MAX_DIST - 2]
    for p in wall_particles:
        p.vx = 0; p.vy = 0
        p.ax = 0; p.ay = 0
        
particles_batch = pyglet.graphics.Batch()
particles = []
for i in range(1):
    particles.append(make_particle(particles_batch))
#for particle in particles:
#    print particle

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        if modifiers & key.MOD_SHIFT:
            for i in range(10):
                add_particle()
        else:
            add_particle()
    
    elif symbol == key.MINUS:
        del_particle()
    
    elif symbol == key.UNDERSCORE:
        for i in range(10):
            del_particle()
    
    elif symbol == key.BACKSPACE:
        del_wall_particle()
    
    elif symbol == key.S:
        stop_wall_particles()
    
    elif symbol == key.ESCAPE:
        window.close()

@window.event
def on_mouse_press(x, y, button, modifiers):
    print((x, y, button))


# Call update 60 times a second
pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()

