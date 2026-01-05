import pygame
import sys
from controllers.auth_controller import AuthController
from views.menu_view import MenuView
from models.snake import Snake
from models.food import Food
from views.game_view import GameView

def main():
    pygame.init()
    pygame.mixer.init() # WEEK 3: Audio
    
    try:
        eat_sound = pygame.mixer.Sound("sounds/eat.wav")
        death_sound = pygame.mixer.Sound("sounds/death.wav")
        click_sound = pygame.mixer.Sound("sounds/click.wav")
        pygame.mixer.music.load("sounds/music.mp3") 
    except:
        eat_sound = death_sound = click_sound = None

    WIDTH, HEIGHT = 1280, 725 
    CELL_SIZE = 25
    GRID_W, GRID_H = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
    FPS = 6 

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game - Week 4 Final")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28, bold=True)
    
    auth = AuthController()
    menu = MenuView(screen)
    
    user_input, pass_input = "", ""
    active_field, message = "Username", "Login to Start"
    is_authenticated, game_active, show_game_over, is_muted, music_started = False, False, False, False, False
    current_best = 0

    while True: 
        # LOGIN / LEADERBOARD
        while not is_authenticated:
            leaderboard = auth.db.get_leaderboard() 
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if menu.buttons["login"].collidepoint(pos):
                        user_data = auth.db.validate_login(user_input, pass_input)
                        if user_data:
                            auth.current_user, current_best = user_input, user_data[2]
                            is_authenticated, game_active = True, True
                            if click_sound: click_sound.play()
                        else: message = "Login Failed!"
                    elif menu.buttons["signup"].collidepoint(pos):
                        message = auth.sign_up(user_input, pass_input)
                        if click_sound: click_sound.play()
                    elif menu.buttons["guest"].collidepoint(pos):
                        auth.current_user, is_authenticated, game_active, current_best = "Guest", True, True, 0
                        if click_sound: click_sound.play()

                    if pygame.Rect(WIDTH//2-200, HEIGHT*0.3, 400, 50).collidepoint(pos): active_field = "Username"
                    elif pygame.Rect(WIDTH//2-200, HEIGHT*0.3+90, 400, 50).collidepoint(pos): active_field = "Password"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if active_field == "Username": user_input = user_input[:-1]
                        else: pass_input = pass_input[:-1]
                    elif event.key == pygame.K_RETURN: active_field = "Password" if active_field == "Username" else "Username"
                    else:
                        if event.unicode.isprintable():
                            if active_field == "Username": user_input += event.unicode
                            else: pass_input += event.unicode

            menu.draw_menu(message, user_input, pass_input, active_field, leaderboard)
            pygame.display.flip()

        snake = Snake(max_x=GRID_W, max_y=GRID_H) 
        food, view, score, has_died = Food(WIDTH, HEIGHT, CELL_SIZE), GameView(screen), 0, False
        if not is_muted and not music_started:
            pygame.mixer.music.play(-1); music_started = True

        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: snake.change_direction(snake.UP)
                    elif event.key == pygame.K_DOWN: snake.change_direction(snake.DOWN)
                    elif event.key == pygame.K_LEFT: snake.change_direction(snake.LEFT)
                    elif event.key == pygame.K_RIGHT: snake.change_direction(snake.RIGHT)

            snake.move()
            if snake.get_head_position() == food.get_position():
                if eat_sound: eat_sound.play()
                snake.grow(); food.respawn(snake.body); score += 1 

            # COLLISION LOGIC
            if snake.check_self_collision() and not has_died:
                has_died = True; pygame.mixer.music.stop(); music_started = False
                if death_sound: death_sound.play()
                if auth.current_user != "Guest": auth.db.update_score(auth.current_user, score)
                game_active, show_game_over = False, True; break

            view.draw_background()
            view.draw_snake(snake.body, score) # Pass score for color cycle
            view.draw_food(food.get_position())
            hud = font.render(f"Score: {score}  Record: {current_best}", True, (255,255,255))
            screen.blit(hud, (30, 30)); pygame.display.flip(); clock.tick(FPS)

        while show_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if menu.game_over_buttons["restart"].collidepoint(pos):
                        if click_sound: click_sound.play(); show_game_over, game_active = False, True
                    elif menu.game_over_buttons["menu"].collidepoint(pos):
                        if click_sound: click_sound.play(); show_game_over, is_authenticated = False, False
                    elif menu.game_over_buttons["mute"].collidepoint(pos):
                        is_muted = not is_muted; pygame.mixer.music.stop() if is_muted else None; click_sound.play() if click_sound else None

            menu.draw_game_over(score, current_best, is_muted)
            pygame.display.flip()

if __name__ == "__main__":
    main()