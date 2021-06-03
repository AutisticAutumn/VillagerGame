#
# Villager Game
# Config Module
# Written by Madeline Autumn
# Last modified on 03/06/21
#

def init():
    '''Initializes the global variables for the program'''

    # Stores the village houses and the villagers
    global village, villagers
    village = []
    villagers = []

    # Materials
    global food, wood
    food = 0
    wood = 0

    # Turn Log and  counter
    global log, turn
    log = ['Turn 1']
    turn = 1

def save():
    '''Save the variables into files'''

    # Save the logs
    with open('log.txt', 'w') as f:
        f.writelines(log)
