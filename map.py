#
# Villager Game
# Map Module
# Written by Madeline Autumn
# Last modified on 05/06/21
#

### Importants and Varibles ###
import config
import random

### Classes ###
class Map:
    '''Deals with the functionality of the map'''

    def __init__(self, frame):

        self.frame = frame
    
    def build_building(self, key):
        '''Creates a building on the map'''

        posy = 6
        posx = 13

        # Add each segement seperately to the main map dictionary
        for x in range(config.get_building(key).size[0]):
            for y in range(config.get_building(key).size[1]):

                building = config.get_building(key)

                segment = x + (y*building.size[0])

                pos_key = f'({posy+y}:{posx+x})'

                config.map[pos_key] = building
                config.map[pos_key].pos = segment
                print(config.map[pos_key])
