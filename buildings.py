#
# Villager Game
# Buildings Module
# Written by Madeline Autumn
#

### Imports and variables ###
import random
import config

### Buildings ###

class Building:
    '''Main building class'''

    def __init__(self):

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.profession = None

    def get_texture(self, pos):
        '''returns the texture for the building'''

        texture = self.texture.replace('\n','')[pos]
        colour = self.colours[self.colour_map[pos]]
        
        return (texture, colour)

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

class WoodenHut(Building):
    '''Simple build that holds two villagers'''

    def __init__(self, pos_x=None, pos_y=None):

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
                     'wood': 10}

    def on_creation(self):
        '''Runs functions for when the building is built'''
        
        # Increase the max number of villagers
        config.max_villagers += 1 

class WoodenStatue(Building):
    '''Simple statue that provides an instant boost to happiness
        slightly increases chance of new villagers'''

    def __init__(self, pos_x=None, pos_y=None):

        self.name = 'Wooden Statue'
        self.description = 'A simple wooden statue'

        self.size = (3,3)
        self.texture = '''
 ± 
┐┼┌
≡≡≡'''
        self.colour_map = (0,2,0,
                           0,0,0,
                           1,1,1)
        
        self.colours = ['chocolate3', 'brown4', 'navajo white']

        self.cost = {'food': 0,
                     'wood': 6}
    
    def on_creation(self):
        '''Runs functions for when the building is built'''
        
        # Run through all villagers and add to their happiness by 1
        for villager in config.villagers:
            villager.gain_happiness(1, 1)

class Farm(Building):
    '''A farm the provides a space for farmers to work
        hold one farmer job'''

    def __init__(self, pos_x=None, pos_y=None):

        self.name = 'Farm'
        self.description = 'Provides food for the village'

        self.size = (3,2)
        self.texture = ''
        # Produce a randomized colourmap for each object
        self.colour_map = []
        self.colours = ['sienna3', 'chocolate3', 'indianred3', 'goldenrod', 'forest green']

        for i in range(self.size[0]*self.size[0]):

            # Add plants to the texture
            if random.randint(1,4) == 1:
                self.texture += '♠'
                self.colour_map.append(random.randint(2, len(self.colours)-1))
            else:
                self.texture += '≈'
                self.colour_map.append(random.randint(0, len(self.colours)-3))
        
        

        self.cost = {'food': 5,
                     'wood': 0}
    
    def on_creation(self):
        '''Runs functions for when the building is built'''
        
        # Run through all villagers and add to their happiness by 1
        for villager in config.villagers:
            villager.gain_happiness(1, 1)
