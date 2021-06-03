#
# Villager Game
# Villager Module
# Written by Madeline Autumn
# Last modified on 03/06/21
#

### Imports and Varibles ###
import config
import random

### Villager class ###

class Villager:

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
