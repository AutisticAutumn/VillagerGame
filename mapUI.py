#
# Villager Game
# VillageUI Module
# Written by Madeline Autumn
# Last modified on 05/06/21
#

### Importants and Varibles ###
import tkinter as tk
import config

### Classes ##
class map:
    '''Class to deal with the onscreen map of the village'''

    def __init__(self, parent, frame):

        self.parent = parent
        self.frame = frame

        self.create_map()

    def create_map(self):
        '''Creates the onscreen mapbox'''

        self.map_scrollbar = tk.Scrollbar(self.frame)
        self.map_scrollbar.grid(row=0, column=1, sticky=tk.NSEW)

        self.map_text = tk.Text(self.frame, 
                                width=48, 
                                height=21,
                                state=tk.DISABLED,
                                bg='black')
        self.map_text.grid(row=0, column=0, padx=4, pady=4)

        self.map_text.config(yscrollcommand=self.map_scrollbar.set)
        self.map_scrollbar.config(command=self.map_text.yview)