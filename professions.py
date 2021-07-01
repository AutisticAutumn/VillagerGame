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

def draw_villager_home(self, villager):
    '''Draws a villager into their house'''

    # Make sure villager has a house to display in
    if villager.house != None:
            
        # Reset house texture
        villager.house.reset_texture()

        # Set new texture as villager face
        pos = random.randint(7,8)

        villager.house.texture = list(villager.house.texture)
        villager.house.texture[pos] = '☺'
        villager.house.texture = ''.join(villager.house.texture)

        villager.house.colours.append(self.colour)
        villager.house.colour_map[pos-2] = len(villager.house.colours)-1
            
        # Update the texture on the map
        villager.house.update_texture_map()

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
        response = response.format(villager.name, building.name)
        villager.append_villager_log(response, 'lime')

    def villager_location_set(self, villager):
        '''Places the villager in there house for their action'''

        draw_villager_home(self, villager)
    

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
                return (response.format(villager.name, villager.turn_action[1].name), 'cyan')

            else:
                response = config.get_response('farmer_action_build_fail')
                return (response.format(villager.name, villager.turn_action[1].name), 'red')

        else:

            # Check if the farm can work at a farm
            if villager.work_building != None:

                # Get food from farm
                food = villager.work_building.food
                config.food += food

                # Add food to the farm
                food_produced = random.randint(1,3)
                self.villager_location_set(villager, food_produced)
                
                # Return output if food was produced
                if food > 0:
                    response = config.get_response('farmer_action')
                    return (response.format(villager.name, food), 'lime')
        
    def villager_location_set(self, villager, crops=0):
        '''Places villager next to farm'''

        # Place villager next to farm is it exists, else place next to house
        if villager.work_building != None:
            
            building = villager.work_building

            # Reset house texture
            building.reset_texture(crops)

            # Find a suitable position next to the farm
            found_space = False
            while found_space == False:

                # Get position
                pos_x = random.randint(0, 1)
                pos_y = random.randint(1, building.size[1]-2)
                pos = (pos_x*( building.size[0]-1) ) + (pos_y*building.size[0])

                # Make sure space is free and not a coner position
                if building.texture[pos] == ' ':

                    # Set new texture as villager face
                    building.texture = list(building.texture)
                    building.texture[pos] = '☺'
                    building.texture = ''.join(building.texture)

                    building.colours.append(self.colour)
                    building.colour_map[pos] = len(building.colours)-1

                    found_space = True
                
            # Update the texture on the map
            building.update_texture_map()

        else:
            draw_villager_home(self, villager)


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
        draw_villager_home(self, villager)

        # Collect wood and add to logs
        wood_produced = random.randint(2,3)
        config.wood += wood_produced

        response = config.get_response('feller_action')
        return (response.format(villager.name, wood_produced), 'chocolate')

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
        draw_villager_home(self, villager)

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
                return (response.format(villager.name, villager.turn_action[1].name), 'cyan')

            else:
                response = config.get_response('carpenter_action_no_wood')
                return (response.format(villager.name, villager.turn_action[1].name), 'red')
