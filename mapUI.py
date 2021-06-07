#
# Villager Game
# MapUI Module
# Written by Madeline Autumn
# Last modified on 07/06/21
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

        self.map_size = (48, 21)

        self.create_map()
        self.draw_map()

        self.map.build_building('Wooden Hut', False)

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
                                width=self.map_size[0], 
                                height=self.map_size[1],
                                state=tk.DISABLED,
                                bg='black')
        self.map_box.grid(row=0, column=0, padx=4, pady=4)

        # Place the scrollbars in
        self.map_box.config(yscrollcommand=self.map_scrollbar_vertical.set)
        self.map_scrollbar_vertical.config(command=self.map_box.yview)

        self.map_box.config(xscrollcommand=self.map_scrollbar_horizontal.set)
        self.map_scrollbar_horizontal.config(command=self.map_box.xview)

    def draw_map(self):
        '''Draws the base map to the screen. No buildings are drawn'''

        # Enable the map for editing
        self.map_box.config(state=tk.NORMAL)
        self.map_box.delete('1.0', tk.END)

        # Run through every position in the map and add a tag to it
        for y in range(1, config.map_y2-config.map_y1+1):
            for x in range(config.map_x2-config.map_x1):
                
                # Get the position and key
                pos = f'{y}.{x-1}'
                key = f'({y}:{x})'

                # Get and add grass texture to map
                item = config.get_building('Grass').get_texture(y + x*123456)
                self.map_box.insert(pos, item[0])

                # Add tag to colour text
                self.map_box.tag_add(key, pos, pos+'+1c')
                self.map_box.tag_config(key, foreground=item[1])
            
            self.map_box.insert(tk.END, '\n')

        # Deletes Trailing newline
        self.map_box.delete(f'{config.map_y2+1}.0', tk.END)

        # Turn the map back off 
        self.map_box.config(state=tk.DISABLED)

    def insert_building(self, pos_key):
        '''Insert a building onto the map.
            pos_key should be top right corner of the building'''

        # Maker sure building exists at the position
        try:
            # Get the building object from the map
            building = config.map[pos_key]

            # Enable the map for editing
            self.map_box.config(state=tk.NORMAL)

            # Get variables for the for loop
            x0 = building.pos_x
            x1 = building.pos_x+building.size[0]

            y0 = building.pos_y
            y1 = building.pos_y+building.size[1]

            # Run through the complete building
            for y in range(y0, y1):
                for x in range(x0, x1):
                    
                    # Get the position for the building in textbox form
                    pos_key = f'{y}.{x-1}'

                    # Delete the current text at that position
                    self.map_box.delete(pos_key, pos_key+'+1c')

                    # Insert new text into the widget and add the tag
                    pos = (x-x0)+((y-y0)*building.size[0])
                    texture = building.get_texture(pos)
                    self.map_box.insert(pos_key, texture[0])

                    self.map_box.tag_add(pos_key, pos_key, pos_key+'+1c')
                    self.map_box.tag_config(pos_key, foreground=texture[1])
            
            # Turn the map back off 
            self.map_box.config(state=tk.DISABLED)
        except:
            return False
