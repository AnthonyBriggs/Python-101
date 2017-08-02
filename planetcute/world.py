#!/usr/bin/python

import sys, os
import random

import pyglet
from pyglet.window import key


TILE_WIDTH = 100 // 2
#TILE_HEIGHT = 170.0 / 2
TILE_HEIGHT = 42

def center_anchor(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

def load_images(file_path='images'):
    pyglet.resource.path.append(file_path)
    pyglet.resource.reindex()
    images = {}
    for filename in os.listdir(file_path):
        print("Loading image", filename)
        image = pyglet.resource.image(filename)
        image.name = filename
        #center_anchor(image)
        images[filename] = image
    return images


class Tile(pyglet.sprite.Sprite):
    def __init__(self, x, y, image, batch=None, group=None):
        super(Tile, self).__init__(image, x, y, batch=batch, group=group)
        center_anchor(self.image)
        self.x = x
        self.y = y
        self.scale = TILE_WIDTH / float(self.image.width)
        self.rotation = 0

    def update(self, dt):
        pass
    
    def is_water(self):
        return 'water' in self.image.name.lower()

class Map(object):
    def __init__(self, width, height, terrains, batch=None):
        self.blocks = {}
        self.height = height
        self.width = width
        skew = 0
        self.border_x = window.width % TILE_WIDTH + TILE_WIDTH*2
        self.border_y = window.height % TILE_HEIGHT + TILE_HEIGHT

        self.batch = batch
        self.group = pyglet.graphics.OrderedGroup(100)
        for y in range(self.height):
            ygroup = pyglet.graphics.OrderedGroup(
                         order=self.height-y, 
                         parent=self.group)
            for x in range(self.width):
                self.blocks[(x,y)] = Tile(
                      self.get_xcoord(x) + y*skew, 
                      self.get_ycoord(y), 
                      random.choice(terrains), 
                      batch=self.batch,
                      group=ygroup)

    def draw(self):
        self.batch.draw()

    def update(self, dt):
        pass

    def get_xcoord(self, x_pos):
        return self.border_x + TILE_WIDTH * x_pos

    def get_ycoord(self, y_pos):
        return self.border_y + TILE_HEIGHT * y_pos


class Girl(pyglet.sprite.Sprite, key.KeyStateHandler):
    def __init__(self, x, y, image, batch=None):
        super(Girl, self).__init__(image, x, y, batch=batch)
        center_anchor(self.image)
        self.x_pos = x
        self.y_pos = y
        self.scale = TILE_WIDTH / float(self.image.width)
        self.update_pos()
        self.tile_change_index = 0
        
    def on_key_press(self, symbol, modifiers):
        #print modifiers
        if symbol == key.LEFT:
            move = (-1, 0)
        elif symbol == key.RIGHT:
            move = (1,0)
        elif symbol == key.UP:
            move = (0,1)
        elif symbol == key.DOWN:
            move = (0,-1)
        elif symbol == key.SPACE:
            move = (0,0)
            self.tile_change_index += 1
            self.tile_change_index = self.tile_change_index % len(map_images)
        else:
            return
        
        new_pos = (self.x_pos+move[0], self.y_pos+move[1])
        if (new_pos in map.blocks and not map.blocks[new_pos].is_water()):
            if modifiers & key.MOD_SHIFT:
                # shift == trying to change current block
                block = map.blocks[(self.x_pos, self.y_pos)]
                block.image = dashboard.image
            # move
            self.x_pos, self.y_pos = new_pos
            self.update_pos()
            
    def update_pos(self):
        self.x = map.get_xcoord(self.x_pos)
        self.y = map.get_ycoord(self.y_pos) + 25

        
class Dashboard(pyglet.sprite.Sprite):
    def __init__(self, x, y, image, batch=None, group=None):
        super(Dashboard, self).__init__(image, x, y, batch=batch, group=group)
        center_anchor(self.image)
        self.x = x
        self.y = y
        self.scale = TILE_WIDTH / float(self.image.width)

    def update(self, dt):
        self.image = map_images[girl.tile_change_index]


window = pyglet.window.Window(fullscreen=True)
images = load_images()
print("Images loaded:", images)

map_images = [images[n+'.png'] for n in 'dirt water stone grass wood'.split()]
map_batch = pyglet.graphics.Batch()
map = Map(window.width//TILE_WIDTH - 2, 
          window.height//TILE_HEIGHT - 1,
          map_images,
          batch=map_batch)

girl = Girl(0, 0, images['pink_girl.png'])
window.push_handlers(girl)
dashboard = Dashboard(TILE_WIDTH//2, window.height-TILE_HEIGHT, map_images[0])

@window.event
def on_mouse_press(x, y, button, modifiers):
    print("Mouse clicked at (%s, %s) -> %s, %s" % (x, y, button, modifiers))
    
    
@window.event
def on_draw():
    window.clear()
    map_batch.draw()
    girl.draw()
    dashboard.draw()

#@window.event
#def on_key_press(symbol, modifiers):
#    print symbol, pyglet.window.key.LEFT, pyglet.window.key.SPACE, pyglet.window.key.RIGHT
    
def update(dt):
    map.update(dt)
    #girl.update(dt)
    dashboard.update(dt)
    #print "Framerate: %.02f" % (1.0/dt)

# Call update 60 times a second
pyglet.clock.schedule_interval(update, 1/30.0)
pyglet.app.run()
