class Snake:
    UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

    def __init__(self, start_pos=(10, 10), cell_size=25, max_x=51, max_y=28): 
        self.cell_size = cell_size
        self.max_x = max_x 
        self.max_y = max_y
        self.body = [start_pos, (start_pos[0]-1, start_pos[1]), (start_pos[0]-2, start_pos[1])]
        self.direction = self.RIGHT
        self.new_direction = self.direction
        self.grow_pending = False

    def move(self):
        self.direction = self.new_direction
        
        # TELEPORT LOGIC: Modulo (%) ensures perfect teleportation at the edges
        # This prevents the "skipping" by wrapping exactly at max_x and max_y
        new_head = ((self.body[0][0] + self.direction[0]) % self.max_x, 
                    (self.body[0][1] + self.direction[1]) % self.max_y)
        
        self.body.insert(0, new_head)
        if self.grow_pending: 
            self.grow_pending = False
        else: 
            self.body.pop()

    def change_direction(self, new_dir):
        # Prevent 180-degree turns into self
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.new_direction = new_dir

    def grow(self): 
        self.grow_pending = True
        
    def get_head_position(self): 
        return self.body[0]
        
    def check_self_collision(self): 
        return self.body[0] in self.body[1:]