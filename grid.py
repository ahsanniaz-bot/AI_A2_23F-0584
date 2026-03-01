# grid.py
import random

class Grid:
    def __init__(self, width=20, height=20, obstacle_probability=0.1, 
                 dynamic_obstacle_probability=0.10):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        
        # 0 = empty, 1 = static wall, 2 = start, 3 = goal, 4 = dynamic obstacle
        self.start = (0, 0)
        self.goal = (height - 1, width - 1)
        
        self.dynamic_obstacle_probability = dynamic_obstacle_probability
        self.dynamic_obstacles = set()
        
        # Mark start and goal
        self.grid[self.start[0]][self.start[1]] = 2
        self.grid[self.goal[0]][self.goal[1]] = 3
        
        # Add static obstacles
        self.add_obstacles(obstacle_probability)
    
    def add_obstacles(self, probability):
        """Add random static walls with consistent distribution"""
        total_cells = self.width * self.height - 2
        target_obstacle_count = int(total_cells * probability)
        actual_count = 0
        
        possible_positions = []
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in [self.start, self.goal]:
                    possible_positions.append((i, j))
        
        random.shuffle(possible_positions)
        
        for i, (row, col) in enumerate(possible_positions):
            if actual_count >= target_obstacle_count:
                break
            self.grid[row][col] = 1
            actual_count += 1
    
    def spawn_dynamic_obstacle(self):
        """Spawn a random dynamic obstacle during algorithm execution"""
        if random.random() < self.dynamic_obstacle_probability:
            attempts = 0
            max_attempts = 50
            
            while attempts < max_attempts:
                row = random.randint(0, self.height - 1)
                col = random.randint(0, self.width - 1)
                
                if ((row, col) not in [self.start, self.goal] and
                    self.grid[row][col] == 0 and
                    (row, col) not in self.dynamic_obstacles):
                    
                    self.grid[row][col] = 4
                    self.dynamic_obstacles.add((row, col))
                    return (row, col)
                
                attempts += 1
        
        return None
    
    def remove_dynamic_obstacle(self, pos):
        """Remove a dynamic obstacle"""
        if pos in self.dynamic_obstacles:
            self.dynamic_obstacles.remove(pos)
            self.grid[pos[0]][pos[1]] = 0
    
    def is_path_blocked(self, path):
        """Check if current path is blocked by dynamic obstacles"""
        for pos in path:
            if self.grid[pos[0]][pos[1]] == 4:
                return pos
        return None
    
    def is_walkable(self, row, col):
        """Check if a cell is walkable"""
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col] not in [1, 4]
        return False
    
    def get_neighbors(self, row, col):
        """Get neighbors in order: Up, Right, Down, Down-Right, Left, Up-Left"""
        neighbors = []
        
        # Up
        if self.is_walkable(row - 1, col):
            neighbors.append((row - 1, col))
        
        # Right
        if self.is_walkable(row, col + 1):
            neighbors.append((row, col + 1))
        
        # Down
        if self.is_walkable(row + 1, col):
            neighbors.append((row + 1, col))
        
        # Down-Right (Diagonal)
        if (self.is_walkable(row + 1, col + 1) and
            self.is_walkable(row + 1, col) and
            self.is_walkable(row, col + 1)):
            neighbors.append((row + 1, col + 1))
        
        # Left
        if self.is_walkable(row, col - 1):
            neighbors.append((row, col - 1))
        
        # Up-Left (Diagonal)
        if (self.is_walkable(row - 1, col - 1) and
            self.is_walkable(row - 1, col) and
            self.is_walkable(row, col - 1)):
            neighbors.append((row - 1, col - 1))
        
        return neighbors
    
    def get_movement_cost(self, from_pos, to_pos):
        """Calculate movement cost: 1.0 for cardinal, 1.414 for diagonal"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        
        if row_diff == 1 and col_diff == 1:
            return 1.414  # Diagonal
        else:
            return 1.0  # Cardinal