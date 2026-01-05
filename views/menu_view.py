import pygame

class MenuView:
    def __init__(self, screen):
        # WEEK 1 & 4 Setup
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 32)
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.colors = {
            "bg": (10, 40, 10), "text": (255, 255, 255), "box": (50, 80, 50), 
            "active": (200, 255, 200), "btn": (40, 90, 40), "go_bg": (5, 20, 5),
            "mute": (150, 50, 50), "placeholder": (100, 130, 100), "gold": (255, 215, 0)
        }
        self.buttons = {}
        self.game_over_buttons = {}

    def draw_menu(self, message, user_text, pass_text, active_field, leaderboard=[]):
        w, h = self.screen.get_size()
        center_x = w // 2
        self.screen.fill(self.colors["bg"])
        
        title = self.title_font.render("SNAKE GAME", True, self.colors["text"])
        self.screen.blit(title, (center_x - title.get_width() // 2, h * 0.1))

        # WEEK 4: Leaderboard
        lb_title = self.font.render("GLOBAL TOP 5", True, self.colors["gold"])
        self.screen.blit(lb_title, (50, h * 0.3))
        for i, (name, score) in enumerate(leaderboard):
            entry = self.small_font.render(f"{i+1}. {name}: {score}", True, self.colors["text"])
            self.screen.blit(entry, (50, h * 0.35 + (i * 35)))

        # WEEK 2: Placeholders for Input Boxes
        fields = [("Username", user_text), ("Password", pass_text)]
        for i, (label_name, content) in enumerate(fields):
            is_active = active_field == label_name
            color = self.colors["active"] if is_active else self.colors["box"]
            rect = pygame.Rect(center_x - 200, h * 0.3 + (i * 90), 400, 50)
            pygame.draw.rect(self.screen, color, rect, 2, border_radius=5)
            
            if content == "":
                display_text, text_color = label_name, self.colors["placeholder"]
            else:
                display_text = "*" * len(content) if label_name == "Password" else content
                text_color = self.colors["text"]

            txt_surf = self.font.render(display_text, True, text_color)
            self.screen.blit(txt_surf, (rect.x + 10, rect.y + 10))

        # WEEK 1: Buttons
        self.buttons["login"] = pygame.Rect(center_x - 205, h * 0.55, 195, 60)
        self.buttons["signup"] = pygame.Rect(center_x + 10, h * 0.55, 195, 60)
        self.buttons["guest"] = pygame.Rect(center_x - 205, h * 0.65, 410, 60)

        for name, rect in self.buttons.items():
            pygame.draw.rect(self.screen, self.colors["btn"], rect, border_radius=5)
            btn_text = self.font.render(name.upper(), True, self.colors["text"])
            self.screen.blit(btn_text, (rect.centerx - btn_text.get_width()//2, rect.centery - btn_text.get_height()//2))

        msg_surf = self.font.render(message, True, (255, 255, 100))
        self.screen.blit(msg_surf, (center_x - msg_surf.get_width() // 2, h * 0.22))

    def draw_game_over(self, final_score, high_score, is_muted):
        # WEEK 3: Navigation Buttons
        w, h = self.screen.get_size()
        center_x = w // 2
        self.screen.fill(self.colors["go_bg"])
        go_surf = self.title_font.render("GAME OVER", True, (255, 50, 50))
        self.screen.blit(go_surf, (center_x - go_surf.get_width()//2, h * 0.2))
        
        score_surf = self.font.render(f"Final Score: {final_score}", True, (255, 255, 255))
        record_surf = self.font.render(f"Personal Best: {high_score}", True, (255, 255, 100))
        self.screen.blit(score_surf, (center_x - score_surf.get_width()//2, h * 0.4))
        self.screen.blit(record_surf, (center_x - record_surf.get_width()//2, h * 0.47))

        self.game_over_buttons["restart"] = pygame.Rect(center_x - 210, h * 0.6, 200, 60)
        self.game_over_buttons["menu"] = pygame.Rect(center_x + 10, h * 0.6, 200, 60)
        self.game_over_buttons["mute"] = pygame.Rect(center_x - 100, h * 0.72, 200, 50)
        
        for name, rect in self.game_over_buttons.items():
            btn_col = self.colors["mute"] if name == "mute" else self.colors["btn"]
            pygame.draw.rect(self.screen, btn_col, rect, border_radius=5)
            label = "UNMUTE" if name == "mute" and is_muted else name.upper()
            if name == "mute" and not is_muted: label = "MUTE MUSIC"
            text = self.font.render(label, True, (255, 255, 255))
            self.screen.blit(text, (rect.centerx - text.get_width()//2, rect.centery - text.get_height()//2))