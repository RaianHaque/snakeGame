# models/food.py - The Model: Handles the Food's Data Logic

import random

class Food:
    """
    Represents the food item's state and logic for placement.
    """
    def __init__(self, screen_width, screen_height, cell_size):
        self.cell_size = cell_size
        
        # Calculate max grid coordinates
        self.max_x = screen_width // cell_size - 1
        self.max_y = screen_height // cell_size - 1
        
        # Initial placement
        self.position = self.random_position()

    def random_position(self, occupied_positions=[]):
        """
        Generates a new random (x, y) grid position that is NOT 
        in the list of occupied_positions (e.g., the snake's body).
        """
        while True:
            # Generate random grid coordinates
            x = random.randint(0, self.max_x)
            y = random.randint(0, self.max_y)
            new_pos = (x, y)
            
            # Check if the new position is clear
            if new_pos not in occupied_positions:
                return new_pos

    def respawn(self, occupied_positions):
        """
        Sets the food to a new random position after being eaten.
        """
        self.position = self.random_position(occupied_positions)
        
    def get_position(self):
        """
        Returns the (x, y) grid coordinates of the food.
        """
        return self.position