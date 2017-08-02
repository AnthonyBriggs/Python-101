#!/usr/bin/python

import pyglet

window = pyglet.window.Window(fullscreen=True)

pyglet.resource.path.append('./images')
pyglet.resource.reindex()

def center_anchor(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2
    
planet_image = pyglet.resource.image('mars.png')
center_anchor(planet_image)

class Planet(pyglet.sprite.Sprite):
    def __init__(self, image, x=0, y=0, batch=None):
        super(Planet, self).__init__(image, x, y, batch=batch)
        self.x = x
        self.y = y
		
center_x = int(window.width/2)
center_y = int(window.height/2)
planet = Planet(planet_image, center_x, center_y, None)

@window.event
def on_draw():
    window.clear()
    planet.draw()
	
pyglet.app.run()
