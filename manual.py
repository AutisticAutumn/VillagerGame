#
# Villager Game
# Manual Module
# Written by Madeline Autumn
#

### Imports and variables ###
import tkinter as tk
import config


### Manual class ###
class Manual:

    def __init__(self):

        self.get_manual_dictionary()
        self.open_manual()

    def open_manual(self):
        '''Opens the manual'''

        self.root = tk.Toplevel()

        self.root.title('Villager game manual')
        self.root.resizable(width=0, height=0)

        # Draw in buttons along edge
        self.selection_frame = tk.Frame()
        self.selection_frame.grid(row=0, column=0)

        self.widgets = {}

        for name, button_type in self.button_list.items():

            # Get widget type
            if button_type == 'text':

                button = tk.Button(self.selection_frame,
                                   text=name,
                                   width=20,
                                   height=2)
                button.grid(padx=4, pady=4)

                self.widgets.update({name: [button]})

            elif button_type == 'menu':
                
                menu_data = self.menus[name]
                menu_var = tk.StringVar()

                menu = tk.OptionMenu(self.selection_frame,
                                     menu_var,
                                     *menu_data)
                menu.config(width=18, height=2)
                menu.grid(padx=4, pady=4)

                menu_var.set(menu_data[0])

                self.widgets.update({name: [menu, menu_var]})

    def get_manual_dictionary(self):
        '''Creates the dicionary for the manual'''

        self.menus = {}
        data_temp = {}
        self.data = {}
        self.button_list = {}

        # Open file with the responses
        with open('Assets/Manual', 'r') as f:
            
            lines = f.readlines()

            mode = 'FindEntry'
            key = ''
            values = []

            for line in lines:

                # Check for the next { to begin writing the next dictonary statement
                if mode == 'FindEntry':
                    if line.strip() == '{':
                        mode = 'GetKey'

                # Find the key for the dictonary item
                elif mode == 'GetKey':
                    key = line.strip()
                    mode = 'GetValues'

                # Get the values for the dictonary
                elif mode == 'GetValues':

                    # If end of entry find the next item
                    if line.strip() == '}':
                        
                        # Add key to the order of buttons
                        self.button_list.update({key: values[0]})

                        # Add values to correct dictionary
                        if values[0] == 'text':
                            values.pop(0)
                            data_temp[key] = values
                        elif values[0] == 'menu':
                            values.pop(0)
                            self.menus[key] = values

                        # Reset variables
                        key = ''
                        values = []
                        mode = 'FindEntry'
                    else:
                        values.append(line.strip())
        
        # Join text data together
        for key, value in data_temp.items():
            self.data.update({key : ' '.join(value)})
            
        print(self.data, '\n')
        print(self.menus)
        print(self.button_list)
