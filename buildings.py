#
# Villager Game
# Buildings Module
# Written by Madeline Autumn
# Last modified on 05/06/21
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
        self.texture = [' ', ' ', ' ', ' ',
                        '`', '.', ',', '"']
        self.colour = 'green'

    def get_texture(self):
        '''returns the texture for the building'''

        return random.choice(self.texture)

class WoodenHut:
    '''Simple build that holds two villagers'''

    def __init__(self):

        self.name = 'Wooden Hut'
        self.description = ''

        self.size = (3,2)
        self.pos = 0
        self.texture = ['┌','─','┐',
                        '└','─','┘']
        
        self.colour = 'saddle brown'

        self.cost = {'food': 0,
                     'wood' : 10}
        self.profession = None

    def get_texture(self):
        '''returns the texture for the building'''
        
        return self.texture[self.pos]
