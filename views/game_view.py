# views/game_view.py - The View: Handles Data Presentation & Graphics

import pygame

class GameView:
    def __init__(self, screen, cell_size=25): 
        self.screen = screen
        self.cell_size = cell_size
        
        # High-Quality Color Palette
        self.background_color = (30, 30, 40)    
        self.grid_color = (45, 45, 55)          
        self.snake_color = (100, 200, 100)      
        self.snake_head_color = (150, 255, 150) 
        self.food_color = (255, 60, 60)         

        self.width = screen.get_width()
        self.height = screen.get_height()
        
    def draw_background(self):
        self.screen.fill(self.background_color)
        
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.width, y))

    def draw_snake(self, snake_body_coords):
        for i, (x, y) in enumerate(snake_body_coords):
            rect_x = x * self.cell_size
            rect_y = y * self.cell_size
            
            snake_rect = pygame.Rect(rect_x, rect_y, self.cell_size, self.cell_size)
            
            color = self.snake_head_color if i == 0 else self.snake_color
            
            pygame.draw.rect(self.screen, color, snake_rect)
            
            highlight_color = (200, 200, 200) if i == 0 else (50, 50, 50)
            pygame.draw.rect(self.screen, highlight_color, snake_rect, 1)

    def draw_food(self, food_coord):
        x, y = food_coord
        
        rect_x = x * self.cell_size
        rect_y = y * self.cell_size
        
        center_x = rect_x + self.cell_size // 2
        center_y = rect_y + self.cell_size // 2
        radius = self.cell_size // 2 - 2 
        
        pygame.draw.circle(self.screen, self.food_color, (center_x, center_y), radius)
        
        pygame.draw.circle(self.screen, (255, 255, 255), (center_x - radius // 3, center_y - radius // 3), 2)