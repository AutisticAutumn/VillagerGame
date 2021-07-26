#
# Villager Game
# Menu Module
# Written by Madeline Autumn
#

### Importants and Varibles ###
import tkinter as tk
import config, string

### Classes ###
class Del:
  def __init__(self, keep=string.digits):
    self.comp = dict((ord(c),c) for c in keep)
  def __getitem__(self, k):
    return self.comp.get(k)

DD = Del()

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
        self.creation_root.title('Create Game')
        self.creation_root.resizable(width=0, height=0)

        # Widgets
        self.village_name = tk.StringVar()
        self.name_box = tk.Entry(self.creation_root,
                                 width=24,
                                 textvariable=self.village_name)
        self.village_name.set('Unnamed Village')
        self.name_box.grid(row=0, column=0, padx=8, pady=8)
        self.name_box.bind("<FocusOut>", self.round_data)

        self.settings_frame = tk.Frame(self.creation_root)
        self.settings_frame.grid(row=1, column=0, padx=8, pady=8)

        self.settings_title = tk.Label(self.settings_frame, text='World Settings')
        self.settings_title.grid(row=0, column=0, columnspan=2, pady=4)

        self.width_text = tk.Label(self.settings_frame, text='Width:')
        self.width_text.grid(row=1, column=0, sticky=tk.E)

        self.width = tk.StringVar()
        self.width_box = tk.Entry(self.settings_frame,
                                  width=10,
                                  textvariable=self.width)
        self.width.set(config.map.default_width)
        self.width_box.grid(row=1, column=1, sticky=tk.W, pady=2)
        self.width_box.bind("<FocusOut>", self.round_data)

        self.height_text = tk.Label(self.settings_frame, text='Height:')
        self.height_text.grid(row=2, column=0, sticky=tk.E)

        self.height = tk.StringVar()
        self.height_box = tk.Entry(self.settings_frame,
                                  width=10,
                                  textvariable=self.height)
        self.height.set(config.map.default_height)
        self.height_box.grid(row=2, column=1, sticky=tk.W, pady=2)
        self.height_box.bind("<FocusOut>", self.round_data)

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

        # Track entry boxes to keep data in range
        self.village_name.trace("w", lambda name, index, mode: self.round_data())
        
    def round_data(self, button=None):
        '''Make sure all entered data is within bounds'''

        self.village_name.set(self.village_name.get()[:24])

        self.width.set(self.width.get().translate(DD))
        self.width.set(max(int(self.width.get()), config.world_size_min))
        self.width.set(min(int(self.width.get()), config.world_size_max))

        self.height.set(self.height.get().translate(DD))
        self.height.set(max(int(self.height.get()), config.world_size_min))
        self.height.set(min(int(self.height.get()), config.world_size_max))

        config.map.width = int(self.width.get())
        config.map.height = int(self.height.get())
        config.map.get_world_data()

    def create_world(self):
        '''Close the application and begin the game'''

        # Adjust config variables accordingly
        config.village_name = self.village_name.get()

        # Adjust variables for main loop
        self.generate_world = True
        self.quit = False

        # Close window and begin generating world
        self.root.destroy()
