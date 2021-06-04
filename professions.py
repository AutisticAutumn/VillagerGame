#
# Villager Game
# Professions Module
# Written by Madeline Autumn
# Last modified on 03/06/21
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
        
        food_produced = random.randint(2,4)
        config.food += food_produced

        return f'{villager.name} has produced {food_produced} food'

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

        return f'{villager.name} has produced {wood_produced} wood'
