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
        self.health = config.health_max
        self.happiness = 0

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

    def feed_villager(self):
        '''Feed the villager and calculate stats'''
        # Only caluate food if needed
        if self.hunger > 0:
            if config.food > 0:
                init_food = config.food
                config.food -= self.hunger
                self.hunger = 0
                if config.food < 0:
                    # Add back food and hunger so that food > 0
                    self.hunger += config.food*-1
                    config.food += config.food*-1
                food_consumed = init_food - config.food
                # Add result to log
                self.turn_log.append(f'{self.name} has consumed {food_consumed} food')
            else:
                # Add result to log
                self.turn_log.append(f'There is no food for {self.name} to consume')
                # Add hunger if no food was consumed
                self.add_hunger()

        else:
            # Add hunger if no food was consumed
            self.add_hunger()

    def add_hunger(self):
        '''Add hunger to villager and keep within bounds'''

        self.hunger += random.randint(config.hunger_range[0],
                                      config.hunger_range[1])
        self.hunger = min(self.hunger, config.hunger_max)

        self.lose_happiness(0,2)


    def lose_happiness(self, min, max):
        '''Calculate happiness loss and keep withing bounds'''

        self.happiness -= random.randint(min, max)
        self.happiness = max(min(self.happiness, config.happiness_max), config.happiness_min)


def create_villager():
    '''Creates a randomized villager and to the village'''

    config.villagers.append(Villager(random.choice(names), professions.Unemployed()))
