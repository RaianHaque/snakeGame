import pygame

# WEEK 3: MVC View Architecture 
class MenuView:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()
        self.font = pygame.font.SysFont("Arial", 22)
        self.title_font = pygame.font.SysFont("Arial", 40, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 16)
        
        self.BG_COLOR = (30, 30, 30)
        self.INPUT_BG = (50, 50, 50)
        self.ACTIVE_BORDER = (100, 149, 237)
        self.PASSIVE_BORDER = (100, 100, 100)
        self.BTN_GREEN = (50, 160, 80)
        self.BTN_RED = (200, 60, 60)
        self.TEXT_WHITE = (255, 255, 255)
        self.GOLD = (255, 215, 0)
        self.PANEL_BG = (40, 40, 40)
        
        self.buttons = {}
        self.dev_trigger_rect = pygame.Rect(self.WIDTH - 80, 20, 60, 30)

    # WEEK 5: Auto-Resize
    def update_layout(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = screen.get_size()
        self.dev_trigger_rect = pygame.Rect(self.WIDTH - 80, 20, 60, 30)

    # Helper to draw background (Video or Solid Color)
    def _draw_background(self, bg_surface):
        if bg_surface:
            # Draw video frame
            self.screen.blit(bg_surface, (0, 0))
            # Optional: Add a dark overlay so text remains readable
            overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100)) # 100 = Transparency level (0-255)
            self.screen.blit(overlay, (0,0))
        else:
            # Fallback to solid color
            self.screen.fill(self.BG_COLOR)

    # WEEK 4: Login UI 
    def draw_login(self, inputs, active_field, message, leaderboard=[], dev_mode_active=False, bg_surface=None):
        self._draw_background(bg_surface)
        
        # Dev Toggle
        toggle_color = self.BTN_GREEN if dev_mode_active else self.PASSIVE_BORDER
        pygame.draw.rect(self.screen, toggle_color, self.dev_trigger_rect, border_radius=15)
        knob_x = self.dev_trigger_rect.right - 15 if dev_mode_active else self.dev_trigger_rect.left + 15
        pygame.draw.circle(self.screen, self.TEXT_WHITE, (knob_x, self.dev_trigger_rect.centery), 12)
        dev_lbl = self.small_font.render("DEV MODE", True, self.PASSIVE_BORDER)
        self.screen.blit(dev_lbl, (self.dev_trigger_rect.x, self.dev_trigger_rect.y + 35))
        
        # Leaderboard
        lb_rect = pygame.Rect(40, 80, 250, 400)
        pygame.draw.rect(self.screen, self.PANEL_BG, lb_rect)
        pygame.draw.rect(self.screen, self.GOLD, lb_rect, 2)
        
        header_rect = pygame.Rect(40, 80, 250, 50)
        pygame.draw.rect(self.screen, (20, 20, 20), header_rect)
        pygame.draw.rect(self.screen, self.GOLD, header_rect, 2)
        lb_title = self.font.render("TOP PLAYERS", True, self.GOLD)
        self.screen.blit(lb_title, (header_rect.centerx - lb_title.get_width()//2, header_rect.centery - lb_title.get_height()//2))
        
        start_y = 150
        if not leaderboard:
            self.screen.blit(self.small_font.render("No records yet...", True, self.PASSIVE_BORDER), (60, start_y))
        else:
            for i, (name, score) in enumerate(leaderboard[:10]):
                color = self.GOLD if i==0 else (192,192,192) if i==1 else (205,127,50) if i==2 else self.TEXT_WHITE
                self.screen.blit(self.small_font.render(f"{i+1}. {name}: {score}", True, color), (55, start_y))
                start_y += 30

        cx = self.WIDTH // 2 + 100
        title = self.title_font.render("SNAKE GAME LOGIN", True, self.TEXT_WHITE)
        self.screen.blit(title, (cx - title.get_width()//2, 100))

        self._draw_input_box(cx - 150, 220, 300, 40, inputs["Identifier"], "Username/Email", active_field == "Identifier")
        self._draw_input_box(cx - 150, 290, 300, 40, inputs["Password"], "Password", active_field == "Password", is_pass=True)

        if message:
            msg_surf = self.small_font.render(message, True, self.BTN_RED)
            self.screen.blit(msg_surf, (cx - msg_surf.get_width()//2, 180))

        login_btn = pygame.Rect(cx - 150, 360, 140, 45)
        signup_btn = pygame.Rect(cx + 10, 360, 140, 45)
        guest_btn = pygame.Rect(cx - 150, 420, 300, 40)
        
        self._draw_button(login_btn, "LOGIN", self.BTN_GREEN)
        self._draw_button(signup_btn, "REGISTER", self.ACTIVE_BORDER)
        self._draw_button(guest_btn, "PLAY AS GUEST", (100, 100, 100))
        self.buttons = {"login_submit": login_btn, "goto_signup": signup_btn, "guest": guest_btn}

    # WEEK 4: Signup UI 
    def draw_signup(self, inputs, active_field, message, bg_surface=None):
        self._draw_background(bg_surface)
        cx = self.WIDTH // 2
        title = self.title_font.render("NEW USER REGISTRY", True, self.TEXT_WHITE)
        self.screen.blit(title, (cx - title.get_width()//2, 50))
        
        if message:
            msg_surf = self.small_font.render(message, True, self.BTN_RED)
            self.screen.blit(msg_surf, (cx - msg_surf.get_width()//2, 100))

        self._draw_input_box(cx - 310, 150, 300, 40, inputs["Username"], "Username", active_field == "Username")
        self._draw_input_box(cx - 310, 240, 300, 40, inputs["First Name"], "First Name", active_field == "First Name")
        self._draw_input_box(cx - 310, 420, 300, 40, inputs["Password"], "Password", active_field == "Password", is_pass=True)
        self._draw_input_box(cx + 10, 150, 300, 40, inputs["Email"], "Email", active_field == "Email")
        self._draw_input_box(cx + 10, 240, 300, 40, inputs["Last Name"], "Last Name", active_field == "Last Name")
        self._draw_input_box(cx + 10, 420, 300, 40, inputs["Confirm Pass"], "Confirm Pass", active_field == "Confirm Pass", is_pass=True)
        self._draw_input_box(cx - 150, 330, 300, 40, inputs["Phone"], "Phone (Optional)", active_field == "Phone")

        back_btn = pygame.Rect(cx - 310, 500, 300, 50)
        reg_btn = pygame.Rect(cx + 10, 500, 300, 50)
        self._draw_button(back_btn, "BACK TO LOGIN", self.BTN_RED)
        self._draw_button(reg_btn, "REGISTER", self.BTN_GREEN)
        self.buttons = {"back_login": back_btn, "signup_submit": reg_btn}

    # WEEK 3: Mode Selection
    def draw_mode_select(self, current_theme="Classic", bg_surface=None):
        self._draw_background(bg_surface)
        cx, cy = self.WIDTH // 2, self.HEIGHT // 2
        title = self.title_font.render("SELECT GAME MODE", True, self.TEXT_WHITE)
        self.screen.blit(title, (cx - title.get_width()//2, 80))

        btn_classic = pygame.Rect(cx - 150, cy - 100, 300, 60)
        btn_box = pygame.Rect(cx - 150, cy - 20, 300, 60)
        btn_obs = pygame.Rect(cx - 150, cy + 60, 300, 60)
        btn_theme = pygame.Rect(cx - 150, cy + 130, 300, 50)
        btn_back = pygame.Rect(cx - 150, cy + 200, 300, 50)

        self._draw_button(btn_classic, "CLASSIC (No Walls)", self.BTN_GREEN)
        self._draw_button(btn_box, "BOX MODE (Walled)", self.ACTIVE_BORDER)
        self._draw_button(btn_obs, "OBSTACLES", (200, 100, 50))
        self._draw_button(btn_theme, f"THEME: {current_theme.upper()}", (100, 100, 200))
        self._draw_button(btn_back, "LOGOUT", self.BTN_RED)

        self.buttons = {"mode_classic": btn_classic, "mode_box": btn_box, "mode_obstacles": btn_obs, "theme_toggle": btn_theme, "mode_back": btn_back}

    def draw_dev_auth(self, current_input, bg_surface=None):
        self._draw_background(bg_surface)
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0,0))
        box = pygame.Rect(self.WIDTH//2 - 150, self.HEIGHT//2 - 50, 300, 100)
        pygame.draw.rect(self.screen, (20, 20, 20), box)
        pygame.draw.rect(self.screen, self.BTN_RED, box, 2)
        txt = self.font.render("ENTER DEV PIN:", True, self.BTN_RED)
        self.screen.blit(txt, (box.x + 20, box.y + 20))
        pass_txt = self.font.render("*" * len(current_input), True, self.TEXT_WHITE)
        self.screen.blit(pass_txt, (box.x + 20, box.y + 60))

    def _draw_input_box(self, x, y, w, h, text, label, is_active, is_pass=False):
        lbl_surf = self.small_font.render(label, True, (150, 150, 150))
        self.screen.blit(lbl_surf, (x, y - 20))
        rect = pygame.Rect(x, y, w, h)
        color = self.ACTIVE_BORDER if is_active else self.INPUT_BG
        border_color = self.ACTIVE_BORDER if is_active else self.PASSIVE_BORDER
        pygame.draw.rect(self.screen, self.INPUT_BG, rect)
        pygame.draw.rect(self.screen, border_color, rect, 2)
        display_text = "*" * len(text) if is_pass else text
        txt_surf = self.font.render(display_text, True, self.TEXT_WHITE)
        self.screen.set_clip(rect.inflate(-10, -10)) 
        self.screen.blit(txt_surf, (x + 10, y + 8))
        self.screen.set_clip(None)

    def _draw_button(self, rect, text, color):
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        txt_surf = self.font.render(text, True, self.TEXT_WHITE)
        self.screen.blit(txt_surf, (rect.centerx - txt_surf.get_width()//2, rect.centery - txt_surf.get_height()//2))