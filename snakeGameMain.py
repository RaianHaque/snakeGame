import pygame
import sys
from models.snake import Snake
from models.food import Food 
from views.game_view import GameView 

# --- CONFIGURATION ---
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 800
GAME_TITLE = "Snake Game"
GRID_CELL_SIZE = 25 
FPS = 7

def main():
    # 1. Initialization
    pygame.init()
    
    # Setup Screen and Clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    
    # Calculate grid dimensions 
    MAX_GRID_X = SCREEN_WIDTH // GRID_CELL_SIZE
    MAX_GRID_Y = SCREEN_HEIGHT // GRID_CELL_SIZE
    
    # 2. Instantiate Model and View
    SNAKE_GRID_START = (MAX_GRID_X // 2, MAX_GRID_Y // 2)
    
    # Pass grid dimensions to the Snake Model for wrap-around logic
    snake_model = Snake(
        start_pos=SNAKE_GRID_START, 
        cell_size=GRID_CELL_SIZE,
        max_x=MAX_GRID_X, # Max number of cells horizontally
        max_y=MAX_GRID_Y  # Max number of cells vertically
    ) 
    
    food_model = Food(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_CELL_SIZE)
    game_view = GameView(screen, cell_size=GRID_CELL_SIZE) 
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
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
        
        # Check for GAME OVER.
        if snake_model.check_self_collision():
            print("GAME OVER! Self-collision.")
            running = False
            
        #3. View Draw (Presentation) 
        game_view.draw_background()
        game_view.draw_snake(snake_model.body)
        game_view.draw_food(food_model.get_position())
        
        pygame.display.flip()
        clock.tick(FPS) 

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()