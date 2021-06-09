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

        return (f'{villager.name} has produced {food_produced} food', 'lime')

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

        return (f'{villager.name} has produced {wood_produced} wood', 'lime')

class Carpenter:
    '''The carpenter builds building with wood'''

    def __init__(self):

        self.name = 'Carpenter'
        self.description = 'Constructs wooden buildings'
        self.ability = None

    def action(self, villager):
        # Collect Wood

        return (f'{villager.name} has produced {wood_produced} wood', 'cyan')
