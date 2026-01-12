import pygame
import sys
import math
import os 

# VIDEO SUPPORT 
try:
    import cv2
except ImportError:
    cv2 = None
    print("Video Library (OpenCV) not found. Falling back to static images.")

# WEEK 4: Auth & DB 
try:
    from controllers.auth_controller import AuthController
    from views.menu_view import MenuView
except ImportError:
    pass 

# WEEK 3: Models & View
try:
    from models.snake import Snake
    from models.food import Food
    from views.game_view import GameView
except ImportError:
    from snake import Snake
    from food import Food

# WEEK 1: Main Loop Setup 
def main():
    pygame.init()
    pygame.mixer.init()
    
    # WEEK 5: Audio & Polish 
    try:
        def resource_path(relative_path):
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            try:
                base = sys._MEIPASS
            except AttributeError:
                base = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(base, relative_path)

        eat_sound = pygame.mixer.Sound(resource_path(os.path.join("sounds", "eat.wav")))
        death_sound = pygame.mixer.Sound(resource_path(os.path.join("sounds", "death.wav")))
        click_sound = pygame.mixer.Sound(resource_path(os.path.join("sounds", "click.wav")))
        pygame.mixer.music.load(resource_path(os.path.join("sounds", "music.mp3")))
    except Exception:
        eat_sound = death_sound = click_sound = None

    # Load Assets (Robust Pathing)
    bg_assets = {}
    
    # Helper to load images safely (works with PyInstaller --onefile)
    def load_img(name):
        try:
            img_path = resource_path(os.path.join("assets", name))
        except NameError:
            img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", name)
        if os.path.exists(img_path):
            return pygame.image.load(img_path)
        return None

    bg_assets["Desert"] = load_img("dessart.png")
    bg_assets["Ocean"] = load_img("ocean.png")
    bg_assets["Jungle"] = load_img("jungle.png")

    # FIX: VIDEO LOADING
    video_cap = None
    fallback_bg = bg_assets.get("Jungle") # Default to jungle if video fails
    
    if cv2:
        try:
            video_path = resource_path(os.path.join("assets", "menu_bg.mp4"))
        except NameError:
            video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "menu_bg.mp4")
        if os.path.exists(video_path):
            video_cap = cv2.VideoCapture(video_path)
        else:
            print("Video file 'menu_bg.mp4' not found in assets.")

    WIDTH, HEIGHT = 1280, 720
    HUD_HEIGHT = 50 
    CELL_SIZE = 25
    
    GRID_W = WIDTH // CELL_SIZE
    GRID_H = (HEIGHT - HUD_HEIGHT) // CELL_SIZE + 1
    
    BASE_FPS = 60

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Snake Game") 
    clock = pygame.time.Clock()
    
    # WEEK 3: MVC Init
    try:
        auth = AuthController()
        menu = MenuView(screen)
    except:
        auth = None
        menu = None 
    
    app_state = "LOGIN"
    if not auth: app_state = "GAME" 
    
    inputs = {
        "Identifier": "", "Username": "", "Password": "", 
        "First Name": "", "Last Name": "", "Email": "", 
        "Phone": "", "Confirm Pass": ""
    }
    active_field = ""
    message = ""
    
    dev_pass = ""
    dev_mode_active = False
    dev_typing_score = False
    temp_score_input = ""
    
    is_muted = False
    
    current_mode = "Classic" 
    current_theme = "Classic" 
    available_themes = ["Classic", "Desert", "Jungle", "Ocean"]
    
    obstacles = []

    snake = None
    food = None
    view = None
    score = 0
    current_fps = BASE_FPS

    def calculate_fps(current_score):
        new_fps = BASE_FPS
        if current_score <= 100:
            increase = current_score // 10
            new_fps += increase
        else:
            base_increase = 10
            remaining = current_score - 100
            extra_increase = remaining // 25
            new_fps += base_increase + extra_increase
        return new_fps

    def generate_obstacles():
        obs = []
        cx, cy = GRID_W // 2, GRID_H // 2
        for i in range(2, 7): obs.append((i, 2)); obs.append((2, i)) 
        for i in range(2, 7): obs.append((GRID_W - i - 1, 2)); obs.append((GRID_W - 3, i)) 
        for i in range(2, 7): obs.append((i, GRID_H - 3)); obs.append((2, GRID_H - i - 1)) 
        for i in range(2, 7): obs.append((GRID_W - i - 1, GRID_H - 3)); obs.append((GRID_W - 3, GRID_H - i - 1)) 
        for i in range(-4, 5): obs.append((cx + i, cy))
        return obs

    # VIDEO / IMAGE HELPER
    def get_background_surface(cap, static_img, target_w, target_h):
        # Priority 1: Video (Only if working)
        if cap and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = cap.read()
            
            if ret:
                frame = cv2.resize(frame, (target_w, target_h))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
        
        # Priority 2: Static Image
        if static_img:
            return pygame.transform.scale(static_img, (target_w, target_h))
            
        return None

    # WEEK 1: Main Loop
    while True:
        # Get Background (Video or Image)
        bg_surf = None
        if app_state in ["LOGIN", "SIGNUP", "MODE_SELECT", "DEV_AUTH"]:
            bg_surf = get_background_surface(video_cap, fallback_bg, WIDTH, HEIGHT)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            
            elif event.type == pygame.VIDEORESIZE:
                if event.w < 400 or event.h < 300: continue 

                WIDTH, HEIGHT = event.w, event.h
                GRID_W = WIDTH // CELL_SIZE
                GRID_H = (HEIGHT - HUD_HEIGHT) // CELL_SIZE + 1
                
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                
                if menu: menu.update_layout(screen)
                if view: view.resize(screen)
                if snake: snake.update_grid_dimensions(GRID_W, GRID_H)
                if food: food.update_grid_dimensions(WIDTH, HEIGHT - HUD_HEIGHT)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    is_full = screen.get_flags() & pygame.FULLSCREEN
                    if is_full: screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
                    else: screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    w, h = screen.get_size()
                    if w > 300 and h > 300: pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, {'w': w, 'h': h}))

        # STATE: LOGIN 
        if app_state == "LOGIN" and menu:
            try: leaderboard = auth.db.get_leaderboard()
            except: leaderboard = []
            menu.draw_login(inputs, active_field, message, leaderboard, dev_mode_active, bg_surface=bg_surf)
            pygame.display.flip(); clock.tick(60)

            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    cx = WIDTH // 2 + 100 
                    if pygame.Rect(cx - 150, 220, 300, 40).collidepoint(pos): active_field = "Identifier"
                    elif pygame.Rect(cx - 150, 290, 300, 40).collidepoint(pos): active_field = "Password"
                    elif menu.buttons.get("login_submit") and menu.buttons["login_submit"].collidepoint(pos):
                        user = auth.db.validate_login(inputs["Identifier"], inputs["Password"])
                        if user: auth.current_user = user[0]; app_state = "MODE_SELECT"; click_sound.play() if click_sound and not is_muted else None
                        else: message = "Invalid Credentials"
                    elif menu.buttons.get("goto_signup") and menu.buttons["goto_signup"].collidepoint(pos):
                        app_state = "SIGNUP"; message = ""; active_field = ""; inputs["Password"] = ""; inputs["Confirm Pass"] = ""
                    elif menu.buttons.get("guest") and menu.buttons["guest"].collidepoint(pos):
                        auth.current_user = "Guest"; app_state = "MODE_SELECT" 
                    elif menu.dev_trigger_rect.collidepoint(pos):
                        if not dev_mode_active: app_state = "DEV_AUTH"; dev_pass = ""
                        else: dev_mode_active = False; message = "DEV MODE OFF"
                    else: active_field = ""
                if event.type == pygame.KEYDOWN:
                    if active_field:
                        if event.key == pygame.K_BACKSPACE: inputs[active_field] = inputs[active_field][:-1]
                        else: inputs[active_field] += event.unicode

        # STATE: SIGNUP
        elif app_state == "SIGNUP" and menu:
            menu.draw_signup(inputs, active_field, message, bg_surface=bg_surf)
            pygame.display.flip(); clock.tick(60)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    cx = WIDTH // 2
                    if pygame.Rect(cx - 310, 150, 300, 40).collidepoint(pos): active_field = "Username"
                    elif pygame.Rect(cx - 310, 240, 300, 40).collidepoint(pos): active_field = "First Name"
                    elif pygame.Rect(cx - 310, 420, 300, 40).collidepoint(pos): active_field = "Password"
                    elif pygame.Rect(cx + 10, 150, 300, 40).collidepoint(pos): active_field = "Email"
                    elif pygame.Rect(cx + 10, 240, 300, 40).collidepoint(pos): active_field = "Last Name"
                    elif pygame.Rect(cx + 10, 420, 300, 40).collidepoint(pos): active_field = "Confirm Pass"
                    elif pygame.Rect(cx - 150, 330, 300, 40).collidepoint(pos): active_field = "Phone"
                    elif menu.buttons.get("signup_submit") and menu.buttons["signup_submit"].collidepoint(pos):
                        if inputs["Password"] != inputs["Confirm Pass"]: message = "Passwords do not match!"
                        elif not inputs["Username"] or not inputs["Email"]: message = "Username & Email required!"
                        else:
                            res = auth.db.register_user(inputs["Username"], inputs["Password"], inputs["First Name"], inputs["Last Name"], inputs["Email"], inputs["Phone"])
                            message = res
                            if res == "Success": app_state = "LOGIN"; message = "Account Created! Login now."; inputs["Password"] = ""; inputs["Confirm Pass"] = ""
                    elif menu.buttons.get("back_login") and menu.buttons["back_login"].collidepoint(pos): app_state = "LOGIN"
                    else: active_field = ""
                if event.type == pygame.KEYDOWN:
                    if active_field:
                        if event.key == pygame.K_BACKSPACE: inputs[active_field] = inputs[active_field][:-1]
                        else: inputs[active_field] += event.unicode

        # STATE: MODE SELECT 
        elif app_state == "MODE_SELECT" and menu:
            menu.draw_mode_select(current_theme, bg_surface=bg_surf) 
            pygame.display.flip(); clock.tick(60)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if menu.buttons.get("mode_classic") and menu.buttons["mode_classic"].collidepoint(pos):
                        current_mode = "Classic"; app_state = "GAME"; snake = None
                        if pygame.mixer.music.get_busy() == False and not is_muted: pygame.mixer.music.play(-1)
                    elif menu.buttons.get("mode_box") and menu.buttons["mode_box"].collidepoint(pos):
                        current_mode = "Box"; app_state = "GAME"; snake = None
                        if pygame.mixer.music.get_busy() == False and not is_muted: pygame.mixer.music.play(-1)
                    elif menu.buttons.get("mode_obstacles") and menu.buttons["mode_obstacles"].collidepoint(pos):
                        current_mode = "Obstacles"; app_state = "GAME"; snake = None
                        if pygame.mixer.music.get_busy() == False and not is_muted: pygame.mixer.music.play(-1)
                    elif menu.buttons.get("theme_toggle") and menu.buttons["theme_toggle"].collidepoint(pos):
                        try:
                            idx = available_themes.index(current_theme)
                            next_idx = (idx + 1) % len(available_themes)
                            current_theme = available_themes[next_idx]
                        except: current_theme = "Classic"
                    elif menu.buttons.get("mode_back") and menu.buttons["mode_back"].collidepoint(pos): app_state = "LOGIN"

        # STATE: GAME
        elif app_state == "GAME":
            if snake is None:
                snake = Snake(GRID_W, GRID_H, CELL_SIZE)
                food = Food(WIDTH, HEIGHT - HUD_HEIGHT, CELL_SIZE)
                try: view = GameView(screen, HUD_HEIGHT)
                except: print("GameView missing")
                score = 0
                current_fps = BASE_FPS 
                obstacles = generate_obstacles() if current_mode == "Obstacles" else []
                dev_typing_score = False

            for event in events:
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if view and view.menu_btn_rect.collidepoint(pos): app_state = "PAUSED"
                    elif dev_mode_active and view and view.dev_score_rect.collidepoint(pos):
                        dev_typing_score = True; temp_score_input = str(score)
                    else: dev_typing_score = False
                if event.type == pygame.KEYDOWN:
                    if dev_typing_score:
                        if event.key == pygame.K_RETURN:
                            if temp_score_input.isdigit(): score = int(temp_score_input)
                            dev_typing_score = False
                        elif event.key == pygame.K_BACKSPACE: temp_score_input = temp_score_input[:-1]
                        else:
                            if event.unicode.isdigit(): temp_score_input += event.unicode
                    else:
                        if event.key == pygame.K_UP: snake.change_direction(snake.UP)
                        elif event.key == pygame.K_DOWN: snake.change_direction(snake.DOWN)
                        elif event.key == pygame.K_LEFT: snake.change_direction(snake.LEFT)
                        elif event.key == pygame.K_RIGHT: snake.change_direction(snake.RIGHT)
                        elif event.key == pygame.K_ESCAPE: app_state = "PAUSED"

            if snake and not dev_typing_score:
                snake.move(current_mode)
                current_fps = calculate_fps(score)
                
                hit_wall = (current_mode == "Box" and snake.check_wall_collision())
                hit_self = snake.check_self_collision()
                hit_obs = snake.check_obstacle_collision(obstacles)
                
                if hit_wall or hit_self or hit_obs:
                    if death_sound and not is_muted: death_sound.play()
                    # FIX: SAFE DATABASE UPDATE
                    try:
                        if auth and auth.current_user != "Guest": 
                            auth.db.update_score(auth.current_user, score)
                    except Exception as e:
                        print(f"Score update failed: {e}")
                    
                    app_state = "GAME_OVER"
                    # FIX: DO NOT DELETE SNAKE YET
                
                else:
                    food_grid_pos = food.get_position()
                    food_px_x = food_grid_pos[0] * CELL_SIZE
                    food_px_y = food_grid_pos[1] * CELL_SIZE
                    
                    food_rect = pygame.Rect(food_px_x + 4, food_px_y + 4, 16, 16)
                    head_rect = pygame.Rect(snake.head_pos[0] + 4, snake.head_pos[1] + 4, 16, 16)

                    if head_rect.colliderect(food_rect):
                        if eat_sound and not is_muted: eat_sound.play()
                        snake.grow()
                        occupied = obstacles + snake.get_occupied_grids()
                        food.respawn(occupied)
                        score += 1

                if snake is not None and view:
                    view.draw_background(current_theme, bg_assets)
                    if current_mode == "Box": view.draw_border()
                    view.draw_obstacles(obstacles)
                    view.draw_food(food.get_position())
                    view.draw_snake(snake, score)
                    view.draw_ui(score, current_fps, current_mode, dev_mode_active, dev_typing_score, temp_score_input)
                    pygame.display.flip()
                    clock.tick(current_fps)
            
            elif dev_typing_score and snake is not None and view:
                 view.draw_background(current_theme, bg_assets)
                 if current_mode == "Box": view.draw_border()
                 view.draw_obstacles(obstacles)
                 view.draw_food(food.get_position())
                 view.draw_snake(snake, score)
                 view.draw_ui(score, current_fps, current_mode, dev_mode_active, dev_typing_score, temp_score_input)
                 pygame.display.flip()

        # STATE: PAUSED 
        elif app_state == "PAUSED" and view:
            view.draw_pause_menu(is_muted, current_theme)
            pygame.display.flip(); clock.tick(60)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: app_state = "GAME"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if view.btn_resume.collidepoint(pos): app_state = "GAME"
                    elif view.btn_theme.collidepoint(pos):
                        try:
                            idx = available_themes.index(current_theme)
                            next_idx = (idx + 1) % len(available_themes)
                            current_theme = available_themes[next_idx]
                        except: current_theme = "Classic"
                    elif view.btn_mute.collidepoint(pos):
                        is_muted = not is_muted
                        if is_muted: pygame.mixer.music.pause()
                        else: pygame.mixer.music.unpause()
                    elif view.btn_quit.collidepoint(pos): app_state = "MODE_SELECT"

        # STATE: GAME OVER 
        elif app_state == "GAME_OVER" and view:
            # FIX: DRAW GAME WORLD UNDER THE MENU 
            view.draw_background(current_theme, bg_assets)
            if current_mode == "Box": view.draw_border()
            view.draw_obstacles(obstacles)
            view.draw_food(food.get_position())
            if snake: view.draw_snake(snake, score) # Draw dead snake
            
            view.draw_game_over(score) # Draw menu on top
            
            pygame.display.flip(); clock.tick(60)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: app_state = "GAME"; snake = None # Reset now
                    if event.key == pygame.K_m: app_state = "MODE_SELECT"; snake = None
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if view.btn_play_again.collidepoint(pos):
                        app_state = "GAME"; snake = None
                    elif view.btn_menu_gameover.collidepoint(pos):
                        app_state = "MODE_SELECT"; snake = None
        
        # STATE: DEV AUTH 
        elif app_state == "DEV_AUTH" and menu:
            menu.draw_login(inputs, active_field, message, [], dev_mode_active, bg_surface=bg_surf)
            menu.draw_dev_auth(dev_pass, bg_surface=bg_surf)
            pygame.display.flip(); clock.tick(60)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: app_state = "LOGIN"
                    elif event.key == pygame.K_RETURN: 
                        if dev_pass == "1234": dev_mode_active = True; app_state = "LOGIN"; message = "DEV MODE ON"
                        else: app_state = "LOGIN"; message = "ACCESS DENIED"
                    elif event.key == pygame.K_BACKSPACE: dev_pass = dev_pass[:-1]
                    else: dev_pass += event.unicode

if __name__ == "__main__":
    main()