#
# Villager Game
# Map Module
# Written by Madeline Autumn
#

### Importants and Varibles ###
import config
import random

### Classes ###
class Map:
    '''Deals with the functionality of the map'''

    def __init__(self):

        # Map variables
        self.width = 96
        self.height = 42

        # Map storage
        self.map = {}
        self.texture_map = []

        # Selector positions
        self.selector_x = int(self.width/2)
        self.selector_y = int(self.height/2)

        # Map frame
        self.frame = None

    def check_free_land(self, building, pos_x, pos_y, extra_space=False):
        '''Checks if the land is free from buildings based on set building'''

        # Check if extra space padding is required
        if extra_space == True:
            pos_x -= 1
            pos_y -= 1
            building_range = (building.size[0]+2,
                              building.size[1]+2)
        else:
            building_range = (building.size[0],
                              building.size[1])

        # Check the selected area has enough space
        for x in range(building_range[0]):
            for y in range(building_range[1]):
                
                # Get unique building object and data 
                pos_key = f'({pos_y+y}:{pos_x+x})'
                
                if pos_key in self.map.keys():
                    return False
        
        return True
    
    def build_building(self, building, pos_x, pos_y, pay=True, extra_space=False):
        '''Creates a building on the map'''

        # Get the building position
        building.pos_x = pos_x
        building.pos_y = pos_y

        if not(self.check_free_land(building, building.pos_x, building.pos_y, extra_space)):
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

        # Add building to map
        building.positions = []
        for x in range(building.size[0]):
            for y in range(building.size[1]):

                pos_key = f'({building.pos_y+y}:{building.pos_x+x})'

                building.positions.append(pos_key)
                self.map[pos_key] = building
        
        # Draw building onscreen
        self.frame.insert_building(f'({building.pos_y}:{building.pos_x})')

        return True
