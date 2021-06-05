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

        # Create the scrollbars
        self.map_scrollbar_vertical = tk.Scrollbar(self.frame)
        self.map_scrollbar_vertical.grid(row=0, column=1, sticky=tk.NSEW)

        self.map_scrollbar_horizontal = tk.Scrollbar(self.frame, 
                                                     orient=tk.HORIZONTAL)
        self.map_scrollbar_horizontal.grid(row=1, column=0, sticky=tk.NSEW)

        # Create the textbox itself
        self.map = tk.Text(self.frame, 
                                width=48, 
                                height=21,
                                state=tk.DISABLED,
                                bg='black')
        self.map.grid(row=0, column=0, padx=4, pady=4)

        # Place the scrollbars in
        self.map.config(yscrollcommand=self.map_scrollbar_vertical.set)
        self.map_scrollbar_vertical.config(command=self.map.yview)

        self.map.config(xscrollcommand=self.map_scrollbar_horizontal.set)
        self.map_scrollbar_horizontal.config(command=self.map.xview)
