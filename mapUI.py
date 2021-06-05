#
# Villager Game
# MapUI Module
# Written by Madeline Autumn
# Last modified on 05/06/21
#

### Importants and Varibles ###
import tkinter as tk
import config, map
import random

### Classes ###
class MapFrame:
    '''Class to deal with the onscreen map of the village'''

    def __init__(self, parent, frame):

        self.parent = parent
        self.frame = frame

        self.map = map.Map(self)
        self.map.build_building('Wooden Hut')

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
        self.map_box = tk.Text(self.frame, 
                                width=config.map_x2, 
                                height=config.map_y2,
                                state=tk.DISABLED,
                                bg='black')
        self.map_box.grid(row=0, column=0, padx=4, pady=4)

        # Place the scrollbars in
        self.map_box.config(yscrollcommand=self.map_scrollbar_vertical.set)
        self.map_scrollbar_vertical.config(command=self.map_box.yview)

        self.map_box.config(xscrollcommand=self.map_scrollbar_horizontal.set)
        self.map_scrollbar_horizontal.config(command=self.map_box.xview)

    def draw_map(self):
        '''Draws the map to the screen'''

        # Enable the map for editing
        self.map_box.config(state=tk.NORMAL)
        self.map_box.delete('1.0', tk.END)

        # Run through every position in the map and add a tag to it
        for y in range(1, config.map_y2-config.map_y1+1):
            for x in range(config.map_x2-config.map_x1):
                
                # Get the position and key
                pos = f'{y}.{x-1}'
                key = f'({y}:{x})'

                # Draw a building if it exists. Place grass if else
                try:
                    item = config.map[key]
                    # Add text to the map
                    self.map_box.insert(pos, item.get_texture())
                except:
                    item = config.get_building('Grass')
                    # Add text to the map
                    self.map_box.insert(pos, item.get_texture(y + x*123456))

                # Add tag to colour text
                self.map_box.tag_add(key, pos, pos+'+1c')
                self.map_box.tag_config(key, foreground=item.colour)
            
            self.map_box.insert(tk.END, '\n')

        # Deletes Trailing newline
        self.map_box.delete(f'{config.map_y2+1}.0', tk.END)

        # Turn the map back off for editing 
        self.map_box.config(state=tk.DISABLED)
