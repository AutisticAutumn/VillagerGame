#
# Villager Game
# Main Module
# Written by Madeline Autumn
# Last modified on 31/05/21
#

### Importants and Varibles ###
import tkinter as tk
import villagers

### Game Application Class ###

class GameApp:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title('Villager game')
        self.root.resizable(width=0, height=0)

        self.root.mainloop()

### Main Game Loop ###

if __name__ == '__main__':
    main_app = GameApp()