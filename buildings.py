#
# Villager Game
# Main Module
# Written by Madeline Autumn
#

### Importants and Varibles ###
import config
import gameApp, mapUI

init_villagers = 3

# Initialize the globals
config.init()

### Main Game Loop ###

if __name__ == '__main__':

    config.init_app()
    
    # Create the innitial houses and villagers
    for i in range(init_villagers):

        # Add wooden huts and adjust max villagers accordingly
        config.map.build_building(config.get_building('Wooden Hut'), 16+(i*5), 16, False)
        config.max_villagers += 1

        config.map.build_building(config.get_building('Farm'), 16+(i*5), 20, False)
        
        # Create inital villagers
        config.create_villager()
    
    # Update the map
    mapUI.draw_map(config.map.frame)

    config.main_app.root.mainloop()

    config.save()
