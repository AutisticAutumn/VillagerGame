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
                self.map.terrain_map.append('Grass')

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

    # Get list of villager positions
    villager_positions = {}
    for villager in config.villagers:
        villager_positions.update({villager.pos: villager})
        
    for y in range(1, self.map.height+1):
        for x in range(1,self.map.width):

            # Get position of the texture
            pos = x + ((y-1)*self.map.width)
            pos_key = f'{y}.{x-1}'
            texture = self.map.texture_map[pos]

            # Check is position has changes
            pos_change = self.map_box.get(pos_key, pos_key+'+1c') == texture[0]

            # If tile is a villager tile then draw that instead
            villager_tile = (x, y) in villager_positions.keys()
            if villager_tile == True:
                
                updated_positions.append(pos_key)

                villager = villager_positions[(x, y)]
                texture = (villager.texture, villager.colour)
            
            if not(pos_change) or pos_key in updated_positions:
                # Remove old texture
                self.map_box.delete(pos_key, pos_key+'+1c')

                # insert the new texture into the box
                self.map_box.insert(pos_key, texture[0])

                self.map_box.tag_add(pos_key, pos_key, pos_key+'+1c')
                self.map_box.tag_config(pos_key, foreground=texture[1])

    # Turn the map back off 
    self.map_box.config(state=tk.DISABLED)

    # Update villager maps
    try:
        for villager in config.villagers:
            villager.frame.update_map()
    except:
        pass

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

        self.font_size = 14
        self.map_size = (round(48*(10/self.font_size)), 
                        round(21*(10/self.font_size)))

        self.create_map()
        create_map_base(self)

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
                               wrap=tk.NONE,
                               font=('Courier', self.font_size))
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

            # Update the map texture
            building.update_texture_map()
            
        except:
            return False

class MapPopout:
    '''Creates a toplevel tkinter element that displays the full map'''

    def __init__(self, parent):

        self.parent = parent
        self.map = config.map

        # Functions for building
        self.building = None
        self.build_positions = (None, None)
        self.villager = None

        # Variables
        self.width = min(config.map.width, config.map.default_width)
        self.height = min(config.map.height, config.map.default_height)

    def create_toplevel(self):
        '''Create the toplevel widget for the map popout'''

        # Initialize the root
        self.root = tk.Toplevel(self.parent.parent.root)
        self.root.title(f'{config.village_name}  |  Turn: {config.turn}  |  World map')
        self.root.resizable(width=0, height=0)
        self.root.focus()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Add the map textbox
        self.map_frame = tk.Frame(self.root)
        self.map_frame.grid(row=0, column= 0, rowspan=5, padx=8, pady=8)

        self.map_box = tk.Text(self.map_frame, 
                               width=self.width, 
                               height=self.height,
                               bg='black',
                               wrap=tk.NONE)
        self.map_box.grid(row=0, column=0)

        # Add scrollbars to the relevant axis if needed
        if config.map.width > config.map.default_width:
            self.map_scrollbar_horizontal = tk.Scrollbar(self.map_frame, 
                                                     orient=tk.HORIZONTAL)
            self.map_scrollbar_horizontal.grid(row=1, column=0, sticky=tk.NSEW)

            self.map_box.config(xscrollcommand=self.map_scrollbar_horizontal.set)
            self.map_scrollbar_horizontal.config(command=self.map_box.xview)
        
        if config.map.height > config.map.default_height:
            self.map_scrollbar_vertical = tk.Scrollbar(self.map_frame, 
                                                       orient=tk.VERTICAL)
            self.map_scrollbar_vertical.grid(row=0, column=1, sticky=tk.NSEW)

            self.map_box.config(yscrollcommand=self.map_scrollbar_vertical.set)
            self.map_scrollbar_vertical.config(command=self.map_box.yview)

        # Add the tile information boxes
        self.tile_texture_box = tk.Text(self.root, 
                                        width=1, 
                                        height=1,
                                        bg='black')
        self.tile_texture_box.grid(row=0, column= 1,padx=4, pady=8, sticky='N')

        self.tile_name_box = tk.Text(self.root, 
                                     width=16, 
                                     height=1,
                                     bg='black')
        self.tile_name_box.grid(row=0, column= 2,padx=4, pady=8, sticky='N')

        self.tile_info_box = tk.Text(self.root, 
                                     width=20, 
                                     height=16,
                                     bg='black',
                                     wrap=tk.WORD)
        self.tile_info_box.grid(row=1, column= 1, columnspan=2, padx=4, pady=4, sticky='N')

        # Add construct button is in building mode
        if self.building != None:
            
            # Building selection menu
            self.selected_building = tk.StringVar()
            self.selected_building.set(self.building.name)

            self.building_select = tk.OptionMenu(self.root,
                                                 self.selected_building,
                                                 *self.villager.profession.buildings,
                                                 command=self.select_building)
            self.building_select.grid(row=2, column= 1, columnspan=2, padx=4, pady=4, sticky='S')

            self.building_stats = tk.Text(self.root, 
                                          width=20, 
                                          height=16,
                                          bg='black',
                                          wrap=tk.WORD)
            self.building_stats.grid(row=3, column= 1, columnspan=2, padx=4, pady=4, sticky='N')

            self.update_building_text()

            # Building button
            self.construct_button = tk.Button(self.root,
                                              text='Construct building',
                                              width=20,
                                              height=2,
                                              command=self.construct_building)
            self.construct_button.grid(row=4, column= 1, columnspan=2, padx=4, pady=8, sticky='S')

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

        # Special case tiles
        villager_tile = False
        for villager in config.villagers:
            if x == villager.pos[0] and y == villager.pos[1]:
                
                villager_tile = True

                break

        width = 1  
        height = 1 
        complex_tile = False
        if self.building != None:
            width = self.building.size[0]
            height = self.building.size[1]
            self.tile_texture_box.config(width=width, 
                                         height=height)
            complex_tile = True    
            
        # Get texture
        texture = self.map.texture_map[pos]

        # Get description        
        description = []
        for yy in range(height):
            for xx in range(width):

                # Get position of the texture
                pos = (x+xx) + ((y+yy-1)*config.map.width)
                pos_key = f'({y+yy}:{x+xx})'

                # Attempt to find building at location, else return grass
                try:
                    building = self.map.map[pos_key]
                except:
                    building = config.get_building(self.map.terrain_map[pos])
                name = building.name
                    
                # Get advanced building descriptiong
                description.append(self.get_building_description(building))

        # Prune complex descriptions
        if complex_tile:
            temp_description = [] 
            for sub_desc in description:
                for text in sub_desc:
                    if not(text in temp_description):
                        temp_description.append(text)

            description = temp_description
        else:
            description = description[0]

        # Set Villager tile varibles
        if villager_tile:
            texture = (villager.texture, villager.colour)
            name = f'{villager.name}\n{name}'
            self.tile_name_box.config(height=2)
        else:
            self.tile_name_box.config(height=1)

        # Enable and clear all the boxes
        self.tile_texture_box.config(state=tk.NORMAL)
        self.tile_name_box.config(state=tk.NORMAL)
        self.tile_info_box.config(state=tk.NORMAL)

        self.tile_texture_box.delete(1.0, tk.END)
        self.tile_name_box.delete(1.0, tk.END)
        self.tile_info_box.delete(1.0, tk.END)

        ## Texture box
        if complex_tile:
            self.update_complex_tile_map(x, y, self.building.size[0], self.building.size[1])
        else:
            self.tile_texture_box.insert(1.0, texture[0])
            self.tile_texture_box.tag_add('Colour', 1.0, tk.END)
            self.tile_texture_box.tag_config('Colour', foreground=texture[1])

        ## Tile name box
        self.tile_name_box.insert(1.0, name)
        if villager_tile:
            self.tile_name_box.tag_add('Colour', 1.0, 2.0)
            self.tile_name_box.tag_add('BGColour', 2.0, tk.END)
            self.tile_name_box.tag_config('BGColour', foreground=building.text_colour)
        else:
            self.tile_name_box.tag_add('Colour', 1.0, tk.END)
        
        self.tile_name_box.tag_config('Colour', foreground=texture[1])
        
        ## Info box
        start_point = '0.0'
        tag_id = 0
        
        # Add each line of text and add colour seperatly
        for text in description:
            
            # Remove initial newline
            if tag_id == 0:
                info_box_text = text[0][2:]
            else:
                info_box_text = text[0]

            # Add text
            self.tile_info_box.insert(start_point, info_box_text)
            end_point = self.tile_info_box.index("end")

            self.tile_info_box.tag_add(tag_id, start_point, end_point)
            self.tile_info_box.tag_config(tag_id, foreground=text[1])

            # Update varibles
            tag_id += 1
            start_point = end_point

        # Disable all the boxes
        self.tile_texture_box.config(state=tk.DISABLED)
        self.tile_name_box.config(state=tk.DISABLED)
        self.tile_info_box.config(state=tk.DISABLED)

    def update_complex_tile_map(self, xx, yy, width, height):
        '''Updates the tile texture box box if it is complex'''

        # Get positions of villagers in list
        villager_positions = {}
        for villager in config.villagers:
            villager_positions.update({villager.pos: villager})
        
        # Run through and add tiles
        for y in range(height):
            for x in range(width):

                # Get position of the texture
                pos = (x+xx) + ((y+yy-1)*config.map.width)
                pos_key = f'{y+1}.{x}'

                # Get texture
                texture = config.map.texture_map[pos]
                    
                # If tile is a villager tile then draw that instead
                villager_tile = (x+xx, y+yy) in villager_positions.keys()
                if villager_tile == True:

                    villager = villager_positions[(x+xx, y+yy)]
                    texture = (villager.texture, villager.colour)
                
                # insert the new texture into the box
                self.tile_texture_box.insert(pos_key, texture[0])

                self.tile_texture_box.tag_add(pos_key, pos_key, pos_key+'+1c')
                self.tile_texture_box.tag_config(pos_key, foreground=texture[1])

            self.tile_texture_box.insert(tk.END, '\n')

    def get_building_description(self, building):
        '''Gets a complete description for a building'''
    
        description = [(f'\n\n{building.description}', building.text_colour)]
            
        if building.type != 'Terrain':

            description.insert(0, (f'\n\n{building.name}', building.text_colour))
                
            # Add descriptions for work buildings
            if building.type == 'Work':

                # Add crop numbers for farms
                if building.name == 'Farm':
                    if building.food > 0:
                        description.append((f'\n\nContains {building.food} crops', building.text_colour))
                    else:
                        description.append(('\n\nContains no crops', building.text_colour))

                # Add workers to description
                if building.worker != None:
                    description.append((f'\n\nCurrently worked by {building.worker.name}', building.worker.profession.colour))
            
            elif building.type == 'House':

                # Add villagers to description
                if building.villager != None:
                    name = building.villager.name
                    job = building.villager.profession.name
                    description.append((f'\n\nCurrently occupied by {name} the {job}', building.villager.profession.colour))
                else:
                    description.append((f'\n\nCurrently unoccupied', 'white'))
        
        # Return the complete description
        return description

    def update_building_text(self):
        '''Updates the text for the building display box'''
        
        # Get text data
        self.building_stats.config(state=tk.NORMAL)
        price_mod = self.villager.profession.get_price_modifier(self.villager)

        building_text = self.building.name
        title = "Building Cost:"
        food_text = f"Food: {round(self.building.cost['food'] * price_mod)}"
        wood_text = f"Wood: {round(self.building.cost['wood'] * price_mod)}"
        stone_text = f"Stone: {round(self.building.cost['stone'] * price_mod)}"
        building_description = self.building.description
        text = f"""{building_text}\n\n{title}\n{food_text}\n{wood_text}\n{stone_text}\n\n{building_description}"""
        
        # Add text to the box
        self.building_stats.config(state=tk.NORMAL)
        self.building_stats.delete('1.0', tk.END)
        self.building_stats.insert(tk.END, text)

        # Add colour to the stats
        self.colour_text('name', building_text, self.building.text_colour, '1.0')
        self.colour_text('label', title, 'white', '3.0')
        self.colour_text('food', food_text, 'lime', '4.0')
        self.colour_text('wood', wood_text, 'chocolate', '5.0')
        self.colour_text('stone', stone_text, 'gray72', '6.0')
        self.building_stats.tag_add('desc', '7.0', tk.END)
        self.building_stats.tag_config('desc', foreground=self.building.text_colour)

        self.building_stats.config(state=tk.DISABLED)
    
    def colour_text(self, name, text, colour, start_pos):
        '''Colours stats in the boxes'''

        # Add tag
        end_pos = start_pos[:2] + str(int(start_pos[2:]) + len(text))
        self.building_stats.tag_add(name, start_pos, end_pos)
        self.building_stats.tag_config(name, foreground=colour)

        # Return point at end of text
        return end_pos

    def draw_selector(self):
        '''Draws the selector onscreen that gives information about a tile'''

        # Get the size of the seletion
        if self.building != None:
            size = self.building.size
        else:
            size = (0,0)

        # Check the selector is withing bounds
        max_x = self.map.width - size[0]
        max_y = self.map.height - size[1]
        self.map.selector_x = max(1, min(self.map.selector_x, max_x))
        self.map.selector_y = max(1, min(self.map.selector_y, max_y))

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
                        self.can_build = True
                    else:
                        texture = (self.building.get_texture(xx+(yy*size[0]))[0], 'red')
                        self.can_build = False

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

    # Build a building in build mode
    def construct_building(self):
        '''Returns if a building can be constructed to a villager
            function is for self.constuct_button'''
        
        if self.can_build == True:
            self.villager.profession.turn_action_popout_closed(
                self.villager,
                self.building,
                (self.map.selector_x, self.map.selector_y)
            )
            
            # Reset variables out of building mode
            self.building = None
            self.build_positions = (None, None)
            self.villager = None

            # Close the gui
            self.root.destroy()
            self.root.update()

    def select_building(self, building):
        '''Changes onscreen building based on the selection menu'''

        self.building = config.get_building(building)

        # Draw building
        self.update_building_text()
        self.draw_selector()

    ### Moving selector ###
    def move_selector(self, dir):
        '''Move the sector and run any extra functions'''

        # Move is the correct direction and change varibles
        if dir == 'Right':
            self.map.selector_x += 1
        elif dir == 'Left':
            self.map.selector_x -= 1
        elif dir == 'Up':
            self.map.selector_y -= 1
        elif dir == 'Down':
            self.map.selector_y += 1

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

    def on_closing(self):
        '''Run on closing events'''

        self.building = None
        self.root.destroy()
        self.root.update()
