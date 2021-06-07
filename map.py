#
# Villager Game
# Map Module
# Written by Madeline Autumn
# Last modified on 07/06/21
#

### Importants and Varibles ###
import config
import random

### Classes ###
class Map:
    '''Deals with the functionality of the map'''

    def __init__(self, frame):

        self.frame = frame

    def check_free_land(self, building, pos_x, pos_y):
        '''Checks if the land is free from buildings based on set building'''

        # Check the selected area has enough space
        for x in range(building.size[0]):
            for y in range(building.size[1]):
                
                # Get unique building object and data 
                pos_key = f'({building.pos_y+y}:{building.pos_x+x})'
                
                if pos_key in config.map.keys():
                    print('True')
                    return False
        
        return True
    
    def build_building(self, key, pay=True):
        '''Creates a building on the map'''

        building = config.get_building(key)

        # Get the building position
        building.pos_x = 12
        building.pos_y = 6

        if not(self.check_free_land(building, building.pos_x, building.pos_y)):
            return False


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
                pos_key = f'({building.pos_y+y}:{building.pos_x+x})'

                # Add building to map
                config.map[pos_key] = building
        
        # Draw building onscreen
        self.frame.insert_building(f'({building.pos_y}:{building.pos_x})')
