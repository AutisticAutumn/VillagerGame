#
# Villager Game
# Map Module
# Written by Madeline Autumn
#

### Importants and Varibles ###
from math import *
import config
import random

### Functions ###
def cos_lerp(a, b, x):
    '''Lerps between two points (a,b) with cosine function'''

    ft = x*pi
    f =  (1 - cos(ft))*0.5

    return a*(1-f) + b*f

### Classes ###
class Map:
    '''Deals with the functionality of the map'''

    def __init__(self):

        # Map constants
        self.default_width = 96
        self.default_height = 42

        # Map variables
        self.width = self.default_width
        self.height = self.default_height
        self.get_world_data()

        # Selector positions
        self.selector_x = int(self.width/2)
        self.selector_y = int(self.height/2)

        # Map frame
        self.frame = None

    def reset_map(self):
        '''Purges all maps'''
        # Map storage
        self.map = {}
        self.texture_map = []
        self.terrain_map = []

    def get_world_data(self):
        '''Gets boundries for world data based on world size'''

        size = self.width * self.height

        # Get pond stats
        self.pond_min = floor(size*0.00075)
        self.pond_max = floor(size*0.002)

        # Get tree stats
        self.tree_min = floor(size*0.0075)
        self.tree_max = floor(size*0.0125)

    def get_ground_texture(self, x, y):
        '''Get the texture for the ground base'''

        # Merge position values
        pos = x + (y * self.width)

        if not(self.terrain_map[pos]) == 'Tree':
            return config.get_building(self.terrain_map[pos]).get_texture(y + x*123456)
        else:
            return (config.get_building('Tree').get_texture(5))

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
                pos = (pos_x+x) + (((pos_y+y)-1)*self.width)
                
                if pos_key in self.map.keys() or self.terrain_map[pos] != 'Grass':
                    return False
        
        return True
    
    def build_building(self, building, pos_x, pos_y, 
                        pay=True, extra_space=False, price_mod=1):
        '''Creates a building on the map'''

        # Get the building position
        building.pos_x = pos_x
        building.pos_y = pos_y

        if not(self.check_free_land(building, building.pos_x, building.pos_y, extra_space)):
            return False

        # Make payments for building
        if pay:
            try:
                # Check Prices
                config.food -= self.check_building_cost(building, 'food', config.food, price_mod)
                config.wood -= self.check_building_cost(building,'wood', config.wood, price_mod)
                config.stone -= self.check_building_cost(building,'stone', config.stone, price_mod)
            except:
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

    def check_building_cost(self, building, material, material_total, price_mod):
        '''Checks if a building can be built for the cost'''
        cost = round(building.cost[material]*price_mod)
        if cost <= material_total:
            return cost
        else:
            return 'False'

    ## Generation functions ##
    def create_ponds(self, total_ponds):
        '''Adds ponds to the map'''

        # Get a list of pond coords
        pond_positions = self.get_pond_positions(total_ponds)

        # Loop and add the ponds to the map
        for pond in pond_positions:
            
            pond_size = (random.randint(7,9), random.randint(2,3))
            pond_x = pond[0]
            pond_y = pond[1]

            # Run through the pond's area and add water
            for x in range(pond_x-pond_size[0], pond_x+pond_size[0]):
                for y in range(pond_y-pond_size[1], pond_y+pond_size[1]):

                    # Get values from center point for tile with cos lerp
                    xx = cos_lerp(pond_x, pond_size[0]+pond_x, abs(x-pond_x)/pond_size[0])
                    xx -= pond_x

                    yy = cos_lerp(pond_y, pond_size[1]+pond_y, abs(y-pond_y)/pond_size[1])
                    yy -= pond_y

                    # Return texture if value is within bounds\
                    size_m = pond_size[0] + pond_size[1]
                    if (xx+yy)**2 < random.randint(8*size_m, 32*size_m)/10:
                        pos = x + ((y-1)*self.width)
                        texture = config.get_building('Pond Water').get_texture(y + x*123456)

                        self.texture_map[pos] = texture
                        self.terrain_map[pos] = 'Pond Water'

    def get_pond_positions(self, total_ponds):
        '''Get the positions of the ponds for the map'''

        pond_positions = []

        # Run through all ponds
        for i in range(total_ponds):

            pond_added = False

            # Repeat loop until sutiable location found
            while pond_added == False:
            
                # Get pond positions
                pos = (random.randint(8, config.map.width-8), 
                    random.randint(8, config.map.height-8))

                # Check position against other positions to make sure
                #  ponds are spaced out correctly on the map
                spacing = -1
                if len(pond_positions) > 0:
                    for pond_pos in pond_positions:
                        
                        spacing = abs((pos[0] - pond_pos[0]) +
                                    (pos[1] - pond_pos[1]))
                            
                if spacing > 16 or spacing < 0:
                    pond_added = True
            
            pond_positions.append(pos)

        return pond_positions

    def plant_tree(self):
        '''Plants a tree on the map'''

        while True:

            # Get variables
            tree = config.get_building('Tree')
            x = random.randint(2, self.width-tree.size[0])
            y = random.randint(2, self.height-tree.size[1])

            tree.pos_x = x
            tree.pos_y = y

            # Check if space is empty
            space_free = self.check_free_land(tree, x, y)

            if space_free:
                
                # Add texture
                for xx in range(tree.size[0]):
                    for yy in range(tree.size[1]):


                        # Get variables
                        pos = (x+xx) + ((y+yy)*config.map.width)
                        texture = tree.get_texture(xx + (yy*tree.size[0]))

                        # Add a tree to the center
                        if texture[0] == 'O':
                            self.terrain_map[pos] = 'Tree'
                        else:
                            texture = config.map.get_ground_texture(x+xx, y+yy)

                        self.texture_map[pos] = texture

                return True
