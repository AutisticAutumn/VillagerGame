#
# Villager Game
# Buildings Module
# Written by Madeline Autumn
# Last modified on 06/06/21
#

### Imports and variables ###
import random
import config

### Buildings ###

class Grass:
    '''Default grass. Does nothing'''

    def __init__(self):
        
        self.name = 'Grass'
        self.description = 'Grass'
        self.texture = '''  '".,  '''
        self.colours = ['green']

    def get_texture(self, randkey):
        '''returns the texture for the building'''

        # Make sure texture is psudo-random 
        random.seed(config.grass_seed + randkey)
        texture = random.choice(self.texture)
        random.seed(config.seed + config.turn)
        
        return (texture, self.colours[0])

class WoodenHut:
    '''Simple build that holds two villagers'''

    def __init__(self, pos_x=None, pos_y=None):

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.name = 'Wooden Hut'
        self.description = 'A simple wooden hut'

        self.size = (4,3)
        self.texture = '''
┌──┐
│##│
└──┘'''
        self.colour_map = (0,0,0,0,
                           0,1,1,0,
                           0,0,0,0)
        
        self.colours = ['chocolate3', 'brown4']

        self.cost = {'food': 0,
                     'wood' : 10}
        self.profession = None

    def get_texture(self, pos):
        '''returns the texture for the building'''

        texture = self.texture.replace('\n','')[pos]
        colour = self.colours[self.colour_map[pos]]
        
        return (texture, colour)
