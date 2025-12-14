# models/snake.py - The Model: Handles the Snake's Data Logic (OOP Core)

class Snake:
    """
    Represents the Snake's state, position, and movement logic. 
    """
    
    # Define directional vectors (dx, dy)
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __init__(self, start_pos=(10, 10), cell_size=25):
        self.cell_size = cell_size
        
        # Body is a list of (x, y) grid coordinates.
        self.body = [start_pos, (start_pos[0] - 1, start_pos[1]), (start_pos[0] - 2, start_pos[1])]
        
        self.direction = self.RIGHT 
        self.new_direction = self.direction 
        
        self.grow_pending = False 

    def change_direction(self, new_dir):
        """
        Sets a new intended direction, preventing immediate reversal (180-degree turn).
        """
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.new_direction = new_dir

    def move(self):
        """
        Updates the snake's position based on the current direction.
        """
        self.direction = self.new_direction
        dx, dy = self.direction

        current_head_x, current_head_y = self.body[0]
        new_head = (current_head_x + dx, current_head_y + dy)
        
        self.body.insert(0, new_head)

        if self.grow_pending:
            self.grow_pending = False
        else:
            self.body.pop()

    def grow(self):
        """
        Flags the snake to grow on the next 'move' cycle.
        """
        self.grow_pending = True
        
    def get_head_position(self):
        """
        Returns the (x, y) grid coordinates of the snake's head.
        """
        return self.body[0]

    def check_self_collision(self):
        """
        Checks if the head has collided with any other part of the body.
        """
        return self.body[0] in self.body[1:]