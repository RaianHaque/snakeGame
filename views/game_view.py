import pygame

# WEEK 3: MVC View Architecture 
class GameView:
    def __init__(self, screen, hud_height=50):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()
        self.HUD_HEIGHT = hud_height
        self.CELL_SIZE = 25
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.pause_font = pygame.font.SysFont("Arial", 40, bold=True)
        
        # Colors
        self.COLOR_BG = (20, 20, 20)
        self.COLOR_FOOD = (220, 50, 50)
        self.COLOR_WALL_DARK = (60, 60, 60)
        self.COLOR_WALL_LIGHT = (100, 100, 100)
        self.COLOR_HUD_BG = (15, 15, 15)
        
        # Color Cycle for High Score
        self.COLOR_STAGES = [
            (50, 200, 50), (65, 105, 225), (147, 112, 219), (220, 20, 60),
            (255, 140, 0), (255, 215, 0), (0, 206, 209), (255, 20, 147),
            (139, 69, 19), (192, 192, 192)
        ]
        
        # Clickable Zones
        self.dev_score_rect = pygame.Rect(20, 10, 100, 30)
        self.menu_btn_rect = pygame.Rect(0, 0, 80, 30)
        
        # Menu Buttons (Pause)
        self.btn_resume = pygame.Rect(0, 0, 200, 50)
        self.btn_theme = pygame.Rect(0, 0, 200, 50)
        self.btn_mute = pygame.Rect(0, 0, 200, 50)
        self.btn_quit = pygame.Rect(0, 0, 200, 50)
        
        # Game Over Buttons
        self.btn_play_again = pygame.Rect(0, 0, 200, 50)
        self.btn_menu_gameover = pygame.Rect(0, 0, 200, 50)
        # Cache for scaled background images: keys are (theme, width, height)
        self._bg_cache = {}

    def resize(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()
        # Invalidate cached backgrounds when screen size changes
        self._bg_cache = {}

    #  DRAW BACKGROUND IMAGE 
    def draw_background(self, theme, assets):
        fill_color = self.COLOR_BG
        if theme == "Desert": fill_color = (194, 178, 128)
        elif theme == "Ocean": fill_color = (20, 40, 80)
        elif theme == "Jungle": fill_color = (34, 139, 34)
        
        self.screen.fill(fill_color)
        
        if theme in assets and assets[theme] is not None:
            key = (theme, self.WIDTH, self.HEIGHT)
            bg_img = self._bg_cache.get(key)
            if bg_img is None:
                try:
                    # Scale once per size/theme and cache for reuse
                    bg_img = pygame.transform.scale(assets[theme], (self.WIDTH, self.HEIGHT))
                    # Convert to display format for faster blits when possible
                    try:
                        bg_img = bg_img.convert_alpha() if bg_img.get_alpha() else bg_img.convert()
                    except Exception:
                        pass
                    self._bg_cache[key] = bg_img
                except Exception:
                    bg_img = None
            if bg_img:
                self.screen.blit(bg_img, (0, 0))
        
        # Draw HUD Bar on top
        pygame.draw.rect(self.screen, self.COLOR_HUD_BG, (0, 0, self.WIDTH, self.HUD_HEIGHT))
        pygame.draw.line(self.screen, (100, 100, 100), (0, self.HUD_HEIGHT), (self.WIDTH, self.HUD_HEIGHT), 2)

    def _get_draw_y(self, y_pixel):
        return y_pixel + self.HUD_HEIGHT

    def draw_border(self):
        cols = self.WIDTH // self.CELL_SIZE
        rows = (self.HEIGHT - self.HUD_HEIGHT) // self.CELL_SIZE + 1
        
        # FIX: ADJUSTED LOOPS FOR PERFECT FIT 
        # Top and Bottom walls
        for x in range(cols):
            self._draw_brick(x, 0)          
            self._draw_brick(x, rows - 1)   
        
        # Left and Right walls
        # "cols - 1" places the right wall exactly inside the visible screen area
        for y in range(1, rows - 1):
            self._draw_brick(0, y)          
            self._draw_brick(cols - 1, y)   

    def _draw_brick(self, grid_x, grid_y):
        rect = pygame.Rect(grid_x * self.CELL_SIZE, grid_y * self.CELL_SIZE + self.HUD_HEIGHT, self.CELL_SIZE, self.CELL_SIZE)
        pygame.draw.rect(self.screen, self.COLOR_WALL_DARK, rect)
        pygame.draw.rect(self.screen, self.COLOR_WALL_LIGHT, rect.inflate(-4, -4))
        pygame.draw.line(self.screen, (40, 40, 40), rect.bottomleft, rect.topright, 1)

    def get_rainbow_color(self, index):
        current_time = pygame.time.get_ticks()
        hue = (current_time // 5 + index * 10) % 360
        color = pygame.Color(0)
        color.hsla = (hue, 100, 50, 100)
        return color

    # WEEK 5: Advanced Rendering (Smooth Snake)
    def draw_snake(self, snake_obj, score):
        if not snake_obj.history: return
        
        if score >= 100: is_rainbow = True
        else:
            is_rainbow = False
            stage_index = min((score // 10), 9)
            base_color = self.COLOR_STAGES[stage_index]

        spacing = snake_obj.body_spacing
        points = list(enumerate(snake_obj.history[::spacing]))[::-1]

        for i, (x, y) in points:
            draw_pos = (int(x + self.CELL_SIZE/2), int(y + self.HUD_HEIGHT + self.CELL_SIZE/2))
            
            if is_rainbow: color = self.get_rainbow_color(i)
            else:
                if i == 0: color = base_color 
                else: color = (max(0, base_color[0]-30), max(0, base_color[1]-30), max(0, base_color[2]-30))
            
            # Radius 10 = 20px Diameter. Leaves 2.5px gap from grid edges.
            radius = 10 if i == 0 else 9 
            
            pygame.draw.circle(self.screen, color, draw_pos, radius)
            
            if i == 0: # Eyes
                dx, dy = snake_obj.direction
                eye_off_x = draw_pos[0] + dx * 8
                eye_off_y = draw_pos[1] + dy * 8
                
                if dx != 0: 
                    pygame.draw.circle(self.screen, (255,255,255), (eye_off_x, eye_off_y - 5), 3)
                    pygame.draw.circle(self.screen, (255,255,255), (eye_off_x, eye_off_y + 5), 3)
                    pygame.draw.circle(self.screen, (0,0,0), (eye_off_x+dx*2, eye_off_y - 5), 1)
                    pygame.draw.circle(self.screen, (0,0,0), (eye_off_x+dx*2, eye_off_y + 5), 1)
                else: 
                    pygame.draw.circle(self.screen, (255,255,255), (eye_off_x - 5, eye_off_y), 3)
                    pygame.draw.circle(self.screen, (255,255,255), (eye_off_x + 5, eye_off_y), 3)
                    pygame.draw.circle(self.screen, (0,0,0), (eye_off_x - 5, eye_off_y+dy*2), 1)
                    pygame.draw.circle(self.screen, (0,0,0), (eye_off_x + 5, eye_off_y+dy*2), 1)

    def draw_food(self, position):
        x, y = position
        center = (x * self.CELL_SIZE + self.CELL_SIZE//2, y * self.CELL_SIZE + self.HUD_HEIGHT + self.CELL_SIZE//2)
        radius = 8 
        pygame.draw.circle(self.screen, self.COLOR_FOOD, center, radius)
        pygame.draw.line(self.screen, (139, 69, 19), (center[0], center[1]-radius), (center[0], center[1]-radius-4), 2)

    def draw_obstacles(self, obstacles):
        for (x, y) in obstacles:
            self._draw_brick(x, y) 

    def draw_ui(self, score, fps, mode, is_dev, dev_typing_mode, temp_score_input):
        score_txt = f"Score: {score}"
        if dev_typing_mode: score_txt = f"Score: {temp_score_input}|"
        
        color = (255, 255, 0) if dev_typing_mode else (255, 255, 255)
        surf = self.font.render(score_txt, True, color)
        mid_y = self.HUD_HEIGHT // 2 - surf.get_height() // 2
        self.screen.blit(surf, (20, mid_y))
        
        self.dev_score_rect.topleft = (20, mid_y)
        self.dev_score_rect.size = surf.get_size()
        
        info = f"Mode: {mode}"
        self.screen.blit(self.font.render(info, True, (200, 200, 200)), (200, mid_y))

        self.menu_btn_rect.topright = (self.WIDTH - 20, 10)
        pygame.draw.rect(self.screen, (100, 100, 100), self.menu_btn_rect, border_radius=5)
        menu_txt = self.font.render("MENU", True, (255, 255, 255))
        self.screen.blit(menu_txt, (self.menu_btn_rect.centerx - menu_txt.get_width()//2, self.menu_btn_rect.centery - menu_txt.get_height()//2))

    # PAUSE MENU 
    def draw_pause_menu(self, is_muted, current_theme):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        cx, cy = self.WIDTH // 2, self.HEIGHT // 2
        # Taller panel for 4 buttons
        panel_rect = pygame.Rect(0, 0, 300, 390)
        panel_rect.center = (cx, cy)
        
        pygame.draw.rect(self.screen, (40, 40, 40), panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, (200, 200, 200), panel_rect, 2, border_radius=10)
        
        title = self.pause_font.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(title, (cx - title.get_width()//2, cy - 160))
        
        # Resume
        self.btn_resume.center = (cx, cy - 80)
        pygame.draw.rect(self.screen, (50, 160, 80), self.btn_resume, border_radius=5)
        res_txt = self.font.render("RESUME GAME", True, (255, 255, 255))
        self.screen.blit(res_txt, (self.btn_resume.centerx - res_txt.get_width()//2, self.btn_resume.centery - res_txt.get_height()//2))
        
        # Change Theme
        self.btn_theme.center = (cx, cy - 10)
        pygame.draw.rect(self.screen, (100, 100, 200), self.btn_theme, border_radius=5)
        theme_txt = self.font.render(f"THEME: {current_theme.upper()}", True, (255, 255, 255))
        self.screen.blit(theme_txt, (self.btn_theme.centerx - theme_txt.get_width()//2, self.btn_theme.centery - theme_txt.get_height()//2))

        # Mute
        self.btn_mute.center = (cx, cy + 60)
        color = (200, 200, 0) if is_muted else (100, 100, 100)
        text = "UNMUTE AUDIO" if is_muted else "MUTE AUDIO"
        pygame.draw.rect(self.screen, color, self.btn_mute, border_radius=5)
        mute_txt = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(mute_txt, (self.btn_mute.centerx - mute_txt.get_width()//2, self.btn_mute.centery - mute_txt.get_height()//2))

        # Quit
        self.btn_quit.center = (cx, cy + 130)
        pygame.draw.rect(self.screen, (200, 60, 60), self.btn_quit, border_radius=5)
        quit_txt = self.font.render("MAIN MENU", True, (255, 255, 255))
        self.screen.blit(quit_txt, (self.btn_quit.centerx - quit_txt.get_width()//2, self.btn_quit.centery - quit_txt.get_height()//2))

    # GAME OVER MENU 
    def draw_game_over(self, score):
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        cx, cy = self.WIDTH // 2, self.HEIGHT // 2
        
        txt = self.pause_font.render("GAME OVER", True, (255, 50, 50))
        self.screen.blit(txt, (cx - txt.get_width()//2, cy - 100))
        
        score_txt = self.font.render(f"Final Score: {score}", True, (255, 255, 255))
        self.screen.blit(score_txt, (cx - score_txt.get_width()//2, cy - 50))
        
        # Play Again
        self.btn_play_again.center = (cx, cy + 20)
        pygame.draw.rect(self.screen, (50, 200, 50), self.btn_play_again, border_radius=5)
        play_txt = self.font.render("PLAY AGAIN (R)", True, (20, 20, 20))
        self.screen.blit(play_txt, (self.btn_play_again.centerx - play_txt.get_width()//2, self.btn_play_again.centery - play_txt.get_height()//2))
        
        # Main Menu
        self.btn_menu_gameover.center = (cx, cy + 90)
        pygame.draw.rect(self.screen, (200, 200, 200), self.btn_menu_gameover, border_radius=5)
        menu_txt = self.font.render("MAIN MENU (M)", True, (20, 20, 20))
        self.screen.blit(menu_txt, (self.btn_menu_gameover.centerx - menu_txt.get_width()//2, self.btn_menu_gameover.centery - menu_txt.get_height()//2))