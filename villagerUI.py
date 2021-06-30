#
# Villager Game
# VilalgerUI Module
# Written by Madeline Autumn
#

### Importants and Varibles ###

import tkinter as tk
import config

### Classes ###

## Villager Frame Class ##
class VillagerFrame:
    '''Stores the data for the frame of each villager onscreen'''

    def __init__(self, parent, villager, id):
        
        self.parent = parent
        self.villager = villager
        self.id = id

        self.villager.frame = self

    def create_widgets(self):
        '''Create the widgets onscreen for the villager'''
        
        # Create the main frame for the villager
        self.frame = tk.Frame(self.parent.mod_frame_scrollable, relief=tk.GROOVE, 
                              borderwidth=2, width=12)
        self.frame.grid(row=self.id, column=0, padx=2, pady=4, sticky='')

        # Creat the four frames for the widgets 
        self.ascii_frame = tk.Frame(self.frame)
        self.ascii_frame.grid(row=0, column=0, rowspan=2)

        self.stats_frame = tk.Frame(self.frame)
        self.stats_frame.grid(row=0, column=1)

        self.button_frame = tk.Frame(self.frame)
        self.button_frame.grid(row=0, column=2, rowspan=2)

        self.profession_frame = tk.Frame(self.frame)
        self.profession_frame.grid(row=1, column=1)
        
        # Ascii frame widgets #
        self.ascii_art = tk.Label(self.ascii_frame, text='', relief=tk.GROOVE, borderwidth=2, width=8)
        self.ascii_art.grid(row=0, column=0, padx=2, pady=2, sticky=tk.EW)

        self.ascii_name_var = tk.StringVar()
        self.ascii_name = tk.Label(self.ascii_frame, textvariable=self.ascii_name_var)
        self.ascii_name.grid(row=1, column=0, padx=2, pady=2, sticky=tk.EW)

        self.kill_button = tk.Button(self.ascii_frame, text='Kill', 
                                     width=8, command=self.villager.kill)
        self.kill_button.grid(row=2, column=0, padx=2, pady=2)

        # Stats frame widgets #
        self.title = tk.StringVar()
        self.name_button = tk.Button(self.stats_frame, textvariable=self.title, 
                                     width=35, command=self.open_villager_window)
        self.name_button.grid(row=0, column=0, padx=2, pady=6, sticky=tk.NSEW)

        self.stats_box = tk.Text(self.stats_frame,
                                  width=44, 
                                  height=1,
                                  state=tk.DISABLED,
                                  bg='black')

        self.stats_box.grid(row=1, column=0, padx=2, pady=0, sticky=tk.NSEW)

        # Professions frame widgets #
        self.professions_menu_var = tk.StringVar()
        self.professions_menu_var.set(self.villager.profession.name)

        self.professions_list = config.professions_dict.keys()
        self.professions_menu = tk.OptionMenu(self.profession_frame,
                                              self.professions_menu_var, 
                                              *self.professions_list,
                                              command=self.set_profession)
        self.professions_menu.config(width=14)
        self.professions_menu.grid(row=2, column=0, padx=2, pady=6, sticky=tk.NSEW)

        # Button Frame widgets #
        self.food_label = tk.Label(self.button_frame, text='Food Priority:')
        self.food_label.grid(row=0, column=0, padx=2, pady=4, sticky=tk.NSEW)
        self.food_menu_var = tk.StringVar()
        self.food_menu_var.set(config.food_priority_values[1])

        for value in config.food_priority_values:
            tk.Radiobutton(self.button_frame,
                           text=value, value=value,
                           variable=self.food_menu_var,
                           indicator = 0, width=6,).grid(padx=2, pady=2)

    def set_profession(self, profession):
        '''Upates the villager profession based on the profession menu'''

        self.villager.profession = config.professions_dict[profession]
        self.update_stats()

        # Reset stats associated with profession
        self.villager.turn_action = None
        if self.villager.work_building != None:
            self.villager.work_building.worker = None
            self.villager.work_building = None

        if self.villager.profession.building != None:
            self.villager.assign_work_building()

        # Attempt to add action button for certain professions
        try:
            self.action_button.grid_remove()
        except:
            pass

        try:
            self.action_button = tk.Button(self.profession_frame, 
                                           text=self.villager.profession.action_text,
                                           width=12,
                                           command=lambda: self.villager.profession.turn_action(self.villager))
            self.action_button.grid(row=2, column=1, padx=2, pady=6, sticky=tk.NSEW)
        except:
            pass

    def open_villager_window(self):
        '''Opens the window for a detailed villager view'''

        self.villager_window = VillagerInfoWindow(self, self.villager)
    
    def update_stats(self):
        '''Updates the onscreen stats and data for the villager'''

        self.ascii_name_var.set(self.villager.name)
        self.title.set(f'{self.villager.name} the {self.villager.profession.name}')

        # Get the stats varible
        space = '   '
        health = f'Health: {self.villager.health}{space}'
        hunger = f'Hunger: {self.villager.hunger}{space}'
        morale = f'Morale: {self.villager.morale}'

        self.stats = health + hunger + morale

        # Insert stats into the statbox
        self.stats_box.config(state=tk.NORMAL)
        self.stats_box.delete(1.0, tk.END)
        self.stats_box.insert(1.0, self.stats)

        # Health colouring
        health_start = '1.0'
        health_end = '1.' + str(len(health)-1)
        self.stats_box.tag_add('Health', health_start, health_end)
        self.stats_box.tag_config('Health', 
                                  foreground='red', 
                                  justify=tk.CENTER)

        # Hunger colouring
        hunger_start = str(float(health_end))
        hunger_end = '1.' + str(int(hunger_start[2:]) + len(hunger))
        self.stats_box.tag_add('Hunger', hunger_start, hunger_end)
        self.stats_box.tag_config('Hunger', 
                                  foreground='lime', 
                                  justify=tk.CENTER)

        # Morale colouring
        morale_start = str(float(hunger_end))
        morale_end = '1.' + str(int(morale_start[2:]) + len(morale)+1)
        self.stats_box.tag_add('Morale', morale_start, morale_end)
        self.stats_box.tag_config('Morale', 
                                  foreground='yellow', 
                                  justify=tk.CENTER)

        # Turn box off at end
        self.stats_box.config(state=tk.DISABLED)

## Villager info window ##

class VillagerInfoWindow:
    '''Brings up a window with all the information for the villager'''

    def __init__(self, parent, villager):

        self.parent = parent
        self.villager = villager

        # Disable ending turn and modifying villager while open
        parent.professions_menu.config(state=tk.DISABLED)
        parent.kill_button.config(state=tk.DISABLED)
        parent.name_button.config(state=tk.DISABLED)
        'Action button to be added'
        parent.parent.end_turn_button.config(state=tk.DISABLED)

        # Initiate the window
        self.root = tk.Toplevel(parent.parent.root)
        self.root.title(parent.title.get())
        self.root.resizable(width=0, height=0)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Add the title, stats, biography and logs
        info_frame = tk.Frame(self.root)
        info_frame.grid(row=0, column=0, columnspan=2, padx=8, pady=4)

        title = tk.Label(info_frame, text=parent.title.get(), width=88)
        title.grid(row=0, column=0, pady=4)

        stats = tk.Label(info_frame, text=parent.stats)
        stats.grid(row=1, column=0, pady=4)

        bio_frame = tk.Frame(self.root)
        bio_frame.grid(row=1, column=0, padx=8, pady=8)

        log_frame = tk.Frame(self.root)
        log_frame.grid(row=1, column=1, padx=8, pady=8)

        # Biography frame data
        bio_scrollbar = tk.Scrollbar(bio_frame)
        bio_scrollbar.grid(row=0, column=1, sticky=tk.NSEW)

        bio_text = tk.Text(bio_frame, width=32, height=12, wrap=tk.WORD)
        bio_text.grid(row=0, column=0, padx=4, pady=4)

        bio_text.config(yscrollcommand=bio_scrollbar.set)
        bio_scrollbar.config(command=bio_text.yview)

        bio_text.config(state=tk.DISABLED)
        
        # Log frame data
        log_scrollbar = tk.Scrollbar(log_frame)
        log_scrollbar.grid(row=0, column=1, sticky=tk.NSEW)

        log_text = tk.Text(log_frame, width=32, height=12, wrap=tk.WORD, bg='black')
        log_text.grid(row=0, column=0, padx=4, pady=4)

        log_text.config(yscrollcommand=log_scrollbar.set)
        log_scrollbar.config(command=log_text.yview)

        for line in villager.log:
            
            # Insert line
            log_text.insert(tk.END, f'{line[0]}\n')
            log_text.see("end")

            # Colour Text
            tag_id = int(log_text.index('end-1c').split('.')[0]) - 1
            log_text.tag_add(tag_id, float(tag_id), float(tag_id+1))
            log_text.tag_config(tag_id, foreground=line[1])


        log_text.config(state=tk.DISABLED)
    
    def on_closing(self):
        '''Renable the buttons when window is closed'''

        self.parent.professions_menu.config(state=tk.NORMAL)
        self.parent.kill_button.config(state=tk.NORMAL)
        self.parent.name_button.config(state=tk.NORMAL)
        'Action button to be added'
        self.parent.parent.end_turn_button.config(state=tk.NORMAL)

        self.root.destroy()
