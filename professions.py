#
# Villager Game
# Professions Module
# Written by Madeline Autumn
#

### Imports and variables ###
import config
import map
import random

### Professions ###

class Profession:
    '''Main profession class that deals with globals'''

    def __init__(self):

        self.building = None

    def action(self, villager):
        pass
    
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
    

class Unemployed(Profession):
    '''Unemployed villagers provide no materials or bonuses but can build buildings'''

    def __init__(self):

        # Inherit data
        Profession.__init__(self)

        # Villager info
        self.name = 'Unemployed'
        self.description = ''

class Farmer(Profession):
    '''The farmer provides foods for the village at Farms'''

    def __init__(self):

        # Inherit data
        Profession.__init__(self)

        # Villager info
        self.name = 'Farmer'
        self.description = 'Provides 2-4 food each turn'
        self.building = 'Farm'

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
                villager.work_building.reset_texture(food_produced)
                
                # Return output if food was produced
                if food > 0:
                    response = config.get_response('farmer_action')
                    return (response.format(villager.name, food), 'lime')

class Feller(Profession):
    '''The Feller provides Wood for the village'''

    def __init__(self):
        
        # Inherit data
        Profession.__init__(self)

        # Villager info
        self.name = 'Feller'
        self.description = 'Provides 2-3 wood each turn'

    def action(self, villager):
        '''Collect Wood'''

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

        self.action_text = 'Construct'

        # List of available buildings
        self.buildings = ('Wooden Hut',
                          'Wooden Statue')

    def action(self, villager):
        '''Build a building if the action was selected'''

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
