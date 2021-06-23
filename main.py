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

# Create the innitial villagers
for i in range(init_villagers):
    config.create_villager()

### Main Game Loop ###

if __name__ == '__main__':

    config.init_app()
    
    # Create the innitial houses
    for i in range(init_villagers):
        config.map.build_building(config.get_building('Wooden Hut'), 16+(i*5), 16, False)
    
    # Update the map
    mapUI.draw_map(config.map.frame)

    config.main_app.root.mainloop()

    config.save()
