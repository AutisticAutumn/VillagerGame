#
# Villager Game
# Professions Module
# Written by Madeline Autumn
#

### Imports and variables ###
import config
import map
import random

### Functions ###

def draw_villager_home(villager):
    '''Draws a villager into their house'''

    # Make sure villager has a house to display in
    if villager.house != None:
            
        # Reset house texture
        villager.house.update_texture_map(True)

        # Set new texture as villager face
        pos_change = random.randint(1,2)
        pos_x = villager.house.pos_x + pos_change
        pos_y = villager.house.pos_y + 1

        draw_villager(villager, pos_x, pos_y)

def draw_villager(villager, pos_x, pos_y):
    '''Draws the villager from set building positions'''
    
    villager.pos = (pos_x, pos_y)
    villager.draw_villager()


### Professions ###

class Profession:
    '''Main profession class that deals with globals'''

    def __init__(self):

        self.building = None

    def action(self, villager):
        '''Place villager in house if nothing else occurs'''

        self.villager_location_set(villager)
        
    
    def turn_action(self, villager):
        '''Opens the popout for the placement'''

        building = config.get_building(self.buildings[0])

        config.map.popout.villager = villager
        config.map.popout.building = building
        config.map.popout.create_toplevel()

    def turn_action_popout_closed(self, villager, building, pos):
        '''Runs the functions for when the popout closes'''

        # Set the action for the villager
        villager.turn_action = (config.map.build_building, building, pos)

        # Return output to logs
        response = config.get_response('build_turn_action')
        response[0] = response[0].format(villager.name, building.name)
        villager.append_villager_log(response)

    def villager_location_set(self, villager):
        '''Places the villager in there house for their action'''

        draw_villager_home(villager)
    

class Unemployed(Profession):
    '''Unemployed villagers provide no materials or bonuses but can build buildings'''

    def __init__(self):

        # Inherit data
        Profession.__init__(self)

        # Villager info
        self.name = 'Unemployed'
        self.description = ''
        self.colour = 'light grey'

class Farmer(Profession):
    '''The farmer provides foods for the village at Farms'''

    def __init__(self):

        # Inherit data
        Profession.__init__(self)

        # Villager info
        self.name = 'Farmer'
        self.description = 'Provides 2-4 food each turn'
        self.building = 'Farm'
        self.colour = 'green yellow'

        # Farm construction info
        self.action_text = 'Construct farm'
        self.buildings = ['Farm']

    def action(self, villager):
        '''Collect food'''

        # Check if a build is going to be build as first priority
        if villager.turn_action != None:

            # if building cannot be build return error
            build = villager.turn_action[0](
                                            villager.turn_action[1],
                                            villager.turn_action[2][0],
                                            villager.turn_action[2][1]
                                            )

            if build:
                
                # Run on creation functions for building
                villager.turn_action[1].on_creation()

                response = config.get_response('build_action_succeed')
                response[0] = response[0].format(villager.name, villager.turn_action[1].name)
                return response

            else:
                response = config.get_response('farmer_action_build_fail')
                response[0] = response[0].format(villager.name, villager.turn_action[1].name)
                return response

        else:

            # Check if the farm can work at a farm
            building = villager.work_building
            if building != None:

                # Get food from farm
                food = building.food
                config.food += food

                # Add food to the farm
                food_produced = random.randint(1,3) + config.food_weight
                max_food = (building.size[0]-2)*(building.size[1]-2)
                food_produced = max( min(food_produced, max_food), 0)

                self.villager_location_set(villager, food_produced)
                
                # Return output if food was produced
                if food > 0:
                    response = config.get_response('farmer_action')
                    response[0] = response[0].format(villager.name, food)
                    return response
        
    def villager_location_set(self, villager, crops=0):
        '''Places villager next to farm'''

        # Place villager next to farm is it exists, else place next to house
        if villager.work_building != None:
            
            building = villager.work_building

            # Reset house texture
            building.reset_texture(crops)

            # Update the texture on the map
            building.update_texture_map(True)

            # Find a suitable position next to the farm
            found_space = False
            while found_space == False:

                # Get position
                pos_x = random.randint(0, 1)
                pos_x = pos_x*( building.size[0]-1)
                pos_y = random.randint(1, building.size[1]-2)
                pos = pos_x + (pos_y*building.size[0])

                # Make sure space is free and not a coner position
                if building.texture[pos] == ' ':
                    
                    draw_villager(villager, pos_x+building.pos_x, pos_y+building.pos_y)

                    found_space = True

        else:
            draw_villager_home(villager)


class Feller(Profession):
    '''The Feller provides Wood for the village'''

    def __init__(self):
        
        # Inherit data
        Profession.__init__(self)

        # Villager info
        self.name = 'Feller'
        self.description = 'Provides 2-3 wood each turn'
        self.colour = 'dark goldenrod3'

    def action(self, villager):
        '''Collect Wood'''

        # Place villager in house
        draw_villager_home(villager)

        # Collect wood and add to logs
        wood_produced = random.randint(2,3)
        config.wood += wood_produced

        response = config.get_response('feller_action')
        response[0] = response[0].format(villager.name, wood_produced)
        return response

class Carpenter(Profession):
    '''The carpenter builds building with wood'''

    def __init__(self):
        
        # Inherit data
        Profession.__init__(self)

        # Villager info
        self.name = 'Carpenter'
        self.description = 'Constructs wooden buildings'
        self.colour = 'gold'

        self.action_text = 'Construct'

        # List of available buildings
        self.buildings = ('Wooden Hut',
                          'Wooden Statue')

    def action(self, villager):
        '''Build a building if the action was selected'''

        # Place villager in house
        draw_villager_home(villager)

        # Only attempt to build if action was seleceted
        if villager.turn_action != None:

            # if building cannot be build return error
            build = villager.turn_action[0](
                                            villager.turn_action[1],
                                            villager.turn_action[2][0],
                                            villager.turn_action[2][1]
                                            )

            if build:
                
                # Run on creation functions for building
                villager.turn_action[1].on_creation()

                response = config.get_response('build_action_succeed')
                response[0] = response[0].format(villager.name, villager.turn_action[1].name)
                return response

            else:
                response = config.get_response('carpenter_action_no_wood')
                response[0] = response[0].format(villager.name, villager.turn_action[1].name)
                return response
