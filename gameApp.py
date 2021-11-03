#
# Villager Game
# Main Game Application Module
# Written by Madeline Autumn
#

### Importants and Varibles ###
import tkinter as tk
import config, villagerUI, mapUI, buildings
import random

### Classes ###
class GameApp:
    '''The main game routine application'''

    def __init__(self):

        # Get the frame sizes based on gui
        if config.gui_size == config.gui_size_values[0]:
            villager_size = (574, 192)
            log_size = (124, 10)
            self.font_size = 8
        elif config.gui_size == config.gui_size_values[1]:
            villager_size = (500, 276)
            log_size = (108, 16)
            self.font_size = 9
        else:
            villager_size = (574, 374)
            log_size = (124, 23)
            self.font_size = 10
        
        self.font = (config.main_font, self.font_size)

        # Initialize the window
        self.root = tk.Tk()
        self.set_title()
        self.root.resizable(width=0, height=0)

        # Create the three frames for the gui
        self.map_frame = tk.LabelFrame(self.root, text='')
        self.log_frame = tk.LabelFrame(self.root, text='')
        self.bottom_frame = tk.LabelFrame(self.root, text='')
        
        self.map_frame.grid(row=0, column=0, padx=4, pady=4)
        self.log_frame.grid(row=2, column=0, columnspan=2, padx=4, pady=4)
        self.bottom_frame.grid(row=0, column=1, padx=4, pady=4)

        ## Map Frame ##
        # Create the frames for the village
        self.village_frame = tk.Frame(self.map_frame)
        self.village_frame.grid(row=0, column=0, padx=2, pady=2, sticky= tk.NSEW)
        self.map = mapUI.MapFrame(self, self.village_frame)

        self.map_button = tk.Button(self.map_frame, text='View full map',
                                    width=16, font=self.font,
                                    command=config.map.popout.create_toplevel)
        self.map_button.grid(row=1, column=0, padx=2, pady=4)

        ## Log Frame ##
        self.log_scrollbar = tk.Scrollbar(self.log_frame)
        self.log_scrollbar.grid(row=0, column=1, sticky=tk.NSEW)

        self.log_text = tk.Text(self.log_frame, 
                                width=log_size[0], 
                                height=log_size[1],
                                state=tk.DISABLED,
                                wrap=tk.WORD,
                                bg='black',
                                font=self.font)
        self.log_text.grid(row=0, column=0, padx=5, pady=5)

        self.log_text.config(yscrollcommand=self.log_scrollbar.set)
        self.log_scrollbar.config(command=self.log_text.yview)

        # Stat box
        self.stats_box = tk.Text(self.root,
                                 width=64, 
                                 height=2,
                                 state=tk.DISABLED,
                                 bg='black',
                                 font=self.font)
        self.stats_box.grid(row=1, column=0, columnspan=2, padx=12, pady=4)

        ## Bottom Frame ##
        # Create a scrollable frame for the villager modification section
        self.mod_frame = tk.Frame(self.bottom_frame)

        self.mod_canvas = tk.Canvas(self.mod_frame, height=villager_size[1], width=villager_size[0])
        self.mod_scrollbar = tk.Scrollbar(self.mod_frame,
                                          orient='vertical',
                                          command=self.mod_canvas.yview)

        self.mod_frame_scrollable = tk.Frame(self.mod_canvas)

        self.mod_frame_scrollable.bind("<Configure>", 
                                           lambda e: self.mod_canvas.configure(
                                               scrollregion=self.mod_canvas.bbox("all")
                                            )
                                        )

        self.mod_canvas.create_window((0, 0), window=self.mod_frame_scrollable, anchor="nw")
        self.mod_canvas.configure(yscrollcommand=self.mod_scrollbar.set)

        self.mod_frame.grid(row=0, column=0, padx=2, pady=2, sticky=tk.NSEW)
        self.mod_canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.mod_scrollbar.grid(row=0, column=1, sticky=tk.NSEW)

        # Add the villager modification frames
        self.create_villager_frames()

        # Button to end turn
        self.end_turn_button = tk.Button(self.root, 
                                         text='End Turn', 
                                         width=48, 
                                         command=self.end_turn,
                                         borderwidth=4,
                                         bg='grey84',
                                         font=self.font)
        self.end_turn_button.grid(row=3, column=0, columnspan=2, padx=2, pady=4)

        self.update_stats()
        response = config.get_response('new_turn')
        response[0] = response[0].format(config.turn).strip()
        self.append_log(response)

    def set_title(self):
        '''Sets the widget title'''
        self.root.title(f'{config.village_name}  |  Turn: {config.turn}')

    def add_villager_frame(self, villager):
        '''Creates the frame onscreen to display the villager'''

        villager_frame = villagerUI.VillagerFrame(self, villager, len(self.villager_frames)*2)
        self.villager_frames.append(villager_frame)
        villager_frame.create_widgets()

    def create_villager_frames(self):
        '''Runs through all villagers and frames them all'''

        self.villager_frames = []
        for villager in config.villagers:
            self.add_villager_frame(villager)

    def update_stats(self):
        '''Updates the onscreen stats'''

        # Get text 
        name_text = config.village_name
        turn_text = f'Turn: {config.turn}'
        food_text = f'Total Food: {config.food}'
        wood_text = f'Total Wood: {config.wood}'
        stone_text = f'Total Stone: {config.stone}'
        
        text = f'{name_text}  |  {turn_text}'
        text += f'\n{food_text}  |  {wood_text}  |  {stone_text}'

        # Add text to the box
        self.stats_box.config(state=tk.NORMAL)
        self.stats_box.delete('1.0', tk.END)
        self.stats_box.insert(tk.END, text)
        
        # Justify the text
        self.stats_box.tag_add('justify', '1.0', tk.END)
        self.stats_box.tag_config('justify', justify=tk.CENTER)

        ## Add colour to the stats ##
        # Row 1
        end_point = self.colour_stat('name', name_text, 'white', '1.0')
        end_point = self.colour_bar('bar_1', end_point)
        end_point = turn_end = self.colour_stat('turn', turn_text, 'white', end_point)

        # Row 2
        end_point = self.colour_stat('food', food_text, 'lime', '2.0')
        end_point = self.colour_bar('bar_2', end_point)
        end_point = self.colour_stat('wood', wood_text, 'chocolate', end_point)
        end_point = self.colour_bar('bar_3', end_point)
        end_point = self.colour_stat('stone', stone_text, 'gray72', end_point)

        self.stats_box.config(state=tk.DISABLED)

        # Update the villagers
        for villager_frame in self.villager_frames:
            villager_frame.update_stats()
        
        # Update the map
        mapUI.draw_map(self.map)

    def colour_bar(self, name, end_pos):
        '''Colours the bars in stats'''

        self.stats_box.tag_add(name, end_pos + '+2c', end_pos + '+3c')
        self.stats_box.tag_config(name, foreground='white')

        return end_pos[:2] + str(int(end_pos[2:])+5)

    def colour_stat(self, name, text, colour, start_pos):
        '''Colours stats in the stat box'''

        # Add tag
        end_pos = start_pos[:2] + str(int(start_pos[2:]) + len(text))
        self.stats_box.tag_add(name, start_pos, end_pos)
        self.stats_box.tag_config(name, foreground=colour)

        # Return point at end of text
        return end_pos

    def feed_villagers(self, priotity):
        '''Runs through the list of villagers and uses the frame to
            check for the right priotity'''
        
        # Create a list of the villagers that match the priotity
        feeding = []
        for villager_frame in self.villager_frames:
            if villager_frame.food_menu_var.get() == priotity:
                feeding.append(villager_frame.villager)

        # Shuffle the list and feed the apprioprite villagers
        if feeding != []:
            random.shuffle(feeding)
            for villager in feeding:
                villager.feed_villager()

    def append_log(self, response):
        '''Append a single line to the log'''

        self.log_text.config(state=tk.NORMAL)

        # Add line
        self.log_text.insert(tk.END, f'{response[0]}\n')
        self.log_text.see("end")

        # Colour Text
        tag_id = int(self.log_text.index('end-1c').split('.')[0]) - 1
        self.log_text.tag_add(tag_id, float(tag_id), float(tag_id+1))
        self.log_text.tag_config(tag_id, foreground=response[1])

        self.log_text.config(state=tk.DISABLED)

        config.log.append(response)

    def end_turn(self):
        '''Run end of turn functions'''

        # Run through and feed all the villagers in the right order
        for priority in config.food_priority_values:
            self.feed_villagers(priority)

        # Run through all the villagers and run their actions
        for villager in config.villagers:
            villager.end_turn()

        # End game if no villagers are remaining
        if len(config.villagers) == 0:
            self.append_log(['\nThere are no villagers remaining', 'white'])
            self.append_log(['GAME OVER', 'white'])
            self.end_turn_button.config(state=tk.DISABLED)
            mapUI.draw_map(config.map.frame)
            return False

        # Attempt to run end of turn functions for disaster
        if config.disaster != None:
            config.disaster.end_turn()

        # Update turn counter and add to the logs
        config.turn += 1
        response = config.get_response('new_turn')
        response[0] = '\n' + response[0].format(config.turn)
        self.append_log(response)

        # Attempt to start a disaster
        disaster_chance = random.randint(1, max(config.disaster_chance, 1)) == 1
        disaster_free = config.disaster == None

        if disaster_chance and disaster_free and config.turn > 8:
            
            # Select a random disaster from the list
            disaster = random.choice(config.disaster_list)
            config.disaster = config.get_disaster(disaster)
            config.disaster.on_start()

        else:
            # Increase chance if no disaster has occured
            config.disaster_chance -= 1

        # Find average morale levels
        average_morale = 0
        for villager in config.villagers:
            average_morale += villager.morale
        average_morale /= len(config.villagers)

        # Attempt to add new villagers if there is space
        if len(config.villagers) < config.max_villagers and average_morale > -1:
            
            chance = int(10 / config.arrival_chance)

            # Random chance for villager to arrive
            if random.randint(1, chance) < 10:
                config.create_villager()

                # Return response to log
                response = config.get_response('arrival')
                response[0] = response[0].format(config.villagers[-1].name)
                self.append_log(response)

        # Attempt to run start of turn functions for disaster
        if config.disaster != None:
            config.disaster.begin_turn()

        # Run the beginning of turn functions just before the next turn begins
        config.feller_trees = []
        for villager in config.villagers:
            villager.begin_turn()

        # Update the gui and map
        self.update_stats()
        self.set_title()
