#
# Villager Game
# Villager Module
# Written by Madeline Autumn
#

### Imports and Varibles ###
import config, professions, mapUI
import random, math
from tkinter import DISABLED, NORMAL

### Villager class ###

class Villager:
    '''Class the stores the data for each villager'''

    def __init__(self, name, profession, move=True):

        self.name = name
        self.profession = profession

        # Villagers initial stats
        self.hunger = 0
        self.health = config.health_max
        self.morale = 0

        # Phantom status
        self.phantom = None
        self.phantom_timer = 0

        # Villager Logs
        response = config.get_response('new_turn')
        response[0] = response[0].format(config.turn).strip()
        self.log = [response]
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

        # Map data
        self.pos = (None, None)
        self.texture = config.villager_textures[0]
        self.colour = None

        # Move to random position at start
        if move:
            self.random_movement()

        # Find house
        self.house = None
        self.house = self.find_house()

        # Draw the villager into the new positon
        self.draw_villager()

    ## Map Functions ##

    def draw_villager(self):
        '''Draw the villagers onto the map'''

        # Get colour
        self.colour = self.get_colour()
        
        # Update map
        if not(self.pos[0]) == None:
            self.frame.update_map()
            mapUI.draw_map(config.map.frame)

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
                response = config.get_response('find_work_building')
                response[0] = response[0].format(self.name, building.name)
                self.append_villager_log(response)

                break
        
        # Return to logs if failed
        if self.work_building == None:
            response = config.get_response('find_work_building_fail')
            response[0] = response[0].format(self.name, self.profession.building)
            self.append_villager_log(response)

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
                    self.in_house = True
                    self.profession.villager_location_set(self)

                    return building

        self.in_house = False

    ## Turn functions ##
    def end_turn(self):

        # Run profession action and log the action
        if not(self.phantom):
            action = self.profession.action(self)
            if action != None:
                self.append_villager_log(action)
                
                # Lock profession for three turns if just assigned
                if self.profession_lock <= 0:
                    self.profession_lock = 3
        else:
            # Create a phantom response
            response = random.choice(config.phantom_responses)
            if response[1] == 1:
                response = config.get_response(response[0])
                response[0] = response[0].format(self.name)
            else:
                response = config.get_response(response[0])
                response[0] = response[0].format(self.name, random.randint(1,4))
            self.append_villager_log(response, True)

            # Move phantom villager
            self.random_movement()

        # Random attack villagers if unhappy
        if self.morale < 0 and not(self.phantom):
            if random.randint(1,48) <= self.morale**2:
                self.attack_villager()
        elif self.phantom:
            if random.randint(1,4) == 1:
                self.attack_villager()
    
    def begin_turn(self):  
        '''Beginning of turn functions'''

        # Appends new turn line directly to villager log
        response = config.get_response('new_turn')
        response[0] = '\n' + response[0].format(config.turn)
        self.log.append(response)

        # Reset variables
        self.turn_log = []
        self.turn_action = None

        # Attempt to possess villager
        if self.phantom == None:
            if random.randint(1, config.phantom_chance) == 1:
                self.get_possessed()
        
        # Remove phantom status if phantom
        if self.phantom:
            if self.phantom_timer < 1:
                self.get_unpossessed()
            else:
                self.phantom_timer -= 1

        # Villager profession lock
        if self.profession_lock > 1 or self.phantom:
            self.profession_lock -= 1
            self.frame.professions_menu.config(state=DISABLED)
        else:
            self.profession_lock = max(0 , self.profession_lock-1)
            self.frame.professions_menu.config(state=NORMAL)

        # Attempt to find a building if needed for work
        if not(self.phantom):
            if self.profession.building != None and self.work_building == None: 
                self.assign_work_building()

    def append_villager_log(self, response, phantom_response=False):
        '''Appends a line to the villager log and prints to main log'''

        if self.phantom:
            if not(phantom_response):
                return None
        
        if not(response in self.turn_log):
            self.turn_log.append(response)
            self.log.append(response)
            self.frame.parent.append_log(response)

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

        # Update villagers onscreen texture
        self.profession.villager_location_set(self)

    ## Internal actions ##
    def get_colour(self):
        '''Get the villagers colour'''

        if self.phantom:
            return 'pale turquoise2'
        elif self.health <= config.health_log_boundry[1]:
            return 'red'
        else:
            return self.profession.colour

    def get_possessed(self, timer_min=6, timer_max=12):
        '''Runs code for when a villager gets possessed'''

        # Adjust stats
        self.phantom = True
        self.phantom_timer = random.randint(timer_min, timer_max)
        self.texture = config.villager_textures[1]
        self.colour = 'pale turquoise2'
        self.draw_villager()

        # Adjust ui
        try:
            self.frame.action_button.config(state=DISABLED)
        except:
            pass

        # Return to logs
        response = config.get_response('get_possessed')
        response[0] = response[0].format(self.name)
        self.append_villager_log(response, True)

    def get_unpossessed(self):
        '''Runs code for when a villager gets unpossessed'''

        # Adjust stats
        self.phantom = None
        self.texture = config.villager_textures[0]
        self.colour = None
        self.draw_villager()

        # Adjust ui
        try:
            self.frame.action_button.config(state=NORMAL)
        except:
            pass

        # Return to logs
        response = config.get_response('get_unpossessed')
        response[0] = response[0].format(self.name)
        self.append_villager_log(response)
    
    def random_movement(self):
        '''Randomly moves near another villager if needed'''

        if len(config.villagers) == 1:
            self.draw_villager()
        else:
            # Lock onto the position of a villager
            target_found = False
            while not(target_found):
                target = random.choice(config.villagers)

                if target != self:
                    target_found = True

            # Get list of villager positions
            villager_positions = {}
            for villager in config.villagers:
                villager_positions.update({villager.pos: villager})

            # Find position around target villager
            position_found = False
            delta_real = 3.0
            while not(position_found):
                
                # Get variables
                delta = math.floor(delta_real)

                x = target.pos[0] + random.randint(delta*-1, delta)
                y = target.pos[1] + random.randint(delta*-1, delta)

                pos = x + ((y-1)*config.map.width)
                pos_key = f'({y}.{x-1})'

                # Check to see if tile is valid
                #  Check if tile is within map
                if x < config.map.width-1 or x > 0:
                    if y < config.map.height-1 or y > 0:
                        

                        # Check if tile is empty     
                        pos_key = f'({y}:{x})'
                        pos = (x) + ((y-1)*config.map.width)

                        no_villager = not((x, y) in villager_positions.keys())
                        no_building = not(pos_key in config.map.map.keys())
                        terrain_grass = config.map.terrain_map[pos] == 'Grass'
                        
                        if no_villager and no_building and terrain_grass:
                            position_found = True
                
                # If no tile was found increase search range
                delta_real += 0.2

            # Move villager
            self.pos = (x, y)
            self.draw_villager()
    
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
                result[0] = result[0].format(self.name, food_consumed)
                self.append_villager_log(result)
                # Gain morale from eating if below 0
                if self.morale < 0:
                    self.gain_morale(0,1)
            else:
                # Add result to log
                result = config.get_response('no_food_found')
                result[0] = result[0].format(self.name)
                self.append_villager_log(result)

                # Add hunger if no food was consumed
                self.gain_hunger(True)

        else:
            # Add hunger if no food was consumed
            self.gain_hunger(False)

    def attack_villager(self):
        '''Function for dealing with villager combat'''

        target = random.choice(config.villagers)
        damage = random.randint(1,4)
        
        # Return result
        if target == self:
            result = config.get_response('attack_self')
            result[0] = result[0].format(self.name, damage)
        else:
            result = config.get_response('attack_villager')
            result[0] = result[0].format(self.name, target.name, damage)

            target_result = config.get_response('target_villager')
            target_result[0] = target_result[0].format(self.name, target.name, damage)
            target.log.append(target_result)

        self.append_villager_log(result)
        
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
            result = config.get_response('starving')
            result[0] = result[0].format(self.name)
            self.lose_health(-1, 2)
        elif self.hunger >= config.hunger_log_boundry[1]:
            result = config.get_response('hungry')
            result[0] = result[0].format(self.name)

        if result != None:
            self.append_villager_log(result)

    ## Morale functions ##
    def gain_morale(self, min, max):
        '''Calculate morale loss and keep within bounds'''

        morale_change = random.randint(min, max)
        
        if morale_change > 0:
            self.morale += morale_change

            # Check boundries 
            if self.morale > config.morale_max:
                self.morale = config.morale_max

            # Add change in morale to logs
            result = config.get_response('rising_morale')

            result[0] = result[0].format(self.name, morale_change)

            # Return to logs
            self.append_villager_log(result)
            self.return_morale_log('Rising')


    def lose_morale(self, min, max):
        '''Calculate morale loss and keep within bounds'''

        morale_change = random.randint(min, max)

        if morale_change > 0:
            self.morale -= morale_change

            # Check boundries
            if self.morale < config.morale_min:
                self.morale = config.morale_min

            # Add change in morale to logs
            result = config.get_response('dropping_morale')
            result[0] = result[0].format(self.name, morale_change)
            
            # Return to logs
            self.append_villager_log(result)
            self.return_morale_log('Dropping')

    def return_morale_log(self, dir=True):
        '''Return an output to the logs depending on morale level'''

        result = None

        boundries = [
                     self.morale <= config.morale_log_boundry[0],
                     self.morale <= config.morale_log_boundry[1],
                     self.morale <= config.morale_log_boundry[2],
                     self.morale >= config.morale_log_boundry[3],
                     self.morale >= config.morale_log_boundry[4]
                    ]

        if boundries[0] and (dir == 'Dropping' or dir):
            result = config.get_response('very_low_morale')
            result[0] = result[0].format(self.name)
        elif boundries[1] and (dir == 'Dropping' or dir):
            result = config.get_response('low_morale')
            result[0] = result[0].format(self.name)
        elif boundries[2] and (dir == 'Dropping' or dir):
            result = config.get_response('slightly_low_morale')
            result[0] = result[0].format(self.name)
        elif boundries[3] and (dir == 'Rising' or dir):
            result = config.get_response('high_morale')
            result[0] = result[0].format(self.name)
        elif boundries[4] and (dir == 'Rising' or dir):
            result = config.get_response('very_high_morale')
            result[0] = result[0].format(self.name)

        if result != None:
            self.append_villager_log(result)

    ## Health functions ##
    def lose_health(self, min, max):
        '''Calculate health loss'''

        health_change = random.randint(min, max) 
        
        if health_change > 0:
            self.health -= health_change

            # Add change in health to logs
            result = config.get_response('get_hurt')
            result[0] = result[0].format(self.name, health_change)

            self.append_villager_log(result, True)
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
        start_colour = self.colour

        if self.health <= config.health_log_boundry[0]:
            result = config.get_response('near_death')
            result[0] = result[0].format(self.name)
        elif self.health <= config.health_log_boundry[1]:
            result = config.get_response('hurt_severe')
            result[0] = result[0].format(self.name)
        elif self.health <= config.health_log_boundry[2]:
            result = config.get_response('hurt_moderate')
            result[0] = result[0].format(self.name)
            self.colour = None
        elif self.health <= config.health_log_boundry[3]:
            result = config.get_response('hurt_mild')
            result[0] = result[0].format(self.name)
            self.colour = None
        
        # Update texture if changed
        if start_colour != self.colour:
            self.draw_villager()

        if result != None:
            self.append_villager_log(result, True)

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
        response = config.get_response('death')
        response[0] = response[0].format(self.name)
        self.append_villager_log(response)

        # Remove self from villager list
        config.villagers.remove(self)
