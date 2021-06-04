#
# Villager Game
# Main Game Application Module
# Written by Madeline Autumn
# Last modified on 04/06/21
#

### Importants and Varibles ###
import tkinter as tk
import config, villagerUI
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
        self.village_frame = tk.LabelFrame(self.left_frame, text='Village')
        self.village_frame.grid(row=0, column=0, padx=2, pady=2)

        # Create the frame for the statistics
        self.stats_frame = tk.LabelFrame(self.left_frame, text='Statistics')
        self.stats_frame.grid(row=1, column=0, padx=2, pady=2)

        # Create the labels for the statistics
        self.food_stat_var = tk.StringVar()
        self.food_stat_label = tk.Label(self.stats_frame, textvariable=self.food_stat_var)
        self.food_stat_label.grid(row=1, column=0, padx=8, pady=2, sticky=tk.NSEW)

        self.wood_stat_var = tk.StringVar()
        self.wood_stat_label = tk.Label(self.stats_frame, textvariable=self.wood_stat_var)
        self.wood_stat_label.grid(row=1, column=1, padx=8, pady=2, sticky=tk.NSEW)

        ## Centeral Frame ##
        # Create a scrollable frame for the villager modification section
        self.mod_frame = tk.Frame(self.center_frame)

        self.mod_canvas = tk.Canvas(self.mod_frame)
        self.mod_scrollbar = tk.Scrollbar(self.mod_frame,
                                          orient='vertical',
                                          command=self.mod_canvas.yview)

        self.mod_frame_scrollable = tk.Frame(self.mod_canvas)

        self.mod_frame_scrollable.bind("<Configure>", lambda e: self.mod_canvas.configure(scrollregion=self.mod_canvas.bbox("all")))

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
                                 state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, padx=4, pady=4)

        self.log_text.config(yscrollcommand=self.log_scrollbar.set)
        self.log_scrollbar.config(command=self.log_text.yview)

        self.update_stats()

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

        self.food_stat_var.set(f'Total Food: {config.food}')
        self.wood_stat_var.set(f'Total Wood: {config.wood}')

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
                # Only caluate food if needed
                if villager.hunger > 0:
                    if config.food > 0:
                        init_food = config.food
                        config.food -= villager.hunger
                        villager.hunger = 0
                        if config.food < 0:
                            # Add back food and hunger so that food > 0
                            villager.hunger += config.food*-1
                            config.food += config.food*-1
                        food_consumed = init_food - config.food
                        # Add result to log
                        villager.turn_log.append(f'{villager.name} has consumed {food_consumed} food')
                    else:
                        # Add result to log
                        villager.turn_log.append(f'There is no food for {villager.name} to consume')
                        # Add hunger if no food was consumed
                        villager.hunger += random.randint(config.hunger_range[0],
                                                          config.hunger_range[1])
                else:
                    # Add hunger if no food was consumed
                    villager.hunger += random.randint(config.hunger_range[0],
                                                      config.hunger_range[1])

    def end_turn(self):
        '''Run end of turn functions'''

        # Run through and feed all the villagers in the right order
        for priority in config.food_priority_values:
            self.feed_villagers(priority)

        # Run through all the villagers and run their actions
        for villager in config.villagers:
            villager.end_turn()

        # Updates onscreen logs
        self.log_text.config(state=tk.NORMAL)

        if config.turn > 1:
            self.log_text.insert(tk.END, f'\nTurn {config.turn}\n')
        else:
            self.log_text.insert(tk.END, f'Turn {config.turn}\n')

        for line in config.turn_log:
            self.log_text.insert(tk.END, f'{line}\n')
        self.log_text.see("end")
        
        self.log_text.config(state=tk.DISABLED)

        # Add the turns log to the main log and reset the turn log
        for line in config.turn_log:
            config.log.append(line)
        config.turn_log = []

        # Run the beginning of turn functions just before the next turn begins
        for villager in config.villagers:
            villager.begin_turn()

        # Update turn counter and add to the logs
        config.turn += 1
        config.log.append(f'\nTurn {config.turn}')

        # Update the gui
        self.update_stats()
