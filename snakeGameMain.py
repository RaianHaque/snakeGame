# snakeGameMain.py - The Controller: Handles Request Flow & Game Loop

import pygame
import sys
# Import Models and View
from models.snake import Snake
from models.food import Food 
from views.game_view import GameView 

# --- CONFIGURATION ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_TITLE = "Feature-Rich Snake App"
GRID_CELL_SIZE = 25 
FPS = 7 # Base speed for the Dynamic Difficulty

def main():
    # 1. Initialization
    pygame.init()
    
    # Setup Screen and Clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    
    # 2. Instantiate Model and View
    SNAKE_GRID_START = (SCREEN_WIDTH // GRID_CELL_SIZE // 2, SCREEN_HEIGHT // GRID_CELL_SIZE // 2)
    snake_model = Snake(start_pos=SNAKE_GRID_START, cell_size=GRID_CELL_SIZE) 
    food_model = Food(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_CELL_SIZE)
    game_view = GameView(screen, cell_size=GRID_CELL_SIZE) 
    
    running = True
    while running:
        # --- 1. Event Handling (Input) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                # Map keyboard input to the Model's change_direction method
                if event.key == pygame.K_UP:
                    snake_model.change_direction(snake_model.UP)
                elif event.key == pygame.K_DOWN:
                    snake_model.change_direction(snake_model.DOWN)
                elif event.key == pygame.K_LEFT:
                    snake_model.change_direction(snake_model.LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake_model.change_direction(snake_model.RIGHT)
                    
        # --- 2. Model Update (Data Logic) ---
        snake_model.move() 
        
        # Check for Food Collision
        if snake_model.get_head_position() == food_model.get_position():
            snake_model.grow()
            food_model.respawn(snake_model.body)
        
        if snake_model.check_self_collision():
            print("Game Over! Self collision.")
            running = False
            
        head_x, head_y = snake_model.get_head_position()
        max_grid_x = SCREEN_WIDTH // GRID_CELL_SIZE
        max_grid_y = SCREEN_HEIGHT // GRID_CELL_SIZE
        
        if head_x < 0 or head_x >= max_grid_x or head_y < 0 or head_y >= max_grid_y:
            print("Game Over! Boundary collision.")
            running = False
            
        # --- 3. View Draw (Presentation) ---
        game_view.draw_background()
        game_view.draw_snake(snake_model.body)
        game_view.draw_food(food_model.get_position())
        
        # Update the entire screen
        pygame.display.flip()
        
        # Control the speed/FPS
        # (FPS will be made dynamic later)
        clock.tick(FPS) 

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()