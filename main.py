#
# Villager Game
# Main Module
# Written by Madeline Autumn
# Last modified on 03/06/21
#

### Importants and Varibles ###
import config
import game_app
import villagers, professions

# Initialize the globals
config.init()

### Main Game Loop ###

if __name__ == '__main__':
    main_app = game_app.GameApp()
    main_app.root.mainloop()
