#
# Villager Game
# Disaster Module
# Written by Madeline Autumn
#

### Importants and Varibles ###

import random
import config

### Functions
def get_disaster(key):
    '''Returns a unique disaster object based on key input'''

    if key == Famine().name:
        return Famine()

### Disasters ###

class Disaster():
    '''Generic class for disasters that holds mostly empty functions
        Empty functions exist in case a disaster does not hold a custom 
         function in it's place'''


    def __init__(self):
        pass

    def begin_turn(self):
        '''End disaster if timer is over'''

        if self.timer <= 0:
            self.on_end()
            config.disaster = None
            config.disaster_chance = config.disaster_chance_max
    
    def end_turn(self):
        '''Lower disaster timer'''

        self.timer -= 1

class Famine(Disaster):

    def __init__(self):

        self.name = 'Famine'
        self.weight = 10
        self.timer = random.randint(4,8)

    def on_start(self):
        '''Lower total food produced and send to logs'''

        self.food_loss = random.randint(1,2)
        config.food_weight -= self.food_loss

        response = config.get_response('famine_begin')
        config.main_app.append_log(response)
    
    def on_end(self):
        '''Reset food production and send to logs'''

        config.food_weight += self.food_loss 

        response = config.get_response('famine_end')
        config.main_app.append_log(response)
