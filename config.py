#
# Villager Game
# Config Module
# Written by Madeline Autumn
# Last modified on 03/06/21
#

def init():
    '''Initializes the global variables for the program'''

    # Villagers and housing
    global village, villagers, professions
    village = []
    villagers = []
    professions = ['Unemployed', 'Farmer', 'Feller']

    # Materials
    global food, wood
    food = 0
    wood = 0

    # Turn Log and  counter
    global log, turn, turn_log
    log = ['Turn 1']
    turn = 1
    turn_log = []

def save():
    '''Save the variables into files'''

    # Save the logs
    with open('log.txt', 'w') as f:
        f.writelines(log)
