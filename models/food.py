# models/food.py - The Model: Handles the Food's Data Logic

import random

class Food:
    def __init__(self, screen_width, screen_height, cell_size):
        self.cell_size = cell_size
        
        # Calculate max grid coordinates
        self.max_x = screen_width // cell_size - 1
        self.max_y = screen_height // cell_size - 1
        
        self.position = self.random_position()

    def random_position(self, occupied_positions=[]):
        while True:
            x = random.randint(0, self.max_x)
            y = random.randint(0, self.max_y)
            new_pos = (x, y)
            
            if new_pos not in occupied_positions:
                return new_pos

    def respawn(self, occupied_positions):
        self.position = self.random_position(occupied_positions)
        
    def get_position(self):
        return self.position