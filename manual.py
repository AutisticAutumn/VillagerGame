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

    def open_manual(self):
        '''Opens the manual'''

        self.root = tk.Toplevel()

        self.root.title('Villager game manual')
        self.root.resizable(width=0, height=0)


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