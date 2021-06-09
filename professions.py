#
# Villager Game
# Professions Module
# Written by Madeline Autumn
# Last modified on 09/06/21
#

### Imports and variables ###
import config
import random

### Professions ###

class Unemployed:
    '''Unemployed villagers provide no materials or bonuses but can build buildings'''

    def __init__(self):

        self.name = 'Unemployed'
        self.description = ''
        self.ability = None

    def action(self, villager):
        pass

class Farmer:
    '''The farmer provides foods for the village at Farms'''

    def __init__(self):

        self.name = 'Farmer'
        self.description = 'Provides 2-4 food each turn'
        self.ability = None

    def action(self, villager):
        # Collect food
        
        food_produced = random.randint(1,3)
        config.food += food_produced

        response = config.get_response('farmer_action')
        return (response.format(villager.name, food_produced), 'lime')

class Feller:
    '''The Feller provides Wood for the village'''

    def __init__(self):

        self.name = 'Feller'
        self.description = 'Provides 2-3 wood each turn'
        self.ability = None

    def action(self, villager):
        # Collect Wood

        wood_produced = random.randint(2,3)
        config.wood += wood_produced

        response = config.get_response('feller_action')
        return (response.format(villager.name, wood_produced), 'lime')

class Carpenter:
    '''The carpenter builds building with wood'''

    def __init__(self):

        self.name = 'Carpenter'
        self.description = 'Constructs wooden buildings'
        self.ability = None

    def action(self, villager):
        # Build a building if the action was selected

        response = config.get_response('carpenter_action')
        return (response.format(villager.name), 'cyan')
