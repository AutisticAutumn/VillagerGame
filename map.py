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
    
    def build_building(self, key, pay=True):
        '''Creates a building on the map'''

        building = config.get_building(key)

        # Get the building position
        posy = 6
        posx = 13

        # Make payments for building
        if pay:
            # Check food
            if building.cost['food'] <= config.food:
                config.food -= building.cost['food']
            else:
                return False
            
            # Check wood
            if building.cost['wood'] <= config.wood:
                config.wood -= building.cost['wood']
            else:
                return False

        # Add each segement seperately to the main map dictionary
        for x in range(building.size[0]):
            for y in range(building.size[1]):
                
                # Get unique building object and data 
                building = config.get_building(key)
                segment = x + (y*building.size[0])
                pos_key = f'({posy+y}:{posx+x})'

                # Add building to map
                config.map[pos_key] = building
                config.map[pos_key].pos = segment
