#
# Villager Game
# Menu Module
# Written by Madeline Autumn
#

### Importants and Varibles ###
import tkinter as tk
import config

### Classes ###

class MenuApp():
    '''The popout for the menu'''

    def __init__(self):

        # Variables
        self.generate_world = False
        self.quit = True
        
        # Initialize the window
        self.root = tk.Tk()
        self.root.title('Villager game')
        self.root.resizable(width=0, height=0)

        # Add the widgets
        self.title = tk.Label(self.root,
                             text='Villager Game',
                             justify=tk.CENTER)
        self.title.grid(row=0, column=0, columnspan=3, padx=8, pady=16)

        self.new_game = tk.Button(self.root,
                                  text='New Game',
                                  width=10,
                                  command=self.create_world_menu)
        self.new_game.grid(row=1, column=0, padx=4, pady=8)

        self.load_game = tk.Button(self.root,
                                   text='Load Game',
                                   width=10,
                                   state=tk.DISABLED)
        self.load_game.grid(row=1, column=1, padx=4, pady=8)

        self.quit_game = tk.Button(self.root,
                                   text='Quit',
                                   width=10,
                                   command=self.root.destroy)
        self.quit_game.grid(row=1, column=2, padx=4, pady=8)

    def create_world_menu(self):
        '''Brings up a toplevel for world creation'''

        # Initiate toplevel
        self.creation_root = tk.Toplevel()
        self.root.title('Create Game')
        self.root.resizable(width=0, height=0)

        # Widgets
        self.village_name = tk.StringVar()
        self.name_box = tk.Entry(self.creation_root,
                                 width=24,
                                 textvariable=self.village_name)
        self.village_name.set('Unnamed Village')
        self.name_box.grid(row=0, column=0, padx=8, pady=8)

        self.settings_frame = tk.Frame(self.creation_root)
        self.settings_frame.grid(row=1, column=0, padx=8, pady=8)

        self.advanced_settings_button = tk.Button(self.creation_root,
                                                  text='Advanced settings',
                                                  width=16,
                                                  state=tk.DISABLED)
        self.advanced_settings_button.grid(row=2, column=0, padx=8, pady=8)

        self.create_world_button = tk.Button(self.creation_root,
                                             text='Create World',
                                             width=24,
                                             height=2,
                                             command=self.create_world)

        self.create_world_button.grid(row=3, column=0, padx=8, pady=8)

    def create_world(self):
        '''Close the application and begin the game'''

        # Adjust config variables accordingly
        config.village_name = self.village_name.get()[:24]

        # Adjust variables for main loop
        self.generate_world = True
        self.quit = False

        # Close window and begin generating world
        self.root.destroy()
