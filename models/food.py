import pygame
import random

class Food:
    def __init__(self, screen_width, screen_height, cell_size):
        self.sw = screen_width
        self.sh = screen_height
        self.cs = cell_size
        self.position = [0, 0] # Grid coordinates! [GridX, GridY]
        self.respawn([]) # Spawn immediately

    # Keeps the food logic updated if the window resizes
    def update_grid_dimensions(self, new_width, new_height):
        self.sw = new_width
        self.sh = new_height

    def respawn(self, occupied_grids):
        # Calculate grid limits
        # Example: Width 800 / 25 = 32 columns. Indices 0 to 31.
        max_x = (self.sw // self.cs) - 1
        max_y = (self.sh // self.cs) - 1
        
        # Safety check for tiny screens
        if max_x < 2: max_x = 2
        if max_y < 2: max_y = 2
        
        while True:
            # FIX: ADDED PADDING TO PREVENT WALL SPAWNS
            # Old: random.randint(0, max_x) -> allowed spawning on 0 (Left Wall) and max (Right Wall)
            # New: random.randint(1, max_x - 1) -> forces spawn strictly INSIDE the borders
            new_x = random.randint(1, max_x - 1)
            new_y = random.randint(1, max_y - 1)
            
            # Ensure food doesn't spawn inside snake or manual obstacles
            if (new_x, new_y) not in occupied_grids:
                self.position = [new_x, new_y]
                break

    def get_position(self):
        # Returns GRID coordinates
        return self.position

    def draw(self, surface):
        # Convert Grid -> Pixel for drawing
        pixel_x = self.position[0] * self.cs
        pixel_y = self.position[1] * self.cs
        
        rect = pygame.Rect(pixel_x, pixel_y, self.cs, self.cs)
        pygame.draw.circle(surface, (220, 50, 50), rect.center, self.cs // 2 - 2)