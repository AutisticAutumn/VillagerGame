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

class Unemployed:
    '''Unemployed villagers provide no materials or bonuses but can build buildings'''

    def __init__(self):

        # Villager info
        self.name = 'Unemployed'
        self.description = ''

    def action(self, villager):
        pass

class Farmer:
    '''The farmer provides foods for the village at Farms'''

    def __init__(self):

        # Villager info
        self.name = 'Farmer'
        self.description = 'Provides 2-4 food each turn'

    def action(self, villager):
        '''Collect food'''
        
        food_produced = random.randint(1,3)
        config.food += food_produced

        response = config.get_response('farmer_action')
        return (response.format(villager.name, food_produced), 'lime')

class Feller:
    '''The Feller provides Wood for the village'''

    def __init__(self):

        # Villager info
        self.name = 'Feller'
        self.description = 'Provides 2-3 wood each turn'

    def action(self, villager):
        '''Collect Wood'''

        wood_produced = random.randint(2,3)
        config.wood += wood_produced

        response = config.get_response('feller_action')
        return (response.format(villager.name, wood_produced), 'lime')

class Carpenter:
    '''The carpenter builds building with wood'''

    def __init__(self):
        
        # Villager info
        self.name = 'Carpenter'
        self.description = 'Constructs wooden buildings'

        self.action_text = 'Construct'

    def action(self, villager):
        '''Build a building if the action was selected'''

        # Only attempt to build if action was seleceted
        if villager.turn_action != None:
            # if building cannot be build return error
            print(
                  villager.turn_action[1],
                  villager.turn_action[2][0],
                  villager.turn_action[2][1]
                  )
            build = villager.turn_action[0](
                                            villager.turn_action[1],
                                            villager.turn_action[2][0],
                                            villager.turn_action[2][1]
                                            )
            if build:
                response = config.get_response('carpenter_action_succeed')
                return (response.format(villager.name, villager.turn_action[1].name), 'cyan')
            else:
                response = config.get_response('carpenter_action_no_wood')
                return (response.format(villager.name, villager.turn_action[1].name), 'orange')

    def turn_action(self, villager):
        '''Opens the popout for the placement'''

        building = config.get_building('Wooden Statue')

        config.map.popout.villager = villager
        config.map.popout.building = building
        config.map.popout.create_toplevel()

    def turn_action_popout_closed(self, villager, building, pos):
        '''Runs the functions for when the popout closes'''

        # Set the action for the villager
        villager.turn_action = (config.map.build_building, building, pos)

        # Return output to logs
        response = config.get_response('carpenter_turn_action')
        response = response.format(villager.name, building.name)
        villager.append_villager_log(response, 'lime')
    
