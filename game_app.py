#
# Villager Game
# Main Game Application Module
# Written by Madeline Autumn
# Last modified on 03/06/21
#

### Importants and Varibles ###
import tkinter as tk
import config

### Game Application Class ###

class GameApp:

    def __init__(self):
        
        # Initialize the window
        self.root = tk.Tk()
        self.root.title('Villager game')
        self.root.resizable(width=0, height=0)

        # Create the two frames for the gui
        self.left_frame = tk.LabelFrame(self.root, text='')
        self.center_frame = tk.LabelFrame(self.root, text='')
        self.right_frame = tk.LabelFrame(self.root, text='')
        self.left_frame.grid(row=0, column= 0, padx= 4, pady= 4)
        self.center_frame.grid(row=0, column= 1, padx= 4, pady= 4)
        self.right_frame.grid(row=0, column= 2, padx= 4, pady= 4)

        # Left Frame
        # Create the frames for the village
        self.village_frame = tk.LabelFrame(self.left_frame, text='Village')
        self.village_frame.grid(row=0, column= 0, padx= 2, pady= 2)

        # Create the frame for the statistics
        self.stats_frame = tk.LabelFrame(self.left_frame, text='Statistics')
        self.stats_frame.grid(row=1, column= 0, padx= 2, pady= 2)

        # Create the labels for the statistics
        self.food_stat_var = tk.StringVar()
        self.food_stat_var.set(f'Total Food: {config.food}')
        self.food_stat_label = tk.Label(self.stats_frame, textvariable=self.food_stat_var)
        self.food_stat_label.grid(row=1, column= 0, padx= 8, pady= 2, sticky= tk.NSEW)

        self.wood_stat_var = tk.StringVar()
        self.wood_stat_var.set(f'Total Wood: {config.wood}')
        self.wood_stat_label = tk.Label(self.stats_frame, textvariable=self.wood_stat_var)
        self.wood_stat_label.grid(row=1, column= 1, padx= 8, pady= 2, sticky= tk.NSEW)

        # Centeral Frame
        self.modifcation_frame = tk.Frame(self.center_frame)
        self.modifcation_frame.grid(row=0, column= 0, padx= 2, pady= 2)

        self.end_turn_button = tk.Button(self.center_frame, text= 'End Turn', width= 48)
        self.end_turn_button.grid(row=1, column= 0, padx= 2, pady= 4)

        # Right Frame

    def end_turn(self):
        # Run end of turn functions 

        # Update turn counter and add to the logs
        config.turn += 1
        config.log.append(f'\nTurn {config.turn}')
