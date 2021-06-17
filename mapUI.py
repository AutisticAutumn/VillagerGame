#
# Villager Game
# MapUI Module
# Written by Madeline Autumn
#

### Importants and Varibles ###
import tkinter as tk
from tkinter.constants import NORMAL
import config

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

def draw_map(self, updated_positions=[]):
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
            
            if not(pos_change) or pos_key in updated_positions:
                # Remove old texture
                self.map_box.delete(pos_key, pos_key+'+1c')

                # insert the new texture into the box
                self.map_box.insert(pos_key, texture[0])

                self.map_box.tag_add(pos_key, pos_key, pos_key+'+1c')
                self.map_box.tag_config(pos_key, foreground=texture[1])

    # Turn the map back off 
    self.map_box.config(state=tk.DISABLED)

    # Clear positions that need to be updated 
    if len(updated_positions) > 0:
        self.updated_positions = []

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
        self.building = config.get_building('Wooden Hut')

    def create_toplevel(self):
        '''Create the toplevel widget for the map popout'''

        # Initialize the root
        self.root = tk.Toplevel(self.parent.parent.root)
        self.root.title('World map')
        self.root.resizable(width=0, height=0)
        self.root.focus()

        # Add the map textbox
        self.map_box = tk.Text(self.root, 
                               width=config.map.width, 
                               height=config.map.height,
                               bg='black',
                               wrap=tk.NONE)
        self.map_box.grid(row=0, column= 0, rowspan=2, padx=8, pady=8)

        # Add the tile information boxes
        self.tile_texture_box = tk.Text(self.root, 
                                        width=1, 
                                        height=1,
                                        bg='black',)
        self.tile_texture_box.grid(row=0, column= 1,padx=4, pady=8, sticky='N')

        self.tile_name_box = tk.Text(self.root, 
                                     width=16, 
                                     height=1,
                                     bg='black',)
        self.tile_name_box.grid(row=0, column= 2,padx=4, pady=8, sticky='N')

        self.tile_info_box = tk.Text(self.root, 
                                     width=20, 
                                     height=12,
                                     bg='black',)
        self.tile_info_box.grid(row=1, column= 1, columnspan=2, padx=4, pady=8)

        # Draw the map textures in 
        create_map_base(self)
        draw_map(self)
        self.updated_positions = []

        # Setup the selector
        self.draw_selector()
        self.root.bind('<Right>', self.move_selector_right)
        self.root.bind('<Left>', self.move_selector_left)
        self.root.bind('<Up>', self.move_selector_up)
        self.root.bind('<Down>', self.move_selector_down)
    
    def update_tile_information(self):
        '''Updates stats for the selected tile'''

        # Get position and position keys
        x = self.map.selector_x
        y = self.map.selector_y

        pos = x + ((y-1)*self.map.width)
        pos_key = f'({y}:{x})'

        # Get texture
        texture = self.map.texture_map[pos]

        # Attempt to find building at location, else return grass
        
        try:
            building = self.map.map[pos_key]
        except:
            building = config.get_building('Grass')

        # Clear all textboxes of previous data
        self.tile_texture_box.delete(1.0, tk.END)
        self.tile_name_box.delete(1.0, tk.END)
        self.tile_info_box.delete(1.0, tk.END)

        # Insert new data to the text boxes
        self.tile_texture_box.insert(1.0, texture[0])
        self.tile_name_box.insert(1.0, building.name)
        self.tile_info_box.insert(1.0, building.description)

        # Add colour tags to the boxes
        self.tile_texture_box.tag_add('Colour', 1.0, tk.END)
        self.tile_name_box.tag_add('Colour', 1.0, tk.END)
        self.tile_info_box.tag_add('Colour', 1.0, tk.END)

        self.tile_texture_box.tag_config('Colour', foreground=texture[1])
        self.tile_name_box.tag_config('Colour', foreground=texture[1])
        self.tile_info_box.tag_config('Colour', foreground='white')

    def draw_selector(self):
        '''Draws the selector onscreen that gives information about a tile'''

        # Clear off old selectors
        draw_map(self, self.updated_positions)

        # Enable the map for editing
        self.map_box.config(state=tk.NORMAL)

        # Get the raw positions as x and y
        x = self.map.selector_x
        y = self.map.selector_y

        # Get the texture to draw
        if self.building == None:
            texture = ('X', 'white')
            size = (1, 1)
        else:
            size = self.building.size

        for yy in range(size[1]):
            for xx in range(size[0]):
                
                # Get the position key
                pos_key = f'{y+yy}.{x+xx-1}'

                # Remove old texture
                self.map_box.delete(pos_key, pos_key+'+1c')

                # Get exact texture for building
                if not(self.building == None):
                   
                    # Get colour for building
                    if self.map.check_free_land(self.building, x, y):
                        texture = (self.building.get_texture(xx+(yy*size[0]))[0], 'lime')
                    else:
                        texture = (self.building.get_texture(xx+(yy*size[0]))[0], 'red')

                # insert the new texture into the box
                self.map_box.insert(pos_key, texture[0])

                self.map_box.tag_add(pos_key, pos_key, pos_key+'+1c')
                self.map_box.tag_config(pos_key, foreground=texture[1])

                # Save the positions that have been updated
                self.updated_positions.append(pos_key)

        # Turn the map back off 
        self.map_box.config(state=tk.DISABLED)

        # Update tile info
        self.update_tile_information()

    ### Moving selector ###
    def move_selector(self, dir):
        '''Move the sector and run any extra functions'''

        # Get the size of the seletion
        if self.building != None:
            size = self.building.size
        else:
            size = (0,0)

        # Move is the correct direction and change varibles
        if dir == 'Right':
            self.map.selector_x += 1
        elif dir == 'Left':
            self.map.selector_x -= 1
        elif dir == 'Up':
            self.map.selector_y -= 1
        elif dir == 'Down':
            self.map.selector_y += 1

        # Keep stats within range
        max_x = self.map.width - size[0] + 1
        max_y = self.map.height - size[1] + 1
        self.map.selector_x = max(0, min(self.map.selector_x, max_x))
        self.map.selector_y = max(1, min(self.map.selector_y, max_y))

        # Update the selector
        self.draw_selector()

    def move_selector_right(self, _event=None):
        '''Move the position of the selector right based on keyboard input'''
    
        self.move_selector('Right')

    def move_selector_left(self, _event=None):
        '''Move the position of the selector left based on keyboard input'''

        self.move_selector('Left')

    def move_selector_up(self, _event=None):
        '''Move the position of the selector up based on keyboard input'''

        self.move_selector('Up')

    def move_selector_down(self, _event=None):
        '''Move the position of the selector down based on keyboard input'''

        self.move_selector('Down')
