#
# Villager Game
# Main Game Application Module
# Written by Madeline Autumn
# Last modified on 05/06/21
#

### Importants and Varibles ###
import tkinter as tk
import config, villagerUI, mapUI
import random

### Classes ###
class GameApp:
    '''The main game routine application'''

    def __init__(self):
        
        # Initialize the window
        self.root = tk.Tk()
        self.root.title('Villager game')
        self.root.resizable(width=0, height=0)

        # Create the two frames for the gui
        self.left_frame = tk.LabelFrame(self.root, text='')
        self.center_frame = tk.LabelFrame(self.root, text='')
        self.right_frame = tk.LabelFrame(self.root, text='')

        self.left_frame.grid(row=0, column=0, padx=4, pady=4)
        self.center_frame.grid(row=0, column=1, padx=4, pady=4)
        self.right_frame.grid(row=0, column=2, padx=4, pady=4)

        ## Left Frame ##
        # Create the frames for the village
        self.village_frame = tk.Frame(self.left_frame)
        self.village_frame.grid(row=0, column=0, padx=2, pady=2, sticky= tk.NSEW)
        self.map = mapUI.MapFrame(self, self.village_frame)
        
        self.stats_box = tk.Text(self.left_frame,
                                 width=48, 
                                 height=1,
                                 state=tk.DISABLED,
                                 bg='black')
        self.stats_box.grid(row=1, column=0, padx=6, pady=6, sticky=tk.W)

        ## Centeral Frame ##
        # Create a scrollable frame for the villager modification section
        self.mod_frame = tk.Frame(self.center_frame)

        self.mod_canvas = tk.Canvas(self.mod_frame, height= 320)
        self.mod_scrollbar = tk.Scrollbar(self.mod_frame,
                                          orient='vertical',
                                          command=self.mod_canvas.yview)

        self.mod_frame_scrollable = tk.Frame(self.mod_canvas )

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
        self.end_turn_button = tk.Button(self.center_frame, 
                                         text='End Turn', 
                                         width=48, 
                                         command=self.end_turn)
        self.end_turn_button.grid(row=1, column=0, padx=2, pady=4)

        ## Right Frame ##
        self.log_scrollbar = tk.Scrollbar(self.right_frame)
        self.log_scrollbar.grid(row=0, column=1, sticky=tk.NSEW)

        self.log_text = tk.Text(self.right_frame, 
                                 width=48, 
                                 height=24,
                                 state=tk.DISABLED,
                                 wrap=tk.WORD,
                                 bg='black')
        self.log_text.grid(row=0, column=0, padx=4, pady=4)

        self.log_text.config(yscrollcommand=self.log_scrollbar.set)
        self.log_scrollbar.config(command=self.log_text.yview)

        self.update_stats()
        self.append_log('Turn 1')

    def add_villager_frame(self, villager):
        '''Creates the frame onscreen to display the villager'''

        villager_frame = villagerUI.VillagerFrame(self, villager, len(self.villager_frames))
        self.villager_frames.append(villager_frame)
        villager_frame.create_widgets()

    def create_villager_frames(self):
        '''Runs through all villagers and frames them all'''

        self.villager_frames = []
        for villager in config.villagers:
            self.add_villager_frame(villager)

    def update_stats(self):
        '''Updates the onscreen stats'''

        # Update the stats 
        food_text = f'Total Food: {config.food}    '
        wood_text = f'Total Wood: {config.wood}'

        self.stats_box.config(state=tk.NORMAL)

        # Add text to the box
        self.stats_box.delete('1.0', tk.END)
        self.stats_box.insert(tk.END, food_text + wood_text)

        # Add colour to the stats
        food_start = '1.0'
        food_end = '1.' + str(len(food_text)-1)
        self.stats_box.tag_add('food', food_start, food_end)
        self.stats_box.tag_config('food', 
                                  foreground='lime', 
                                  justify=tk.CENTER)

        wood_start = str(float(food_end)+0.01)
        wood_end = '1.' + str(int(wood_start[2:]) + len(wood_text))
        self.stats_box.tag_add('wood', wood_start, wood_end)
        self.stats_box.tag_config('wood', 
                                  foreground='chocolate', 
                                  justify=tk.CENTER)

        self.stats_box.config(state=tk.DISABLED)

        # Update the villagers
        for villager_frame in self.villager_frames:
            villager_frame.update_stats()

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

    def append_log(self, line, colour='white'):
        '''Append a single line to the log'''

        self.log_text.config(state=tk.NORMAL)

        # Add line
        self.log_text.insert(tk.END, f'{line}\n')
        self.log_text.see("end")

        # Colour Text
        tag_id = int(self.log_text.index('end-1c').split('.')[0]) - 1
        self.log_text.tag_add(tag_id, float(tag_id), float(tag_id+1))
        self.log_text.tag_config(tag_id, foreground=colour)

        self.log_text.config(state=tk.DISABLED)

        config.log.append((line, colour))

    def end_turn(self):
        '''Run end of turn functions'''

        # Run through and feed all the villagers in the right order
        for priority in config.food_priority_values:
            self.feed_villagers(priority)

        # Run through all the villagers and run their actions
        for villager in config.villagers:
            villager.end_turn()

        # Run the beginning of turn functions just before the next turn begins
        for villager in config.villagers:
            villager.begin_turn()

        # Update turn counter and add to the logs
        config.turn += 1
        self.append_log(f'\nTurn {config.turn}')

        # Update the gui
        self.update_stats()
        self.map.draw_map()
