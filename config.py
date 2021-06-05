#
# Villager Game
# Config Module
# Written by Madeline Autumn
# Last modified on 04/06/21
#

import random
import professions, buildings

# Initiate the global variables
def init():
    '''Initializes the global variables for the program'''

    # Villagers and housing
    global village, villagers
    village = []
    villagers = []

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
    global map_x1, map_x2, map_y1, map_y2, map
    map_x1 = 0
    map_y1 = 0
    map_x2 = 48
    map_y2 = 21
    map = {}

    # Turn Log and  counter
    global log, turn
    log = ['Turn 1']
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
                        professions.Feller()]

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

    if key == buildings.WoodenHut().name:
        return buildings.WoodenHut()

def save():
    '''Save the variables into files'''

    # Save the logs
    with open('log.txt', 'w') as f:
        for line in log:
            f.writelines(f'{line[0]}\n')

def create_map():
    '''Creates the blank map grid'''

    for y in range(1, map_y2-map_y1+1):
        for x in range(map_x2-map_x1):
            
            key = f'({y}:{x})'
            map.update({key : buildings.Grass()})
