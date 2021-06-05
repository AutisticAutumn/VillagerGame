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
        self.colour = 'green'

    def get_texture(self, randkey):
        '''returns the texture for the building'''

        # Make sure texture is psudo-random 
        random.seed(config.grass_seed + randkey)
        texture = random.choice(self.texture)
        random.seed(config.seed)
        
        return texture

class WoodenHut:
    '''Simple build that holds two villagers'''

    def __init__(self):

        self.name = 'Wooden Hut'
        self.description = ''

        self.size = (4,2)
        self.pos = 0
        self.texture = '''
┌──┐
└──┘'''
        
        self.colour = 'saddle brown'

        self.cost = {'food': 0,
                     'wood' : 10}
        self.profession = None

    def get_texture(self):
        '''returns the texture for the building'''
        
        return self.texture.replace('\n','')[self.pos]
