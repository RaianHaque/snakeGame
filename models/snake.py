import pygame

# WEEK 3: Object Oriented Programming
class Snake:
    def __init__(self, grid_w, grid_h, cell_size=25):
        self.grid_w = grid_w
        self.grid_h = grid_h
        self.cell_size = cell_size
        
        # WEEK 5: Smooth Movement Setup
        start_x = 150.0
        start_y = float((grid_h // 2) * cell_size)
        
        self.head_pos = [start_x, start_y]
        
        self.UP = (0, -1)
        self.DOWN = (0, 1)
        self.LEFT = (-1, 0)
        self.RIGHT = (1, 0)
        
        self.direction = self.RIGHT
        self.next_direction = self.RIGHT 
        
        self.speed = 3
        self.body_spacing = 5 
        # Radius 10 = 20px Diameter. 
        self.radius = 10 
        
        self.history = []
        for i in range(20): 
            self.history.append((start_x - i*self.speed, start_y))
            
        self.length = 3
        self.grow_pending = 0

    # WEEK 2: Core Logic
    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) == self.direction:
            return
        self.next_direction = new_dir

    def move(self, mode):
        self.direction = self.next_direction
        
        # Move pixels instead of grid blocks
        self.head_pos[0] += self.direction[0] * self.speed
        self.head_pos[1] += self.direction[1] * self.speed
        
        max_w = self.grid_w * self.cell_size
        max_h = self.grid_h * self.cell_size
        
        # Screen Wrapping
        if mode == "Classic" or mode == "Obstacles":
            if self.head_pos[0] < 0: self.head_pos[0] = max_w
            elif self.head_pos[0] > max_w: self.head_pos[0] = 0
            if self.head_pos[1] < 0: self.head_pos[1] = max_h
            elif self.head_pos[1] > max_h: self.head_pos[1] = 0
            
        self.history.insert(0, tuple(self.head_pos))
        
        target_size = self.length * self.body_spacing
        if len(self.history) > target_size:
            self.history.pop()

    def grow(self):
        self.length += 1

    def get_head_grid(self):
        cx = self.head_pos[0] + self.cell_size/2
        cy = self.head_pos[1] + self.cell_size/2
        return (int(cx // self.cell_size), int(cy // self.cell_size))

    # WEEK 5: Safe Food Spawn 
    def get_occupied_grids(self):
        grids = set()
        for (x, y) in self.history:
            gx = int((x + self.cell_size/2) // self.cell_size)
            gy = int((y + self.cell_size/2) // self.cell_size)
            grids.add((gx, gy))
            grids.add((gx+1, gy)); grids.add((gx-1, gy))
            grids.add((gx, gy+1)); grids.add((gx, gy-1))
        return list(grids)

    def update_grid_dimensions(self, new_grid_w, new_grid_h):
        self.grid_w = new_grid_w
        self.grid_h = new_grid_h

    # WEEK 2: Collision Detection (VISUAL MATCH)
    def check_wall_collision(self):
        # FIX: INCREASED MARGIN FOR TIGHTER WALL COLLISIONS 
        # Previous: 2.5 (Too loose, died early)
        # New: 6.0 (Tighter, must physically touch wall)
        margin = 6.0
        diameter = self.cell_size - (margin * 2) # approx 13px hitbox
        
        head_visual_rect = pygame.Rect(self.head_pos[0] + margin, self.head_pos[1] + margin, diameter, diameter)
        
        # Wall Areas
        wall_size = self.cell_size
        play_w = (self.grid_w * self.cell_size)
        play_h = (self.grid_h * self.cell_size)
        
        # Check against the 4 walls
        if head_visual_rect.left < wall_size: return True
        if head_visual_rect.right > play_w - wall_size: return True
        if head_visual_rect.top < wall_size: return True
        if head_visual_rect.bottom > play_h - wall_size: return True
            
        return False

    def check_self_collision(self):
        safe_zone = self.body_spacing * 3 
        head_rect = pygame.Rect(self.head_pos[0], self.head_pos[1], 10, 10)
        for pt in self.history[safe_zone::3]: 
            body_rect = pygame.Rect(pt[0], pt[1], 10, 10)
            if head_rect.colliderect(body_rect):
                return True
        return False
        
    def check_obstacle_collision(self, obstacles):
        margin = 6
        head_rect = pygame.Rect(self.head_pos[0] + margin, self.head_pos[1] + margin, 
                                self.cell_size - margin*2, self.cell_size - margin*2)
                                
        for (ox, oy) in obstacles:
            obs_rect = pygame.Rect(ox * self.cell_size, oy * self.cell_size, self.cell_size, self.cell_size)
            if head_rect.colliderect(obs_rect):
                return True
        return False