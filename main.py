#
# Villager Game
# Main Module
# Written by Madeline Autumn
# Last modified on 05/06/21
#

### Importants and Varibles ###
import config
import gameApp
import villagers

# Initialize the globals
config.init()

# Create the innitial villagers
for i in range(3):
    villagers.create_villager()

### Main Game Loop ###

if __name__ == '__main__':
    main_app = gameApp.GameApp()
    main_app.root.mainloop()

    config.save()
