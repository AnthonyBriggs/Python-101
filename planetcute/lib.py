import pyglet
import os
import math

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

def to_radians(degrees):
    return math.pi * degrees / 180.0


