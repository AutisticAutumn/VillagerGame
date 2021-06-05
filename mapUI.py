#
# Villager Game
# VillageUI Module
# Written by Madeline Autumn
# Last modified on 05/06/21
#

### Importants and Varibles ###
from random import random
import tkinter as tk
import config
import random

### Classes ##
class map:
    '''Class to deal with the onscreen map of the village'''

    def __init__(self, parent, frame):

        self.parent = parent
        self.frame = frame

        self.create_map()
        self.draw_map()

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
                                width=config.map_x2, 
                                height=config.map_y2,
                                state=tk.DISABLED,
                                bg='black')
        self.map.grid(row=0, column=0, padx=4, pady=4)

        # Place the scrollbars in
        self.map.config(yscrollcommand=self.map_scrollbar_vertical.set)
        self.map_scrollbar_vertical.config(command=self.map.yview)

        self.map.config(xscrollcommand=self.map_scrollbar_horizontal.set)
        self.map_scrollbar_horizontal.config(command=self.map.xview)

    def draw_map(self):
        '''Draws the map to the screen'''

        # Enable the map for editing
        self.map.config(state=tk.NORMAL)

        # Run through every position in the map and add a tag to it
        for y in range(1, config.map_y2-config.map_y1+1):
            for x in range(1, config.map_x2-config.map_x1+1):
                
                # Get the position and key
                pos = f'{y}.{x-1}'
                key = f'({y}:{x})'

                item = random.choice([' ',' ','.',',','`'])

                # Add text to the map
                self.map.insert(pos, item)

                # Add tag to colour text
                self.map.tag_add(key, pos, pos+'+1c')
                self.map.tag_config(key, foreground='dark green')

            self.map.insert(tk.END, '\n')

        # Deletes Trailing newline
        self.map.delete(f'{config.map_y2+1}.0', tk.END)

        # Turn the map back off for editing 
        self.map.config(state=tk.DISABLED)
