#
# Villager Game
# Professions Module
# Written by Madeline Autumn
#

### Imports and variables ###
from buildings import Building
import config, map, mapUI
import random, math

### Functions ###

def draw_villager(villager, pos_x, pos_y):
    '''Draws the villager from set building positions'''
    
    villager.pos = (pos_x, pos_y)
    villager.draw_villager()

def get_professions_dict():
    '''Returns the dictionary of professions'''

    professions_list = [Unemployed(),
                        Farmer(),
                        Feller(),
                        Carpenter(),
                        Plantsman(),
                        Miner()]

    professions_dict = {}
    for profession in professions_list:
        professions_dict.update({profession.name : profession})

    return professions_dict

### Professions ###

class Profession:
    '''Main profession class that deals with globals'''

    def __init__(self):

        self.building = None

    def action(self, villager):
        '''Place villager in house if nothing else occurs'''

        self.villager_location_set(villager)
        
    
    def turn_action(self, villager):
        '''Opens the popout for the placement'''

        building = config.get_building(self.buildings[0])

        config.map.popout.villager = villager
        config.map.popout.building = building
        config.map.popout.create_toplevel()

    def turn_action_popout_closed(self, villager, building, pos):
        '''Runs the functions for when the popout closes'''

        # Set the action for the villager
        villager.turn_action = (config.map.build_building, building, pos)

        # Return output to logs
        response = config.get_response('build_turn_action')
        response[0] = response[0].format(villager.name, building.name)
        villager.append_villager_log(response)

    def villager_location_set(self, villager):
        '''Places the villager in there house for their action'''

        self.draw_villager_home(villager)
    
    def draw_villager_home(self, villager):
        '''Draws a villager into their house'''

        # Make sure villager has a house to display in
        if villager.house != None:
                
            # Reset house texture
            villager.house.update_texture_map(True)

            # Set new texture as villager face
            pos_change = random.randint(1,2)
            pos_x = villager.house.pos_x + pos_change
            pos_y = villager.house.pos_y + 1

            draw_villager(villager, pos_x, pos_y)

            villager.in_house = True
    
    def get_price_modifier(self, villager):
        '''Returns price changes based on skill'''

        return 1-(villager.skills[self.name]-2)*0.125

    def get_harvest_modifier(self, villager, value):
        '''Returns modified resource collection based on skill'''

        skill_difference = ((villager.skills[self.name]-2)*0.2)+1

        if random.randint(0,1) == 0:
            value = math.ceil(value*skill_difference)
        else:
            value = math.floor(value*skill_difference)

        return value
    

class Unemployed(Profession):
    '''Unemployed villagers provide no materials or bonuses but can build buildings'''

    def __init__(self):

        # Inherit data
        Profession.__init__(self)

        # Villager info
        self.name = 'Unemployed'
        self.description = ''
        self.colour = 'light grey'

class Farmer(Profession):
    '''The farmer provides foods for the village at Farms'''

    def __init__(self):

        # Inherit data
        Profession.__init__(self)

        # Villager info
        self.name = 'Farmer'
        self.description = 'Provides 2-4 food each turn'
        self.building = 'Farm'
        self.colour = 'green yellow'

        # Farm construction info
        self.action_text = 'Construct farm'
        self.buildings = ['Farm']

    def action(self, villager):
        '''Collect food'''

        # Check if a build is going to be build as first priority
        if villager.turn_action != None:

            price_mod = self.get_price_modifier(villager)

            # if building cannot be build return error
            build = villager.turn_action[0](
                                            villager.turn_action[1],
                                            villager.turn_action[2][0],
                                            villager.turn_action[2][1],
                                            price_mod=price_mod
                                            )

            if build:
                
                # Run on creation functions for building
                villager.turn_action[1].on_creation()

                response = config.get_response('build_action_succeed')
                response[0] = response[0].format(villager.name, villager.turn_action[1].name)
                return response

            else:
                response = config.get_response('farmer_action_build_fail')
                response[0] = response[0].format(villager.name, villager.turn_action[1].name)
                return response

        else:

            # Check if the farm can work at a farm
            building = villager.work_building
            if building != None:

                # Get food from farm
                food = building.food
                config.food += food

                # Add food to the farm
                food_produced = random.randint(1,3) + config.food_weight

                food_produced = self.get_harvest_modifier(villager, food_produced)

                max_food = (building.size[0]-2)*(building.size[1]-2)
                food_produced = max( min(food_produced, max_food), 0)

                self.villager_location_set(villager, food_produced)
                
                # Return output if food was produced
                if food > 0:
                    response = config.get_response('farmer_action')
                    response[0] = response[0].format(villager.name, food)
                    return response
        
    def villager_location_set(self, villager, crops=0):
        '''Places villager next to farm'''

        # Place villager next to farm is it exists, else place next to house
        if villager.work_building != None:
            
            building = villager.work_building

            # Reset house texture
            building.reset_texture(crops)

            # Update the texture on the map
            building.update_texture_map(True)

            # Find a suitable position next to the farm
            found_space = False
            while found_space == False:

                # Get position
                pos_x = random.randint(0, 1)
                pos_x = pos_x*( building.size[0]-1)
                pos_y = random.randint(1, building.size[1]-2)
                pos = pos_x + (pos_y*building.size[0])

                # Make sure space is free and not a coner position
                if building.texture[pos] == ' ':
                    
                    villager.house.update_texture_map(True)
                    draw_villager(villager, pos_x+building.pos_x, pos_y+building.pos_y)
                    villager.in_house = False

                    found_space = True

        else:
            self.draw_villager_home(villager)


class Feller(Profession):
    '''The Feller provides Wood for the village'''

    def __init__(self):
        
        # Inherit data
        Profession.__init__(self)

        # Villager info
        self.name = 'Feller'
        self.description = 'Provides 2-3 wood each turn'
        self.colour = 'dark goldenrod3'

    def action(self, villager):
        '''Collect Wood'''

        # If villager is in a house find a location and end action
        if villager.in_house:
            self.villager_location_set(villager)
            return None

        # If no tree has been found find one.
        if 'Tree' in config.map.terrain_map and villager.turn_action == None:
            self.villager_location_set(villager, False)

        # If a tree is ready to be felled then fell it
        if villager.turn_action != None:

            # Get wood 
            wood_produced = random.randint(1,3)
            wood_produced = self.get_harvest_modifier(villager, wood_produced)

            # If no wood was produced return error
            if wood_produced == 0:
                response = config.get_response('feller_action_fail')
                response[0] = response[0].format(villager.name)
                return response

            config.wood += wood_produced

            # get tree position
            x, y = villager.turn_action

            # Reset tile of tree
            pos = x + ((y-1)*config.map.width)
            config.map.terrain_map[pos] = 'Grass'
            config.map.texture_map[pos] = config.map.get_ground_texture(x, y)
            mapUI.draw_map(config.map.frame)

            # Find the next tree
            self.villager_location_set(villager, False)

            # Return to logs
            response = config.get_response('feller_action')
            response[0] = response[0].format(villager.name, wood_produced)
            return response

        else:
            # Return failed response
            self.draw_villager_home(villager)
    
    def villager_location_set(self, villager, return_home=True):
        '''Places the feller by the tree'''
        
        if 'Tree' in config.map.terrain_map:
            
            # Find tree
            x, y = self.find_tree(villager)

            if not(x == False):

                # Place villager at tree
                dir = random.randint(1,4)
                if dir == 1:
                    x_delta, y_delta = 0, 1
                elif dir == 2:
                    x_delta, y_delta = 1, 0
                elif dir == 3:
                    x_delta, y_delta = 0, -1
                elif dir == 4:
                    x_delta, y_delta = -1, 0

                draw_villager(villager, x+x_delta, y+y_delta)
                villager.in_house = False

                config.feller_trees.append((x, y))
                villager.turn_action = (x, y)

                return True
            else:
                villager.turn_action = None

        if return_home:
            self.draw_villager_home(villager)

    def find_tree(self, villager):
        '''Find and place the feller by the tree'''

        # Get variables
        item = None
        center_x = villager.pos[0]
        center_y = villager.pos[1]
        delta_change = 3
        delta = delta_change

        # Find tree
        attempts = 0
        while not(item == 'Tree'):
            attempts += 1

            # Get variables
            x_dir =(random.randint(0,1)*2)-1
            x_range = range(center_x-(delta*x_dir), center_x+(delta*x_dir), x_dir)

            y_dir =(random.randint(0,1)*2)-1
            y_range = range(center_y-(delta*y_dir), center_y+(delta*y_dir), y_dir)

            # Run through tiles in range
            for x in x_range:
                for y in y_range:

                    if abs(y) < delta-delta_change:
                        y += delta_change*y_dir*2

                    # Rounded variables
                    xx = max(min(x, config.map.width-2), 1)
                    yy = max(min(y, config.map.height-2), 1)

                    if not((xx, yy) in config.feller_trees):

                        pos = xx + ((yy-1)*config.map.width)

                        item = config.map.terrain_map[pos]
                        if item == 'Tree':
                            return xx, yy 

                if abs(x) < delta-delta_change:
                    x += delta_change*x_dir*2

            if attempts > 30 :
                return False, False
 
            delta += delta_change

class Carpenter(Profession):
    '''The carpenter builds building with wood'''

    def __init__(self):
        
        # Inherit data
        Profession.__init__(self)

        # Villager info
        self.name = 'Carpenter'
        self.description = 'Constructs wooden buildings'
        self.colour = 'gold'

        self.action_text = 'Construct'

        # List of available buildings
        self.buildings = ('Wooden Hut',
                          'Wooden Statue')

    def action(self, villager):
        '''Build a building if the action was selected'''

        # Place villager in house
        self.draw_villager_home(villager)

        # Only attempt to build if action was seleceted
        if villager.turn_action != None:

            # if building cannot be build return error
            build = villager.turn_action[0](
                                            villager.turn_action[1],
                                            villager.turn_action[2][0],
                                            villager.turn_action[2][1]
                                            )

            if build:
                
                # Run on creation functions for building
                villager.turn_action[1].on_creation()

                response = config.get_response('build_action_succeed')
                response[0] = response[0].format(villager.name, villager.turn_action[1].name)
                return response

            else:
                response = config.get_response('carpenter_action_no_wood')
                response[0] = response[0].format(villager.name, villager.turn_action[1].name)
                return response

class Plantsman(Profession):
    '''The plantsman plants trees for the people of the village'''
    
    def __init__(self):
        
        # Inherit data
        Profession.__init__(self)

        # Villager info
        self.name = 'Plantsman'
        self.description = 'Plants trees'
        self.colour = 'dark green'

    def action(self, villager):
        '''Plants a tree is one is set to be plant'''

        # If villager is in a house find a location and end action
        if villager.in_house:
            self.villager_location_set(villager)
            return None

        # If no planting space is found find one
        if villager.turn_action == None:
            self.villager_location_set(villager)

        # Plant tree is space is given
        if villager.turn_action != None:
            
            # Get variables
            x = villager.turn_action[0]
            y = villager.turn_action[1]
            pos = x + (y*config.map.width)

            tree = config.get_building('Tree')
            tree.pos_x = x
            tree.pos_y = y

            texture = tree.get_texture(4)

            # Update map
            config.map.terrain_map[pos] = 'Tree'
            config.map.texture_map[pos] = texture

            mapUI.draw_map(config.map.frame)

            # Find a new location for planting
            self.villager_location_set(villager)

            # Return results
            response = config.get_response('plantsmen_plant_tree')
            response[0] = response[0].format(villager.name)
            return response   

    def villager_location_set(self, villager, return_home=True):
        '''Find a suitable location for a tree for the village to move to'''

        # Get initial variables
        a = 2  # Checks per ring
        b = 4  # Size of ring
        # Note that a is the number of times each distance is checked before
        #  moving onto the next distance. Couldn't think of better name

        # Find a location for the tree
        size = max(config.map.width, config.map.height)*a
        for spread in range(b*2, round(size/b), b):

            # Get the delta for the tree
            ring = math.floor(spread/a)

            delta_x = random.randint(0, ring) 
            delta_y = random.randint(0, ring)

            delta_x *= (random.randint(0, 1)*2)-1
            delta_y *= (random.randint(0, 1)*2)-1

            # Get the position
            x = villager.pos[0] + delta_x
            y = villager.pos[1] + delta_y

            # Keep data in bounds
            x = max(min(x, config.map.width-2), 1)
            y = max(min(y, config.map.height-2), 1)

            # Check if space is empty
            try: 
                space_free = config.map.check_free_land(config.get_building('Tree'), x-1, y-1)
            except:
                space_free = False

            # Break loop if space found
            if space_free:
                break
        
        # Move villager to location when found
        if space_free:

            # Place villager at tree
            dir = random.randint(1,4)
            if dir == 1:
                x_delta, y_delta = 0, 1
            elif dir == 2:
                x_delta, y_delta = 1, 0
            elif dir == 3:
                x_delta, y_delta = 0, -1
            elif dir == 4:
                x_delta, y_delta = -1, 0

            # Adjust villager
            draw_villager(villager, x+x_delta, y+y_delta)
            villager.in_house = False
            villager.turn_action = (x, y)

        else:
            # if no tree was found return error
            pass

            self.draw_villager_home(villager)

class Miner(Profession):
    '''Miner builds mines and gathers stone'''

    def __init__(self):
        
        # Inherit data
        Profession.__init__(self)

        # Villager info
        self.name = 'Miner'
        self.description = 'Gathers stone'
        self.colour = 'gray40'
        self.building = 'Mine'

        # Mine construction info
        self.action_text = 'Construct mine'
        self.buildings = ['Mine']

    def action(self, villager):

        # Place villager
        self.villager_location_set(villager)

        # Only attempt to build if action was seleceted
        if villager.turn_action != None:

            # if building cannot be build return error
            build = villager.turn_action[0](
                                            villager.turn_action[1],
                                            villager.turn_action[2][0],
                                            villager.turn_action[2][1]
                                            )

            if build:
                
                # Run on creation functions for building
                villager.turn_action[1].on_creation()

                response = config.get_response('build_action_succeed')
                response[0] = response[0].format(villager.name, villager.turn_action[1].name)
                return response

            else:
                response = config.get_response('carpenter_action_no_wood')
                response[0] = response[0].format(villager.name, villager.turn_action[1].name)
                return response
        
        else:
            # If there is a mine to work at collect stone
            if villager.work_building != None:
                
                # Collect sotne
                stone_produced = random.randint(1,3)
                config.stone += stone_produced

                # Return to logs
                response = config.get_response('miner_action')
                response[0] = response[0].format(villager.name, stone_produced)
                return response

            else:
                self.draw_villager_home(villager)

    
    def villager_location_set(self, villager, return_home=True):
        '''Places the villager in the mines'''

        building = villager.work_building

        if building != None:
            if building.name == self.building:

                # Get variables
                delta = random.randint(0,1)

                pos_x = building.pos_x + delta + 2
                pos_y = building.pos_y + 1

                # Adjust villager visual settings
                draw_villager(villager, pos_x, pos_y)
                villager.in_house = False

        else:
            self.draw_villager_home(villager)
