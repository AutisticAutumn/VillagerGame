#
# Villager Game
# Buildings Module
# Written by Madeline Autumn
#

### Imports and variables ###
import random
import config

### Parent Classes ###
class Building:
    '''Main building class'''

    def __init__(self):

        self.pos_x = None
        self.pos_y = None

        self.profession = None
        self.worker = None

    def get_texture(self, pos):
        '''returns the texture for the building'''

        texture = self.texture.replace('\n','')[pos]
        colour = self.colours[self.colour_map[pos]]

        return (texture, colour)

    def update_texture_map(self):
        x0 = self.pos_x
        x1 = self.pos_x + self.size[0]

        y0 = self.pos_y
        y1 = self.pos_y + self.size[1]

        # Run through the complete building
        for y in range(y0, y1):
            for x in range(x0, x1):
                    
                # Get position and texture
                pos = (x-x0)+((y-y0)*self.size[0])
                texture = self.get_texture(pos)
                
                # Don't update texture map if no texture exists
                if texture[0] != ' ':
                    # Update the texture map
                    pos = x + ((y-1)*config.map.width)
                    config.map.texture_map[pos] = texture

    def on_creation(self):
        '''Runs functions for when the building is built'''
        pass

    def begin_turn(self):
        '''Run any start of turn functions for the building'''
        pass

class Terraian:
    '''Global terrain class'''

    def __init__(self):

        self.type = 'Terraian'

    def get_texture(self, randkey):
        '''returns the texture for the building'''

        # Make sure texture is psudo-random 
        random.seed(config.grass_seed + randkey)
        texture = random.choice(self.texture)
        random.seed(config.seed + config.turn)
        
        return (texture, random.choice(self.colours))

### Building Classes ###
## Terrain ##
class Grass(Terraian):
    '''Default grass. Does nothing'''

    def __init__(self):

        Terraian.__init__(self)
        
        self.name = 'Grass'
        self.description = 'Grass'
        self.texture = '''  '".,  '''
        self.colours = ['green']

class PondWater(Terraian):

    def __init__(self):

        Terraian.__init__(self)
        
        self.name = 'Pond Water'
        self.description = 'Stagnant Water'
        self.texture = '≈≈~'
        self.colours = ['blue', 'blue3']

## Villager Buildings
class WoodenHut(Building):
    '''Simple build that holds two villagers'''

    def __init__(self):

        # Get inherited data
        Building.__init__(self)

        # Get building data
        self.name = 'Wooden Hut'
        self.description = 'A simple wooden hut'
        self.type = 'House'

        self.size = (4,3)
        self.reset_texture()

        self.cost = {'food': 0,
                     'wood': 10}

        self.villager = None

    def on_creation(self):
        '''Runs functions for when the building is built'''
        
        # Increase the max number of villagers
        config.max_villagers += 1 

    def reset_texture(self):
        '''Reset texture to default'''

        self.texture = '''
●──●
│++│
●──●'''
        self.colour_map = [0,0,0,0,
                           0,1,1,0,
                           0,0,0,0]
        
        self.colours = ['chocolate3', 'brown4']
        


class WoodenStatue(Building):
    '''Simple statue that provides an instant boost to happiness
        slightly increases chance of new villagers'''

    def __init__(self):
        
        # Get inherited data
        Building.__init__(self)

        # Get building data
        self.name = 'Wooden Statue'
        self.description = ''.join(['A simple wooden statue that provides a ',
                           'small one time happiness boost and slightly increases ',
                           'the chance of new villagers appearing'])
        self.type = 'Misc'

        self.size = (3,3)
        self.texture = '''
 ± 
┐┼┌
≡≡≡'''
        self.colour_map = [0,2,0,
                           0,0,0,
                           1,1,1]
        
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

    def __init__(self):
        
        # Get inherited data
        Building.__init__(self)

        # Get building data
        self.name = 'Farm'
        self.description = 'Provides food for the village'
        self.type = 'Work'

        self.size = (5, 4)
        
        self.food = 0
        self.profession = 'Farmer'

        # Produce a randomized colourmap for each object
        self.texture = ''
        self.colour_map = []
        
        self.reset_texture()

        # add crops to farm
        self.cost = {'food': 5,
                     'wood': 0}

    def reset_texture(self, crops=0):
        '''Reset the texture to include new crops'''

        # Reset texture data
        self.texture = []
        self.colours = ['sienna1', 'chocolate3', 'indianred3', 'goldenrod', 'forest green']
        self.colour_map = []
        
        texture_temp = ''
        self.food = 0

        # Add crops and dirt
        for i in range(crops):
            texture_temp += '♠'
            self.food += 1

        for i in range( ( (self.size[0]-2) * (self.size[1]-2) ) - crops):
            texture_temp += '≈'

        # Shuffle the string and add to main texture
        texture_temp = ''.join(random.sample(texture_temp ,len(texture_temp)))

        # Add buffer around main texture
        for i in range(self.size[0]+1): 
            self.texture.append(' ')
        for i in range(self.size[0]-2): 
            self.texture.append(texture_temp[i])
        for i in range(2): 
            self.texture.append(' ')
        for i in range(self.size[0]-2): 
            self.texture.append(texture_temp[i+self.size[0]-2])
        for i in range(self.size[0]+1): 
            self.texture.append(' ')

        self.texture = ''.join(self.texture)

        # Add colour to the texture
        for texture in self.texture:
            if texture == '♠':
                self.colour_map.append(random.randint(2, 4))
            else: 
                self.colour_map.append(random.randint(0, 1))

        # Attempt to update texture on the map if possible
        try:
            self.update_texture_map()
        except:
            pass
