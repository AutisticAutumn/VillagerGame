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
    
    if key == MassPossession().name:
        return MassPossession()

def get_disaster_list():
    '''Returns a list of disasters'''

    list = [Famine().name,
            MassPossession().name]
        
    return list

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
    
    def on_end(self):
        pass

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

class MassPossession(Disaster):

    def __init__(self):

        self.name = 'MassPossession'
        self.weight = 3
        self.timer = random.randint(6,10)

    def on_start(self):
        
        # Return to logs
        response = config.get_response('mass_possession_begin')
        response[0] = response[0].format(config.village_name)
        config.main_app.append_log(response)

        # Possess villagers with a rate of 2/3 chance
        for village in config.villagers:
            if random.randint(1,3) < 3:
                village.get_possessed(3,7)
