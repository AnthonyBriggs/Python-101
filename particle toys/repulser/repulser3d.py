#!/usr/bin/python

import pyglet
import math
import sys
import random

# http://partiallydisassembled.net/euclid.html
from euclid import Vector3

# TODO: calculate neighbors with Delaunay Triangulation
#   (http://en.wikipedia.org/wiki/Delaunay_triangulation)
# ie. find all spheres which touch three points which have no other
#     points in them (1 check / second should do)
#     Assume centre of sphere is coplanar w/ points
# [https://bitbucket.org/flub/delny might be ok, but needs libs]

"""
http://paulbourke.net/geometry/circlesphere/
http://www.reddit.com/r/math/comments/1gm3t1/point_with_same_distance_to_3_or_more_points_on_a/
http://ask.metafilter.com/143311/Equidistant-location-from-three-locations#2051827
http://steve.hollasch.net/cgindex/geometry/sphere4pts.html
http://www.st-andrews.ac.uk/~pl10/c/djmpark/Assets/18FF9AB0/SphereFrom3Points.pdf

>>> http://en.wikipedia.org/wiki/Circumscribed_circle
https://www.google.com.au/search?q=3d+triangle+Circumcenter
"""

window = pyglet.window.Window(1024, 768) # or fullscreen=True)
pyglet.resource.path.append('./images')
pyglet.resource.reindex()

key = pyglet.window.key

# Gravity constant - no relation to normal G
G = 100000

# Particles shouldn't go off the edge of the screen.
DEPTH = min(window.height, window.width)
MAX_DIST = int(0.45 * min(window.height, window.width))
CENTER = Vector3(window.width / 2, window.height / 2, DEPTH / 2)

def center_anchor(img):
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

    def __init__(self, image, x=0, y=0, z=0, vx=0, vy=0, vz=0, mass=1, batch=None):
        super(Particle, self).__init__(image, x, y, batch=batch)
        center_anchor(self.image)
        self.pos = Vector3(x, y, z)
        self.vel = Vector3(vx, vy, vz)
        self.mass = mass
        self.scale = 0.5
        self.opacity = 255 # random.randint(100,255)
        
    def __str__(self):
        return "<Particle #%s, pos=%s, vel=%s>" % (id(self), self.pos, self.vel)
            
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
        vector = target.pos - self.pos
        
        # try and reduce weird non-linear behaviour
        # when particles are close
        if vector.magnitude() < self.image.radius:
            vector = vector.normalized() * self.image.radius
        
        # convert direction vector to force
        return -(G * target.mass * vector.normalized() / 
                vector.magnitude() ** 2)

    def update_vel(self, dt, particles):
        # friction
        self.vel *= 0.99
        
        accel = Vector3(0, 0, 0)
        for particle in particles:
            if particle is self:
                continue
            accel += self.force_from(particle)
        
        self.vel += accel / self.mass

    def update(self, dt):
        self.pos += self.vel
        self.constrain()
        if random.random() < 1.0 / 60:
            self.jiggle()
        
        self.x = self.pos.x + CENTER.x
        self.y = self.pos.y + CENTER.y
        
    def constrain(self):
        """Keep within a certain distance of the centre of the screen.
        If too far away, then move back towards the centre."""
        center_vector = self.pos - CENTER
        if center_vector.magnitude() > MAX_DIST:
            self.pos = self.pos.normalized() * MAX_DIST
            self.vel = Vector3(0, 0, 0)     # donk! into the wall
            
        # set opacity max for close, min for far away
        depth_pct = (DEPTH + self.pos.z) / (DEPTH * 2)
        if not (0 <= depth_pct <= 100):
            print("DDD:", self.pos.z, DEPTH, depth_pct)
        depth = int(245 * depth_pct)
        self.opacity = 10 + depth

    def jiggle(self):
        """Brownian motion, to try and find stable configurations."""
        def rand_thing():
            return random.choice((-2, -1, -1, 0, 1, 1, 2))
        self.pos += Vector3(rand_thing(), rand_thing(), rand_thing())
        
        
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
    z = int(random.random() * DEPTH)
    
    vx = random.random()*6 - 3
    vy = random.random()*6 - 3
    vz = random.random()*6 - 3
    
    particle = Particle(images[0], x, y, z, vx, vy, vz, mass=10, batch=particles_batch)
    return particle

def add_particle():
    x = random.randint(CENTER[0] - 100, CENTER[0] + 100)
    y = random.randint(CENTER[1] - 100, CENTER[1] + 100)
    z = random.randint(DEPTH - 100, DEPTH + 100)
    new_particle = Particle(images[0], x, y, z, 0, 0, 0, mass=10, batch=particles_batch)
    particles.append(new_particle)

particles_batch = pyglet.graphics.Batch()
particles = []
for i in range(3):
    #particles.append(make_particle(particles_batch))
    add_particle()
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
    elif symbol == key.ESCAPE:
        window.close()


if False:
    update(0.05)
    print()
    update(0.05)
    print()
    update(0.05)
else:
    # Call update 60 times a second
    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.app.run()
