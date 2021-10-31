#
# Villager Game
# Main Module
# Written by Madeline Autumn
#

### Importants and Varibles ###
import config
import mapUI, menu
import random

# Initialize the globals
config.init()

init_villagers = 3
offset_max = (7, 5)

### Functions ###
def get_starting_pos():
    '''Gets the starting position for the village'''

    global init_pos

    # Find a position that is on grass terrian
    init_pos = None
    while init_pos == None:
        
        x = random.randint(10, config.map.width-10)
        y = random.randint(10, config.map.height-10)

        pos = ((y-1)*config.map.width)
        
        if config.map.terrain_map[pos] == 'Grass':
            init_pos = (x, y)

def get_offset(x_offset, y_offset):
    '''Return a randomized offset and position for initital buildings'''

    # Get offset in relation to center pos and set pos
    offset = (random.randint(x_offset*-1, x_offset), 
              random.randint(y_offset*-1, y_offset))
    pos = (init_pos[0] + offset[0], init_pos[1] + offset[1])

    return pos

def build_building(pos, building):
    '''Attemps to place a building on the map'''

    # Attempt to place building
    global attempts
    if attempts < 201:
        get_building = config.map.build_building(config.get_building(building),
                                                pos[0], pos[1],
                                                False, True)

        return get_building

    return True

def create_village():
    '''Creates the innitial houses and villagers'''

    global attempts
    attempts = 0

    # Add wooden huts and adjust max villagers accordingly
    print('Adding Houses')
    config.max_villagers = 0
    for i in range(init_villagers):

        build_hut = False
        while build_hut == False:
            pos = get_offset(offset_max[0], offset_max[1])
            build_hut = build_building(pos, 'Wooden Hut')
            attempts +=1
        config.max_villagers += 1

        config.seed += 1

    # Add Buildings
    print('Adding Buildings')
    #  Farms
    for i in range(round(init_villagers*(2/3))):  

        build_farm = False
        while build_farm == False: 
            pos = get_offset(offset_max[0]+1, offset_max[1]+1)
            build_farm = build_building(pos, 'Farm')
            attempts +=1

        config.seed += 1
    #  Storehouse
    build_storehouse = False
    while build_storehouse == False: 
        pos = get_offset(offset_max[0]+2, offset_max[1]+2)
        build_storehouse = build_building(pos, 'Storehouse')
        attempts +=1

    config.seed += 1

    # Add Trees
    print('Adding Trees')
    for i in range(init_trees):
        config.map.plant_tree()
    
    # Create inital villagers
    print('Adding Villagers')
    for i in range(init_villagers): 
        
        config.create_villager(move=False)
        config.villagers[-1].profession.action(config.villagers[-1])

def create_map(reset=False):
    '''Runs a series of functions that generate the map'''

    # Delete the old gameapp if a new one is created
    if reset:
        config.main_app.root.destroy()

        # Reset map
        config.villagers = []

    # Initiate the applications and variables
    initiate_apps()

    global total_ponds, init_trees
    total_ponds = random.randint(config.map.pond_min, config.map.pond_max)
    init_trees = random.randint(config.map.tree_min, config.map.tree_max)

    # Add ponds to the map
    print('Adding ponds')
    config.map.create_ponds(total_ponds)

    # Get villager position
    print('Finding Village')
    get_starting_pos()
    config.map.selector_x = init_pos[0]
    config.map.selector_y = init_pos[1]

    # Add buildings
    create_village()

    # If an error occured earlier reset
    global attempts
    if attempts > 200:
        print('Resetting\n')
        create_map(True)

def initiate_apps():
    '''Initiates the apps'''

    print('Initializing Map')
    config.get_seed()

    config.map.reset_map()
    config.init_app()

### Main Game Loop ###

if __name__ == '__main__':

    # initialize the main menu
    menu_app = menu.MenuApp()
    menu_app.root.mainloop()

    # If menu was closed with no action end program
    if menu_app.quit == True:
        exit()

    # Create the world map if requested
    if menu_app.generate_world == True:
        create_map()
    else:
        initiate_apps()

    # Draw the map
    mapUI.draw_map(config.map.frame)

    # Set the scrollbar to center on the map
    map_frame = config.main_app.map

    x = init_pos[0] / ( config.map.width + ( map_frame.map_size[0]*1.5 ) )
    y = init_pos[1] / ( config.map.height + ( map_frame.map_size[1]*1.5 ) )

    map_frame.map_box.xview_moveto(x)
    map_frame.map_box.yview_moveto(y)

    config.manual.open_manual()

    # Run the main loop
    config.main_app.root.mainloop()

    # Save upon game closing
    config.save()
