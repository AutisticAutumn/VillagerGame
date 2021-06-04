#
# Villager Game
# Config Module
# Written by Madeline Autumn
# Last modified on 04/06/21
#

import professions

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

    # Turn Log and  counter
    global log, turn, turn_log
    log = ['Turn 1']
    turn = 1
    turn_log = []

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

    # Turn the list into a dictionary
    professions_dict = {}
    for profession in professions_list:
        professions_dict.update({profession.name : profession})

def save():
    '''Save the variables into files'''

    # Save the logs
    with open('log.txt', 'w') as f:
        for line in log:
            f.writelines(f'{line}\n')
