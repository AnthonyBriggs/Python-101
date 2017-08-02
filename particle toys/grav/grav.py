#!/usr/bin/python

import pyglet
import math
import sys
import random

window = pyglet.window.Window(fullscreen=True)
pyglet.resource.path.append('./images')
pyglet.resource.reindex()

G = 10

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
        
class Asteroid(pyglet.sprite.Sprite):

    def __init__(self, image, x=0, y=0, vx=0, vy=0, mass=100, rotv=0, batch=None):
        super(Asteroid, self).__init__(image, x, y, batch=batch)
        center_anchor(self.image)
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.rotv = rotv
        self.mass = mass
        self.collide_checked = False
        self.scale = 0.5
    def __str__(self):
        return "<Asteroid, mass=%d, x=%d, y=%d, x_vel=%.02f, y_vel=%.02f>" % \
            (self.mass, self.x, self.y, self.vx, self.vy)
            
    def dist_vec_to(self, target):
        dx = self.x - target.x
        dy = self.y - target.y
        
        sqr_distance = dx**2 + dy**2
        distance = math.sqrt(sqr_distance)
        
        angle = math.acos(float(dx) / distance)
        if dy < 0:
            angle = 2*math.pi - angle
        return (distance, angle)
        
    def force_from(self, target):
        distance, angle = self.dist_vec_to(target)
        return (-(G * target.mass) / (distance**2), angle)
    
    def update_vel(self, dt, asteroids):
        ax = 0
        ay = 0
        for asteroid in asteroids:
            if asteroid is self:
                continue
            force = self.force_from(asteroid)
            force_x = force[0] * math.cos(force[1]) * dt
            force_y = force[0] * math.sin(force[1]) * dt
            ax += force_x
            ay += force_y

        self.vx += ax
        self.vy += ay
        
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rotation += self.rotv * dt
        if self.mass <= 200:
            self.image = images[0]
        elif self.mass <= 1000:
            self.image = images[1]
        else:
            self.image = images[2]
    
    def check_collisions(self, asteroids):
        """Asteroids will collide if they are closer than the sum of their radii"""
        for asteroid in asteroids:
            if asteroid is self or asteroid.collide_checked:
                continue
            sum_radii = self.image.radius + asteroid.image.radius
            distance, ignored = self.dist_vec_to(asteroid)
            if distance >= 0.6 * sum_radii:
                # too far - no collision
                continue
            
            # Crash! Sum the masses and average out 
            # the position and velocity (weighted by mass)
            combined_mass = self.mass + asteroid.mass
            self.x = (self.x * self.mass + asteroid.x * asteroid.mass) / combined_mass
            self.y = (self.y * self.mass + asteroid.y * asteroid.mass) / combined_mass
            self.vx = (self.vx * self.mass + asteroid.vx * asteroid.mass) / combined_mass
            self.vy = (self.vy * self.mass + asteroid.vy * asteroid.mass) / combined_mass
            self.mass = self.mass + asteroid.mass
            print("Collision! ", (self.mass, (self.x, self.y), (self.vx, self.vy)))
            asteroid.mass = 0
            asteroid.collide_checked = True
        self.collide_checked = True
        
if 0:
    label = pyglet.text.Label('distance: 0',
                          font_name='Arial',
                          font_size=16,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

@window.event
def on_draw():
    window.clear()
    #label.draw()
    asteroids_batch.draw()

def update(dt):
    for asteroid in asteroids:
        asteroid.update_vel(dt, asteroids)
        
    for asteroid in asteroids:
        asteroid.update(dt)
        
    for asteroid in asteroids:
        asteroid.check_collisions(asteroids)
        
    for asteroid in asteroids:
        asteroid.collide_checked = False
        if asteroid.mass == 0:
            asteroid.delete()
            asteroids.remove(asteroid)
            # delete from 
    if 0:
        distance, angle = asteroids[1].dist_vec_to(asteroids[0])
        force, angle = asteroids[1].force_from(asteroids[0])
        velocity = math.sqrt(asteroids[1].vx**2 + asteroids[1].vy**2)
        label.text = "dist/angle/force/vel: %s/%s/%.03f/%.03f" % (int(distance), int(angle*100), force, velocity)
    #sys.exit()
    
asteroids_batch = pyglet.graphics.Batch()

center_x = int(window.width/2)
center_y = int(window.height/2)
sun = Asteroid(images[2], center_x, center_y, 0, 0, mass=100000, rotv=3, batch=asteroids_batch)

def make_asteroid(sun, batch):
    assert sun is not None
    # evenly across screen
    #x = int(random.random() * window.width)
    #y = int(random.random() * window.height)
    
    # in middle of screen
    x = int(random.random() * (window.width / 2) + window.width / 4)
    y = int(random.random() * (window.height / 2) + window.height / 4)

    # circular setup - asteroids in circular orbit, between 0.1 and 1.0 max radius
    center = (window.width / 2, window.height / 2)
    radius = max(center[0], center[1])
    d = random.random() * radius * 0.9 + radius * 0.1
    angle = random.random() * 2.0 *math.pi
    x = center[0] + d * math.cos(angle)
    y = center[1] + d * math.sin(angle)

    rotv = int(random.random() *  20) - 10
    asteroid = Asteroid(images[0], x, y, 0, 0, mass=100, rotv=rotv, batch=asteroids_batch)
    
    # now pick a velocity giving the asteroid a rough clockwise, circular orbit
    # v = sqrt(G * M(sun) / dist, according to 
    # http://www.physicsclassroom.com/class/circles/Lesson-4/Mathematics-of-Satellite-Motion
    dist, angle = asteroid.dist_vec_to(sun)
    angle += math.pi / 2
    #spd = (0.0175 * G * sun.mass) / dist
    spd = math.sqrt( (G * sun.mass) / dist )
    asteroid.vx = spd * math.cos(angle)
    asteroid.vy = spd * math.sin(angle)
    return asteroid
    
asteroids = [sun]
for i in range(250):
    asteroids.append(make_asteroid(sun, asteroids_batch))
for asteroid in asteroids:
    print(asteroid)
    
# Call update 60 times a second
pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
