# models/snake.py - The Model: Handles the Snake's Data Logic (OOP Core)

class Snake:
    
    # Define directional vectors (dx, dy)
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    # FIX: Corrected __init__ to accept max_x and max_y for wrap-around
    def __init__(self, start_pos=(10, 10), cell_size=25, max_x=40, max_y=30): 
        self.cell_size = cell_size
        
        # Save the max dimensions to the object for use in the move() method
        self.max_x = max_x # Max number of cells horizontally
        self.max_y = max_y # Max number of cells vertically
        
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
        Updates the snake's position and implements the wrap-around (looping) logic.
        """
        self.direction = self.new_direction
        dx, dy = self.direction

        current_head_x, current_head_y = self.body[0]
        
        # 1. Calculate the raw new position
        new_head_x = current_head_x + dx
        new_head_y = current_head_y + dy
        
        # 2. APPLY WRAP-AROUND LOGIC (using the modulus operator %)
        # The position is wrapped back to the other side if it goes out of bounds.
        new_head = (new_head_x % self.max_x, new_head_y % self.max_y)
        
        # 3. Insert New Head
        self.body.insert(0, new_head)

        # 4. Handle Growth or Movement
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