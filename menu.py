#
# Villager Game
# Menu Module
# Written by Madeline Autumn
#

### Importants and Varibles ###
import tkinter as tk
import config

### Classes ###

class MenuApp():
    '''The popout for the menu'''

    def __init__(self):
        
        # Initialize the window
        self.root = tk.Tk()
        self.root.title('Villager game')
        self.root.resizable(width=0, height=0)
