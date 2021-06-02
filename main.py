#
# Villager Game
# Main Module
# Written by Madeline Autumn
# Last modified on 03/06/21
#

### Importants and Varibles ###
import tkinter as tk
import villagers, professions

### Game Application Class ###

class GameApp:

    def __init__(self):
        
        # Initialize the window
        self.root = tk.Tk()
        self.root.title('Villager game')
        self.root.resizable(width=0, height=0)

        # Create the two frames for the gui
        self.left_frame = tk.LabelFrame(self.root, text='')
        self.right_frame = tk.LabelFrame(self.root, text='')
        self.left_frame.grid(row=0, column= 0, padx= 4, pady= 4)
        self.right_frame.grid(row=0, column= 1, padx= 4, pady= 4)

        # Create the frames for the village
        self.village_frame = tk.LabelFrame(self.left_frame, text='Village', width= 48)
        self.village_frame.grid(row=0, column= 0, padx= 2, pady= 2)

        # Create the frame for the statistics
        self.stats_frame = tk.LabelFrame(self.left_frame, text='Statistics')
        self.stats_frame.grid(row=1, column= 0, padx= 2, pady= 2)

### Main Game Loop ###

if __name__ == '__main__':
    main_app = GameApp()
    main_app.root.mainloop()
