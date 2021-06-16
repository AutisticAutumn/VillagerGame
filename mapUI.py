#
# Villager Game
# MapUI Module
# Written by Madeline Autumn
#

### Importants and Varibles ###
import tkinter as tk
from tkinter.constants import NORMAL
import config, map
import random

### Functions ###
def create_map_base(self):
        '''Create the plain base of grass for the map'''

        # Enable the map for editing
        self.map_box.config(state=tk.NORMAL)
        self.map_box.delete('1.0', tk.END)

        for y in range(1, self.map.height+1):
            for x in range(self.map.width):
                
                # Get the position and key
                pos = f'{y}.{x-1}'

                # Add grass base
                item = config.get_building('Grass').get_texture(y + x*123456)
                self.map_box.insert(pos, item[0])
                self.map.texture_map.append(item)

            self.map_box.insert(tk.END, '\n')

        # Add grass colour
        self.map_box.tag_add('Grass', 1.0, tk.END)
        self.map_box.tag_config('Grass', foreground='green')

        # Delete Trailing newline
        self.map_box.delete(f'{config.map.height+1}.0', tk.END)

        # Turn the map back off 
        self.map_box.config(state=tk.DISABLED)

def draw_map(self):
    '''Draws the map from the texture map'''

    # Enable map for editting
    self.map_box.config(state=tk.NORMAL)
        
    for y in range(1, self.map.height+1):
        for x in range(1,self.map.width):

            # Get position of the texture
            pos = x + ((y-1)*self.map.width)
            pos_key = f'{y}.{x-1}'
            texture = self.map.texture_map[pos]

            # Check is position has changes
            pos_change = self.map_box.get(pos_key, pos_key+'+1c') == texture[0]
            
            if not(pos_change):
                # Remove old texture
                self.map_box.delete(pos_key, pos_key+'+1c')

                # insert the new texture into the box
                self.map_box.insert(pos_key, texture[0])

                self.map_box.tag_add(pos_key, pos_key, pos_key+'+1c')
                self.map_box.tag_config(pos_key, foreground=texture[1])

    # Turn the map back off 
    self.map_box.config(state=tk.DISABLED)

### Classes ###
class MapFrame:
    '''Class to deal with the onscreen map of the village'''

    def __init__(self, parent, frame):

        self.parent = parent
        self.frame = frame

        self.map = config.map
        self.map.frame = self
        self.map.popout = MapPopout(self)

        self.map_size = (48, 21)

        self.create_map()
        create_map_base(self)

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
                               bg='black',
                               wrap=tk.NONE)
        self.map_box.grid(row=0, column=0, padx=4, pady=4)

        # Place the scrollbars in
        self.map_box.config(yscrollcommand=self.map_scrollbar_vertical.set)
        self.map_scrollbar_vertical.config(command=self.map_box.yview)

        self.map_box.config(xscrollcommand=self.map_scrollbar_horizontal.set)
        self.map_scrollbar_horizontal.config(command=self.map_box.xview)

    def insert_building(self, pos_key):
        '''Insert a building onto the map.
            pos_key should be top right corner of the building'''

        # Maker sure building exists at the position
        try:
            # Get the building object from the map
            building = self.map.map[pos_key]

            # Get variables for the for loop
            x0 = building.pos_x
            x1 = building.pos_x+building.size[0]

            y0 = building.pos_y
            y1 = building.pos_y+building.size[1]

            # Run through the complete building
            for y in range(y0, y1):
                for x in range(x0, x1):
                    
                    # Get position and texture
                    pos = (x-x0)+((y-y0)*building.size[0])
                    texture = building.get_texture(pos)
                
                    # Update the texture map
                    pos = x + ((y-1)*self.map.width)
                    self.map.texture_map[pos] = texture
            
        except:
            return False

class MapPopout:
    '''Creates a toplevel tkinter element that displays the full map'''

    def __init__(self, parent):

        self.parent = parent
        self.map = config.map

    def create_toplevel(self):
        '''Create the toplevel widget for the map popout'''

        # Initialize the root
        self.root = tk.Toplevel(self.parent.parent.root)
        self.root.title('World map')
        self.root.resizable(width=0, height=0)

        # Add the map textbox
        self.map_box = self.map_box = tk.Text(self.root, 
                                              width=config.map.width, 
                                              height=config.map.height,
                                              bg='black',
                                              wrap=tk.NONE)
        self.map_box.grid(padx=8, pady=8)

        # Draw the map textures in 
        create_map_base(self)
        draw_map(self)
        self.draw_selector()
    
    def draw_selector(self):
        '''Draws the selector onscreen that gives information about a tile'''

        # Enable the map for editing
        self.map_box.config(state=tk.NORMAL)

        # Get the raw positions as x and y
        x = self.map.selector_x
        y = self.map.selector_y

        # Get the position key
        pos_key = f'{y}.{x-1}'

        # Remove old texture
        self.map_box.delete(pos_key, pos_key+'+1c')

        # insert the new texture into the box
        self.map_box.insert(pos_key, 'X')

        self.map_box.tag_add(pos_key, pos_key, pos_key+'+1c')
        self.map_box.tag_config(pos_key, foreground='white')

        # Turn the map back off 
        self.map_box.config(state=tk.DISABLED)
