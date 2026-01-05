import pygame

class GameView:
    def __init__(self, screen):
        # WEEK 1: Basic Init
        self.screen = screen
        self.cell_size = 25
        
        # WEEK 4: Color Cycle Palette
        self.colors = [
            (46, 204, 113),  # Green (0-4)
            (241, 196, 15),  # Yellow (5-9)
            (52, 152, 219),  # Light Blue (10-14)
            (231, 76, 60),   # Red (15-19)
            (155, 89, 182)   # Purple (20-24)
        ]

    def draw_background(self):
        # WEEK 2: Dark Forest Theme
        self.screen.fill((10, 20, 10))

    def draw_snake(self, snake_body, score):
        # WEEK 4: Color cycling logic based on score
        color_index = (score // 5) % len(self.colors)
        current_color = self.colors[color_index]
        
        for i, segment in enumerate(snake_body):
            rect = pygame.Rect(segment[0] * self.cell_size, segment[1] * self.cell_size, 
                               self.cell_size, self.cell_size)
            
            # Head is always white; body cycles based on score
            if i == 0:
                pygame.draw.rect(self.screen, (255, 255, 255), rect)
            else:
                pygame.draw.rect(self.screen, current_color, rect)
            
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

    def draw_food(self, food_pos):
        # WEEK 1: Basic Food Drawing
        rect = pygame.Rect(food_pos[0] * self.cell_size, food_pos[1] * self.cell_size, 
                           self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, (255, 0, 0), rect)