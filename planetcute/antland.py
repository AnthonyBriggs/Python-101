#!/usr/bin/env python

"""Old, old, old pyglet, very, very broken - needs to be converted/rewritten """

import pyglet
from pyglet.window import key

import random
import os

# used to set up GL image blending
#from pyglet.gl import *

# image helper functions

def get_image_dir():
    """ Get the image directory """
    directory = os.path.abspath(os.path.dirname(__file__))
    directory = os.path.join(directory, 'images')
    return directory

def load_image(image_file_name):
    return image.load(image_file_name)

def load_images():
    output = []
    image_dir = get_image_dir()
    for image_name in os.listdir(image_dir):
        if not image_name.endswith('.png'):
            continue
        full_path = os.path.join(image_dir, image_name)
        image = load_image(full_path)
        output.append(image)
        print("Loaded", image_name)
    return output


class GameWindow(window.Window):

    def __init__(self, *args, **kwargs):
        window.Window.__init__(self, *args, **kwargs)
        self.set_mouse_visible(True)
        # make images blend
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.init_sprites()
        self.init_vars()
        self.init_menu()
        self.mouse_pressed = 0
        self.cursor_x = 0
        self.cursor_y = 0
        
    def init_sprites(self):
        self.sprite_types = load_images()
        self.curr_sprite = 0
        self.sprites = {}

        cursor_image = load_image("Selector.png")
        self.cursor = Sprite("", image_data=cursor_image, x=100, y=100)

    def init_vars(self):
        # The sizes of the blocks in the images
        self.block_x = 100
        self.block_y = 80
        self.block_z = 40
        
        # set up the game with a menu down the left side, and the rest for blocks
        self.menu_x = 150
        self.game_x = self.width - self.menu_x
        self.game_y = self.height
        self.blocks_across = self.game_x // self.block_x
        self.blocks_down = self.game_y // self.block_y - 1
        self.coords = [[(x,y) for x in range(self.blocks_across)] for y in reversed(list(range(self.blocks_down)))]
        for coord_line in self.coords:
            print(coord_line)
        # these are used to center the play area in the game
        self.offset_x = (self.game_x % self.block_x ) // 2
        self.offset_y = (self.game_y % self.block_y ) // 2

    def init_menu(self):
        # put up three block images on the left - this will eventually be replaced, but
        # will help get our menu rendering going...
        self.menu_sprites = []
        for image in self.sprite_types[:3]:
            self.menu_sprites.append(Sprite("", image_data=image, x=0, y=0))
        self.update_menu()

    def update_menu(self):
        """ Update the sprites, ordering from the bottom """
        x_pos = (self.menu_x - self.block_x) // 2 + self.offset_x
        y_pos = self.offset_y + 50 # account for bottom text
        self.menu_sprites[0].image = self.sprite_types[self.curr_sprite]
        for sprite in self.menu_sprites:
            sprite.x = x_pos
            sprite.y = y_pos + sprite.image.height
            sprite.update()
            y_pos += self.offset_y + sprite.image.height
            
    def main_loop(self):
        #Create a font and put it in bottom left
        ft = font.load('Arial', 28)
        my_text = font.Text(ft, y=10)

        #Schedule the Monster creation
        #clock.schedule_interval(self.create_monster, 0.05)
        clock.set_fps_limit(60)

        while not self.has_exit:
            self.dispatch_events()
            self.clear()

            self.update()
            self.draw()

            #Tick the clock
            clock.tick()
            #Gets fps and draw it
            my_text.text = ("fps: %d") % (clock.get_fps())
            my_text.draw()

            self.flip()
        
    def update(self):
        for (x,y), sprite_stack in list(self.sprites.items()):
            for z, sprite in enumerate(sprite_stack):
                sprite.update_pos(self, x, y, z)
                sprite.update()
        self.update_menu()

    def draw(self):
        sprite_list = list(self.sprites.items())
        sprite_list.sort()
        sprite_list.reverse()
        cursor_drawn = False
        
        for line in self.coords:
            for (x,y) in line:
                sprite_stack = self.sprites.get((x,y), [])
                for sprite in sprite_stack:
                    sprite.draw()
                if x == self.cursor.x_pos and y == self.cursor.y_pos:
                    self.cursor.draw()
                    cursor_drawn = True
        
        for sprite in self.menu_sprites:
            sprite.draw()
        
        if not cursor_drawn:
            self.cursor.draw()

    def update_cursor(self, x, y):
        if x is None:
            # put the cursor out of sight
            self.cursor.x = -1000
            return
        z = len(self.sprites.get((x, y), []))
        self.cursor.x = self.menu_x + self.offset_x + x * self.block_x
        self.cursor.y = self.offset_y + (y * self.block_y) + (z * self.block_z)
        self.cursor.x_pos = x
        self.cursor.y_pos = y
        print(x, y, self.cursor.x, self.cursor.y)

    def mouse_to_array(self, x, y):
        # mod the coords to be relative to game area
        x_num = x - (self.menu_x + self.offset_x)
        y_num = y - (self.offset_y + self.block_z)
        #print x_num, y_num

        # convert to array pos
        x_num = x_num // self.block_x
        y_num = y_num // self.block_y
        #print "x: %s -> %s/%s\ty: %s -> %s/%s" % (x, x_num, self.blocks_across, y, y_num, self.blocks_down)

        # check bounds
        if (0 <= x_num < self.blocks_across and
            0 <= y_num < self.blocks_down):
            return (x_num, y_num)
        else:
            return (None, None)

    def get_sprite(self, x_num, y_num):
        return self.sprites.get((x_num, y_num, 0), [])

    def create_block(self, x, y, block_type):
        """ grab the block at the coords (if one exists) and update it """
        sprite_stack = self.get_sprite(x, y)
        if sprite_stack:
            sprite = sprite_stack[-1]
            sprite.image = block_type
            return

        # no existing block, so create a new one
        block_x = x * self.block_x + self.offset_x + self.menu_x
        block_y = y * self.block_y + self.offset_y

        bar = Sprite("", image_data=block_type, x=block_x, y=block_y)
        if (x, y) in self.sprites:
            self.sprites[(x, y)].append(bar)
        else:
            self.sprites[(x, y)] = [bar]
    
    def destroy_block(self, x, y):
        # grab the block at the coords (if one exists) and delete it
        sprite_stack = self.sprites.get((x, y), [])
        if sprite_stack:
            self.sprites[(x,y)] = sprite_stack[:-1]

    """******************************************
    Event Handlers
    *********************************************"""
    def on_mouse_motion(self, x, y, dx, dy):
        if x > self.menu_x + self.offset_x:
            x, y = self.mouse_to_array(x, y)
            self.update_cursor(x, y)
        else:
            self.cursor.x = -1000

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if x <= self.menu_x + self.offset_x:
            self.cursor.x = -1000
            return
            
        print(x, y, dx, dy, buttons, modifiers)
        x_pos, y_pos = self.mouse_to_array(x, y)

        if buttons == 1 and (x_pos != self.cursor_x or y_pos != self.cursor_y):
            # dragged while holding left mouse: drop another block
            self.create_block(x_pos, y_pos, self.sprite_types[self.curr_sprite])
        if buttons == 4 and (x_pos != self.cursor_x or y_pos != self.cursor_y):
            # delete topmost from under the cursor
            self.destroy_block(x_pos, y_pos)
        self.cursor_x = x_pos
        self.cursor_y = y_pos
        self.update_cursor(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_pressed = button

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.curr_sprite += scroll_y
        self.curr_sprite = self.curr_sprite % len(self.sprite_types)
        if self.curr_sprite < 0:
            self.curr_sprite += len(self.sprite_types)
        print("self.curr_sprite is now", self.curr_sprite) 

    def on_mouse_release(self, x, y, button, modifiers):
        self.mouse_pressed = 0
        if x < self.menu_x + self.offset_x:
            pass
        else:
            # convert x,y to array coords
            x,y = self.mouse_to_array(x, y)
            #print "button %s at (%s, %s)" % (button, x, y)
            if x is None:
                return
            if button == 1:
                # create a grass block
                self.create_block(x, y, self.sprite_types[self.curr_sprite])
            elif button == 4:
                self.destroy_block(x, y)

class Sprite(object):

    def __get_left(self):
        return self.x
    left = property(__get_left)

    def __get_right(self):
        return self.x + self.image.width
    right = property(__get_right)

    def __get_top(self):
        return self.y + self.image.height
    top = property(__get_top)

    def __get_bottom(self):
        return self.y
    bottom = property(__get_bottom)

    def __init__(self, image_file, image_data=None, **kwargs):

        #init standard variables
        self.image_file = image_file
        if (image_data is None):
            self.image = load_image(image_file)
        else:
            self.image = image_data
        self.x = 0
        self.y = 0
        self.x_pos = 0
        self.y_pos = 0

        self.dead = False
        #Update the dict if they sent in any keywords
        self.__dict__.update(kwargs)

    def draw(self):
        self.image.blit(self.x, self.y)

    def update_pos(self, game, x, y, z):
        self.x_pos = x
        self.y_pos = y
        self.z_pos = z
        self.x = game.menu_x + game.offset_x + x * game.block_x
        self.y = game.offset_y + y * game.block_y + z * game.block_z

    def update(self):
        pass

    def intersect(self, sprite):
        """Do the two sprites intersect?
        @param sprite - Sprite - The Sprite to test
        """
        return not ((self.left > sprite.right)
            or (self.right < sprite.left)
            or (self.top < sprite.bottom)
            or (self.bottom > sprite.top))

    def collide(self, sprite_list):
        """Determing ther are collisions with this
        sprite and the list of sprites
        @param sprite_list - A list of sprites
        @returns list - List of collisions"""

        lst_return = []
        for sprite in sprite_list:
            if (self.intersect(sprite)):
                lst_return.append(sprite)
        return lst_return

    def collide_once(self, sprite_list):
        """Determine if there is at least one
        collision between this sprite and the list
        @param sprite_list - A list of sprites
        @returns - None - No Collision, or the first
        sprite to collide
        """
        for sprite in sprite_list:
            if (self.intersect(sprite)):
                return sprite
        return None


if __name__ == "__main__":
    try:
        antland = GameWindow(fullscreen=True)
        antland.main_loop()
        antland.close()
    except Exception as error_message:
        #antland.close()
        import traceback
        print("There was an error!:")
        traceback.print_exc()

    print("Hit enter to continue")
    ignored = input()


