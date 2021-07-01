#
# Villager Game
# Villager Module
# Written by Madeline Autumn
#

### Imports and Varibles ###
import config, professions
import random
from tkinter import DISABLED, NORMAL

### Villager class ###

class Villager:
    '''Class the stores the data for each villager'''

    def __init__(self, name, profession):

        self.name = name
        self.profession = profession

        # Villagers initial stats
        self.hunger = 0
        self.health = config.health_max
        self.morale = 0

        # Villager Logs
        self.log = [(f'Turn {config.turn}', 'white')]
        self.turn_log = []

        # Turn action
        self.turn_action = None

        # Profession data
        self.profession_lock = 0
        self.work_building = None

        # Frame widget
        self.frame = None
        config.main_app.add_villager_frame(self)
        self.frame.update_stats()

        # Find house
        self.house = None
        self.house = self.find_house()

    ## Turn functions ##
    def end_turn(self):

        # Run profession action and log the action
        action = self.profession.action(self)
        if action != None:
            self.append_villager_log(action[0], action[1])
            
            # Lock profession for three turns if just assigned
            if self.profession_lock <= 0:
                self.profession_lock = 3
        
        # Random attack villagers if unhappy
        if self.morale < 0:
            if random.randint(1,48) <= self.morale**2:
                self.attack_villager()
    
    def begin_turn(self):  
        '''Beginning of turn functions'''

        # Appends new turn line directly to villager log
        self.log.append((f'\nTurn {config.turn+1}', 'white'))

        # Reset variables
        self.turn_log = []
        self.turn_action = None

        # Villager profession lock
        if self.profession_lock > 1:
            self.profession_lock -= 1
            self.frame.professions_menu.config(state=DISABLED)
        else:
            self.profession_lock = max(0 , self.profession_lock-1)
            self.frame.professions_menu.config(state=NORMAL)

        # Attempt to find a building if needed for work
        if self.profession.building != None and self.work_building == None: 
            self.assign_work_building()

    def append_villager_log(self, line, colour='white'):
        '''Appends a line to the villager log and prints to main log'''

        if not(line in self.turn_log):
            self.turn_log.append(line)
            self.log.append((line, colour))
            self.frame.parent.append_log(line, colour=colour)

    def update_profession(self, profession):
        '''Run functions for chaning a villagers profession'''
        
        # Remove villager from buildings related to old profession
        if self.house != None:
            self.house.reset_texture()
            self.house.update_texture_map()
        if self.work_building != None:
            self.work_building.reset_texture()

        # Change profession and upate appropriate stats
        self.profession = config.professions_dict[profession]
        self.frame.update_stats()

        # Reset stats associated with profession
        self.turn_action = None
        if self.work_building != None:
            self.work_building.worker = None
            self.work_building = None

        if self.profession.building != None:
            self.assign_work_building()


    ## Internal actions ##
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
                result = config.get_response('consume_food')
                result = result.format(self.name, food_consumed)
                self.append_villager_log(result,'yellow')
                # Gain morale from eating if below 0
                if self.morale < 0:
                    self.gain_morale(0,1)
            else:
                # Add result to log
                result = config.get_response('no_food_found').format(self.name)
                self.append_villager_log(result, 'red')
                # Add hunger if no food was consumed
                self.gain_hunger(True)

        else:
            # Add hunger if no food was consumed
            self.gain_hunger(False)
    
    def assign_work_building(self):
        '''Finds building for the villager to work in if required'''
        
        # Run through the list of buildings on the map and see if any match
        for building in config.map.map.values():
            
            # Check if building is the right type and free
            building_type = building.profession == self.profession.name
            building_free = building.worker == None

            if building_type and building_free:

                # Update stats for villager and building
                building.worker = self
                self.work_building = building
                
                # Return to logs
                response = config.get_response('find_work_building').format(self.name, building.name)
                self.append_villager_log(response, 'lime')

                break
        
        # Return to logs if failed
        if self.work_building == None:
            response = config.get_response('find_work_building_fail')
            response = response.format(self.name, self.profession.building)
            self.append_villager_log(response, 'red')

    def find_house(self):
        '''Finds a house for the villager if it has none'''

        # Run through the list of buildings on the map and see if any match
        for building in config.map.map.values():
            
            # Check if building is the right type and free
            building_type = building.type == 'House'
            if building_type:

                building_free = building.villager == None
                if building_free:

                    # Update stats for the building and return the building object
                    building.villager = self
                    self.profession.villager_location_set(self)

                    return building

    def attack_villager(self):
        '''Function for dealing with villager combat'''

        target = random.choice(config.villagers)
        damage = random.randint(1,4)
        
        # Return result
        if target == self:
            result = config.get_response('attack_self')
            result = result.format(self.name, damage)
        else:
            result = config.get_response('attack_villager')
            result = result.format(self.name, target.name, damage)
            target_result = config.get_response('target_villager')
            target_result.format(self.name, target.name, damage)
            target.log.append((target_result, 'red2'))
        self.append_villager_log(result, 'red')
        
        target.lose_health(damage, damage)

    ## Hunger functions ##
    def gain_hunger(self, lose_morale):
        '''Add hunger to villager and keep within bounds'''

        self.hunger += random.randint(config.hunger_range[0],
                                      config.hunger_range[1])
        
        # Check boundries
        if self.hunger > config.hunger_max:
            self.hunger = config.hunger_max
    
        self.return_hunger_log()

        # Lose morale if requested
        if lose_morale:
            self.lose_morale(0,2)

    def return_hunger_log(self):
        '''Return an output to the logs depending on hunger level'''

        result = None
        if self.hunger >= config.hunger_log_boundry[0]:
            result = (config.get_response('starving').format(self.name), 'red')
        elif self.hunger >= config.hunger_log_boundry[1]:
            result = (config.get_response('hungry').format(self.name), 'yellow')

        if result != None:
            self.append_villager_log(result[0], result[1])

    ## Morale functions ##
    def gain_morale(self, min, max):
        '''Calculate morale loss and keep within bounds'''

        self.morale += random.randint(min, max)

        # Check boundries 
        if self.morale > config.morale_max:
            self.morale = config.morale_max

        self.return_morale_log()


    def lose_morale(self, min, max):
        '''Calculate morale loss and keep within bounds'''

        self.morale -= random.randint(min, max)

        # Check boundries
        if self.morale < config.morale_min:
            self.morale = config.morale_min

        self.return_morale_log()

    def return_morale_log(self):
        '''Return an output to the logs depending on morale level'''

        result = None

        if self.morale <= config.morale_log_boundry[0]:
            result = (config.get_response('very_low_morale').format(self.name),
                      'medium orchid')
        elif self.morale <= config.morale_log_boundry[1]:
            result = (config.get_response('low_morale').format(self.name),
                      'medium orchid')
        elif self.morale <= config.morale_log_boundry[2]:
            result = (config.get_response('dropping_morale').format(self.name),
                      'medium orchid')
        elif self.morale >= config.morale_log_boundry[3]:
            result = (config.get_response('high_morale').format(self.name), 'cyan')
        elif self.morale >= config.morale_log_boundry[4]:
            result = (config.get_response('very_high_morale').format(self.name),
                      'cyan')

        if result != None:
            self.append_villager_log(result[0], result[1])

    ## Health functions ##
    def lose_health(self, min, max):
        '''Calculate health loss'''

        self.health -= random.randint(min, max) 

        self.return_health_log()

        # Kill if out of bounds
        if self.health <= 0:
            self.kill()
        else:
            # Lose morale as result of injury
            self.lose_morale(1,2)

    def return_health_log(self):
        '''Return output to the log based on health'''

        result = None

        if self.health <= config.health_log_boundry[0]:
            result = config.get_response('near_death').format(self.name)
        elif self.health <= config.health_log_boundry[1]:
            result = config.get_response('hurt_severe').format(self.name)
        elif self.health <= config.health_log_boundry[2]:
            result = config.get_response('hurt_moderate').format(self.name)
        elif self.health <= config.health_log_boundry[3]:
            result = config.get_response('hurt_mild').format(self.name)
        
        if result != None:
            self.append_villager_log(result, 'red')

    def kill(self):
        '''Kills the villager'''

        # Remove frame from screen
        self.frame.frame.grid_forget()
        self.frame.parent.villager_frames.remove(self.frame)

        # Remove self from buildings if needed
        if self.work_building != None:
            self.work_building.worker = None
            self.work_building.reset_texture()
            self.work_building.update_texture_map()

        if self.house != None:
            self.house.villager = None
            self.house.reset_texture()
            self.house.update_texture_map()

        # Add death to logs
        response = config.get_response('death').format(self.name)
        self.append_villager_log(response, 'red')

        # Remove self from villager list
        config.villagers.remove(self)
