#
# Villager Game
# Config Module
# Written by Madeline Autumn
#

import random
import professions, buildings, map
import villagers as villagers_scr

# Initiate the global variables
def init():
    '''Initializes the global variables for the program'''
    
    # Random seeds
    global seed, grass_seed
    seed = random.randint(1000000000,9999999999)
    random.seed(seed)
    grass_seed = random.randint(1000000000,9999999999)

    # Villagers and housing
    global village, villagers
    village = []
    villagers = []

    # Village stats
    global max_villagers, arrival_chance
    max_villagers = 0
    arrival_chance = 0.25

    # Villager names
    global names
    with open("villager_names", 'r') as f:
        names = f.readlines()
    names = [n.strip() for n in names] 

    # Villager stat boundries
    global health_max, hunger_max
    health_max = 8
    hunger_max = 8

    global happiness_max, happiness_min
    happiness_max = 4
    happiness_min = -4

    # Boundries for when villages returns logs for high stats
    # Stats at most extreme to least
    global happiness_log_boundry, hunger_log_boundry, health_log_boundry
    happiness_log_boundry = [-4, -3, -1, 2, 4]
    hunger_log_boundry = [7, 4]
    health_log_boundry = [1, 3, 5, 7]

    # Materials
    global food, wood
    food = 10
    wood = 0

    # Map
    global map
    map = map.Map()

    # Turn Log and counter
    global log, turn
    log = []
    turn = 1

    # Food priority 
    global food_priority_values, food_priority, hunger_range
    food_priority_values = ('High', 'Normal', 'Low')
    food_priority = [[],[],[]]
    hunger_range = (1, 3)

    # Professions Dictionary
    global professions_dict
    professions_list = [professions.Unemployed(),
                        professions.Farmer(),
                        professions.Feller(),
                        professions.Carpenter()]

    professions_dict = {}
    for profession in professions_list:
        professions_dict.update({profession.name : profession})

    # Create the list of responses
    get_responses_dict()

def get_responses_dict():
    '''Produce the dictionary of villager responses'''

    global response_dict
    response_dict = {}

    # Open file with the responses
    with open('villagerResponses', 'r') as f:
        
        lines = f.readlines()

        mode = 'FindEntry'
        key = ''
        values = []

        for line in lines:

            # Check for the next { to begin writing the next dictonary statement
            if mode == 'FindEntry':
                if line.strip() == '{':
                    mode = 'GetKey'
            # Find the key for the dictonary item
            elif mode == 'GetKey':
                key = line.strip()
                mode = 'GetValues'
            # Get the values for the dictonary
            elif mode == 'GetValues':
                # If end of entry find the next item
                if line.strip() == '}':
                    response_dict[key] = values
                    key = ''
                    values = []
                    mode = 'FindEntry'
                else:
                    values.append(line.strip())

def get_response(key):
    '''Return a randomized response from the response dictionary'''

    return random.choice(response_dict[key])

def get_building(key):
    '''Returns a unique building object based on input'''

    if key == buildings.Grass().name:
        return buildings.Grass()
    
    if key == buildings.WoodenHut().name:
        return buildings.WoodenHut()
    
    if key == buildings.WoodenStatue().name:
        return buildings.WoodenStatue()


def create_villager():
    '''Creates a randomized villager and to the village'''

    villagers.append(villagers_scr.Villager(random.choice(names), professions.Unemployed()))


def save():
    '''Save the variables into files'''

    # Save the logs
    with open('log.txt', 'w') as f:
        for line in log:
            f.writelines(f'{line[0]} : ({line[1]})\n')
