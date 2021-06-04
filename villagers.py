#
# Villager Game
# Villager Module
# Written by Madeline Autumn
# Last modified on 04/06/21
#

### Imports and Varibles ###
import config, professions
import random

with open("villager_names", 'r') as f:
    names = f.readlines()
names = [n.strip() for n in names] 

### Villager class ###

class Villager:
    '''Class the stores the data for each villager'''

    def __init__(self, name, profession):

        self.name = name
        self.profession = profession

        # Villagers initial stats
        self.hunger = 0
        self.health_max = 12
        self.health = self.health_max

        self.log = []
        self.turn_log = []

    def end_turn(self):

        # Run action and log the action
        action = self.profession.action(self)
        if action != None:
            self.turn_log.append(action)
        
        # Add internal logs to the main log
        for action in self.turn_log:
            config.turn_log.append(action)
    
    def begin_turn(self):  
        '''Beginning of turn functions'''

        self.log.append(f'\nTurn {config.turn}')

        # Add turn log to main log and clear the turn log
        for line in self.turn_log:
            self.log.append(line)
        self.turn_log = []


def create_villager():
    '''Creates a randomized villager and to the village'''

    config.villagers.append(Villager(random.choice(names), professions.Unemployed()))
