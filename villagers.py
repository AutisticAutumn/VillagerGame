#
# Villager Game
# Villager Module
# Written by Madeline Autumn
# Last modified on 03/06/21
#

### Imports and Varibles ###
import config, professions
import random

with open("villager_names", 'r') as f:
    names = f.readline
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

    def end_turn(self):
        
        # Calculate stat changes
        self.hunger += random.randint(1,3)
        
        # Run action and log the action
        self.log.append(self.profession.action(self))
        config.turn_log.append(self.log[-1])

def create_villager():
    '''Creates a randomized villager and to the village'''

    config.villagers.append(Villager(random.choice(names), professions.Unemployed()))
