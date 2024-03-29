#
# Villager Game
# Buildings Module
# Written by Madeline Autumn
#

### Imports and variables ###
import random, mapUI
import config
from math import floor

### Functions ###
def get_building(key):
    '''Returns a unique building object based off key'''

    if key == Grass().name:
        return Grass()

    if key == PondWater().name:
        return PondWater()

    if key == Tree().name:
        return Tree()
    
    if key == WoodenHut().name:
        return WoodenHut()
    
    if key == WoodenStatue().name:
        return WoodenStatue()

    if key == Farm().name:
        return Farm()
    
    if key == Mine().name:
        return Mine()

    if key == Storehouse().name:
        return Storehouse()

### Parent Classes ###
class Building:
    '''Main building class'''

    def __init__(self):

        self.pos_x = None
        self.pos_y = None

        self.profession = None
        self.worker = None
        
        self.cost = {'food' : 0,
                     'wood' : 0,
                     'stone' : 0}

    def get_texture(self, pos):
        '''returns the texture for the building'''

        texture = self.texture.replace('\n','')[pos]
        colour = self.colours[self.colour_map[pos]]

        try:
            background = self.colours[self.background_map[pos]]
            if self.background_map[pos] != 0:
                 return (texture, colour, background)
        except:
            pass

        return (texture, colour)

    def update_texture_map(self, reset_villager=False):
        '''Updates a buildings texture on the map'''

        x0 = self.pos_x
        x1 = self.pos_x + self.size[0]

        y0 = self.pos_y
        y1 = self.pos_y + self.size[1]

        updated_positions = []

        # Run through the complete building
        for y in range(y0, y1):
            for x in range(x0, x1):
                    
                # Get position and texture
                pos = (x-x0)+((y-y0)*self.size[0])
                texture = self.get_texture(pos)

                updated_positions.append(f'{y}.{x-1}')

                # Ignore tile if villager is placed there
                villager_texture = config.map.texture_map[pos][0] in config.villager_textures
                if not(villager_texture) or reset_villager:

                    # Don't update texture map if no texture exists
                    if texture[0] == ' ':
                        texture = config.map.get_ground_texture(x, y)

                    # Update the texture map
                    pos = x + ((y-1)*config.map.width)
                    config.map.texture_map[pos] = texture

        mapUI.draw_map(config.map.frame, updated_positions)

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
        self.text_colour = 'white'

    def get_texture(self, randkey):
        '''returns the texture for the building'''

        # Make sure texture is psudo-random 
        random.seed(config.grass_seed + randkey)
        texture = random.choice(self.texture)

        try:
            background = random.choice(self.background)
            return (texture, random.choice(self.colours), background)
        except:
            pass

        # Add to seed so new number is produced every time
        config.reset_seed()
        
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
        self.text_colour = self.colours[0]

class PondWater(Terraian):

    def __init__(self):

        Terraian.__init__(self)
        
        self.name = 'Pond Water'
        
        self.description = 'Stagnant Water'
        self.texture = '≈≈~'
        self.colours = ['blue', 'blue3']
        self.text_colour = self.colours[0]

class Tree(Building, Terraian):

    def __init__(self):

        Building.__init__(self)
        Terraian.__init__(self)

        self.name = 'Tree'
        self.text_colour = 'chocolate2'
        self.description = 'Simple tree\ncan be used to gather wood'

        self.texture = '    O    '
        self.colour_map = [0,0,0,
                           0,0,0,
                           0,0,0]
        self.size = (3, 3)
        self.colours = ['chocolate2']
        self.text_colour = self.colours[0]

    # Note that tree uses Building class instead of terrain due to the fact
    #  that the tree is more solid and function wise it makes more sense to
    #  be classed as a building.

## Villager Buildings
class WoodenHut(Building):
    '''Simple build that holds two villagers'''

    def __init__(self):

        # Get inherited data
        Building.__init__(self)

        # Get building data
        self.name = 'Wooden Hut'
        self.text_colour = 'chocolate3'
        self.description = 'A simple wooden hut that houses one villager'
        self.type = 'House'

        self.size = (4,3)
        self.reset_texture()

        self.cost['wood'] = 10

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
        
        self.colours = ['chocolate3', 'brown3']
        
class WoodenStatue(Building):
    '''Simple statue that provides an instant boost to happiness
        slightly increases chance of new villagers'''

    def __init__(self):
        
        # Get inherited data
        Building.__init__(self)

        # Get building data
        self.name = 'Wooden Statue'
        self.text_colour = 'chocolate3'
        self.description = ''.join(['A simple wooden statue that provides a ',
                           'small one time happiness boost\nSlightly increases ',
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

        self.cost['wood'] = 6
    
    def on_creation(self):
        '''Runs functions for when the building is built'''
        
        # Run through all villagers and add to their happiness by 1
        for villager in config.villagers:
            villager.gain_morale(1, 1)

class Farm(Building):
    '''A farm the provides a space for farmers to work
        hold one farmer job'''

    def __init__(self):
        
        # Get inherited data
        Building.__init__(self)

        # Get building data
        self.name = 'Farm'
        self.text_colour = 'lawn green'
        self.description = 'Provides food for the village\nRequires a farmer villager to produce food'
        self.type = 'Work'

        self.size = (5, 4)
        
        self.food = 0
        self.profession = 'Farmer'

        # Produce a randomized colourmap for each object
        self.texture = ''
        self.colour_map = []
        
        self.reset_texture()

        # Add crops to farm
        self.cost['food'] = 5

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

class Mine(Building):
    '''Mine is where stone can be gathered'''

    def __init__(self):
        # Get inherited data
        Building.__init__(self)

        # Get building data
        self.name = 'Mine'
        self.text_colour = 'slate gray'
        self.description = 'A mine where stone can be harvested\nRequires a miner villager to produce stone'
        self.type = 'Work'
        self.profession = 'Miner'

        self.size = (6,2)
        self.reset_texture()

        self.cost['wood'] = 12
        
    def reset_texture(self):
        '''Reset texture to default'''

        self.texture = '''
 ●══● 
±║≡≡║±'''
        self.colour_map = [0,1,1,1,1,0,
                           4,1,2,2,1,4]
        self.background_map = [0,0,0,0,0,0,
                               0,0,3,3,0,0]
        
        self.colours = ['black', 'chocolate3', 'dark slate gray', 'gray16', 'gray64']

class Storehouse(Building):

    def __init__(self):
        # Get inherited data
        Building.__init__(self)

        # Get building data
        self.name = 'Storehouse'
        self.text_colour = 'sienna1'
        self.description = 'Can store up to 32 of any material'
        self.type = 'Storage'

        self.capacity = 32
        self.materials = []
        self.storage = []
        self.barrels = 0

        # Create initial texture
        self.texture = '''●----●¦++++¦●----●'''
        self.colours = ['chocolate3', 'brown4', 'tan1', 'tan4']
        self.colour_map = [0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0]
        self.background_map = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        self.size = (6,3)
        #self.reset_texture()

        self.cost['wood'] = 20

    def reset_texture(self):
        '''Reset texture to default'''
        
        self.barrel_textures = ['õ', 'ð', '%']

        temp_texture = []
        center_texture = []

        # Only update texture if the number of barrels has changed
        if floor(len(self.storage)/8) != self.barrels:

            # Create initial texture
            self.texture = '''●----●¦    ¦●----●'''
            self.colour_map = [0,0,0,0,0,0,
                               0,1,1,1,1,0,
                               0,0,0,0,0,0]
            self.background_map = [0,0,0,0,0,0,
                                   0,0,0,0,0,0,
                                   0,0,0,0,0,0]

            self.barrels = floor(len(self.storage)/8)

            # Add barrels
            for i in range(self.barrels):
                center_texture.append(random.choice(self.barrel_textures))

            for i in range(floor(self.capacity/8)-self.barrels):
                center_texture.append('+')
            
            random.shuffle(center_texture)
            
            # Add variable details to texture
            for i in range(self.size[0]*self.size[1]):
                
                if self.texture[i] != ' ':
                    temp_texture.append(self.texture[i])
                else:
                    temp_texture.append(center_texture[0])

                    if center_texture[0] in self.barrel_textures:
                        self.colour_map[i] = 2
                        self.background_map[i] = 3
                    else:
                        self.background_map[i] = 0

                    center_texture.pop(0)

            # Set final texture
            self.texture = ''.join(temp_texture)
            
        # Attempt to update texture on the map if possible
        try:
            self.update_texture_map()
        except:
            pass
