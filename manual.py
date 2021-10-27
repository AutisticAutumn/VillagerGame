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

        # Draw in buttons along edge
        self.selection_frame = tk.Frame(self.root)
        self.selection_frame.grid(row=0, column=0)

        self.widgets = {}

        for name, button_type in self.button_list.items():

            widget = ManualWidget(name, button_type, self)
            self.widgets.update({name: widget})

        # Add text box
        self.text_frame = tk.Frame(self.root)
        self.text_frame.grid(row=0, column=1, padx=8, pady=8, sticky=tk.NSEW)

        self.text_var = tk.StringVar()
        self.text = tk.Label(self.text_frame, 
                             textvariable=self.text_var,
                             relief='ridge',
                             borderwidth=2,
                             width=32)
        self.text.grid(sticky=tk.NSEW)

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
                        if  values[0] != 'menutext':
                            self.button_list.update({key: values[0]})

                        # Add values to correct dictionary
                        if 'text' in values[0]:
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
    
    def update_text(self, key):
        '''Update the text onscreen on the manual'''

        self.text_var.set(self.data[key])

class ManualWidget:

    def __init__(self, name, widget_type, parent):
        
        self.name = name
        self.type = widget_type
        self.parent = parent

        # Initiate the widget

        if self.type == 'text':

            self.data = parent.data[name]

            self.button = tk.Button(parent.selection_frame,
                                    text=name,
                                    width=20,
                                    height=2,
                                    command=lambda: parent.update_text(name))
            self.button.grid(padx=4, pady=4)

        elif self.type == 'menu':
            
            self.data = parent.menus[name]
            self.menu_var = tk.StringVar()

            self.menu = tk.OptionMenu(parent.selection_frame,
                                      self.menu_var,
                                      *self.data,
                                      command=parent.update_text)
            self.menu.config(width=18, height=2)
            self.menu.grid(padx=4, pady=4)

            self.menu_var.set(self.data[0])

    
