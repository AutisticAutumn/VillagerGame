#
# Villager Game
# Config Module
# Written by Madeline Autumn
#

import random
import professions, buildings, map, gameApp
import villagers as villagers_scr

# Initiate the global variables
def init():
    '''Initializes the global variables for the program'''
    
    ## Misc ##
    # Random seeds
    global seed, grass_seed
    seed = random.randint(1000000000,9999999999)
    random.seed(seed)
    grass_seed = random.randint(1000000000,9999999999)

    ## Villagers ##
    # Villagers and housing
    global villagers
    villagers = []

    # Village stats
    global max_villagers, arrival_chance
    max_villagers = 0
    arrival_chance = 0.25

    # Villager names
    global names
    names = read_file('villager_names')

    # Villager stat boundries
    global health_max, hunger_max
    health_max = 8
    hunger_max = 8

    global morale_max, morale_min
    morale_max = 4
    morale_min = -4

    # Food priority 
    global food_priority_values, food_priority, hunger_range
    food_priority_values = ('High', 'Normal', 'Low')
    food_priority = [[],[],[]]
    hunger_range = (1, 3)

    ## Misc Village ##

    # Weight for food produced
    global food_weight
    food_weight = -2

    # Boundries for when villages returns logs for high stats
    # Stats at most extreme to least
    global morale_log_boundry, hunger_log_boundry, health_log_boundry
    morale_log_boundry = [-4, -3, -1, 2, 4]
    hunger_log_boundry = [7, 4]
    health_log_boundry = [1, 3, 5, 7]

    ## Stats ##
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

    ## Dictionaries ##
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
    global response_dict
    response_dict = read_file('Responses')

def init_app():
    '''Creates the application globals'''
    
    # Game ui
    global main_app
    main_app = gameApp.GameApp()

def read_file(file):
    '''Produce the dictionary of villager responses'''

    response_dict = {}

    # Open file with the responses
    with open(file, 'r') as f:
        
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
    
    # Return the final file
    return response_dict

def get_response(key):
    '''Return a randomized response from the response dictionary'''

    return random.choice(response_dict[key])

def get_building(key):
    '''Returns a unique building object based on input'''

    if key == buildings.Grass().name:
        return buildings.Grass()

    if key == buildings.PondWater().name:
        return buildings.PondWater()
    
    if key == buildings.WoodenHut().name:
        return buildings.WoodenHut()
    
    if key == buildings.WoodenStatue().name:
        return buildings.WoodenStatue()

    if key == buildings.Farm().name:
        return buildings.Farm()


def create_villager():
    '''Creates a randomized villager and to the village'''

    name = random.choice(names['First']) + ' ' + random.choice(names['Last'])

    villagers.append(villagers_scr.Villager(name, professions.Unemployed()))


def save():
    '''Save the variables into files'''

    # Save the logs
    with open('log.txt', 'w') as f:
        for line in log:
            f.writelines(f'{line[0]} : ({line[1]})\n')
