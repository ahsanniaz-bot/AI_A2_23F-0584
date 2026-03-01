# search.py
import heapq
import math
import time

class SearchAlgorithm:
    def __init__(self, grid, heuristic_type="Manhattan"):
        self.grid = grid
        self.explored = set()
        self.frontier_added = set()
        self.steps = []
        self.replans = 0
        self.heuristic_type = heuristic_type
        self.start_time = time.time()
        self.dynamic_mode_enabled = True  # FIXED: Add dynamic mode flag
    
    def manhattan_distance(self, pos):
        """Manhattan distance heuristic"""
        return abs(pos[0] - self.grid.goal[0]) + abs(pos[1] - self.grid.goal[1])
    
    def euclidean_distance(self, pos):
        """Euclidean distance heuristic"""
        return math.sqrt((pos[0] - self.grid.goal[0])**2 + (pos[1] - self.grid.goal[1])**2)
    
    def heuristic(self, pos):
        """Select heuristic based on type"""
        if self.heuristic_type == "Euclidean":
            return self.euclidean_distance(pos)
        else:  # Default to Manhattan
            return self.manhattan_distance(pos)
    
    def handle_dynamic_obstacle(self):
        """Spawn dynamic obstacle and check for re-planning"""
        # FIXED: Check if dynamic mode is enabled before spawning
        if not self.dynamic_mode_enabled:
            return False
        
        spawned = self.grid.spawn_dynamic_obstacle()
        if spawned:
            self.steps.append(('dynamic_obstacle', spawned))
            print(f"  ⚠️ Dynamic obstacle spawned at {spawned}")
            return True
        return False

class GBFS(SearchAlgorithm):
    """Greedy Best-First Search: f(n) = h(n)"""
    
    def __init__(self, grid, heuristic_type="Manhattan"):
        super().__init__(grid, heuristic_type)
        self.name = "GBFS"
    
    def search(self):
        visited = set([self.grid.start])
        pq = [(self.heuristic(self.grid.start), self.grid.start, [self.grid.start])]
        
        while pq:
            self.handle_dynamic_obstacle()
            
            _, node, path = heapq.heappop(pq)
            
            # Check if path is blocked
            blocked_pos = self.grid.is_path_blocked(path)
            if blocked_pos:
                print(f"  🔄 Re-planning: Path blocked at {blocked_pos}")
                self.replans += 1
                visited.clear()
                visited.add(self.grid.start)
                pq.clear()
                pq.append((self.heuristic(self.grid.start), self.grid.start, [self.grid.start]))
                self.frontier_added.clear()
                continue
            
            self.explored.add(node)
            self.steps.append(('explored', node))
            
            if node == self.grid.goal:
                return path
            
            for neighbor in self.grid.get_neighbors(node[0], node[1]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    h = self.heuristic(neighbor)
                    heapq.heappush(pq, (h, neighbor, path + [neighbor]))
                    
                    if neighbor not in self.frontier_added:
                        self.frontier_added.add(neighbor)
                        self.steps.append(('frontier', neighbor))
        
        return None

class AStar(SearchAlgorithm):
    """A* Search: f(n) = g(n) + h(n)"""
    
    def __init__(self, grid, heuristic_type="Manhattan"):
        super().__init__(grid, heuristic_type)
        self.name = "A*"
    
    def search(self):
        g_score = {self.grid.start: 0}
        pq = [(self.heuristic(self.grid.start), self.grid.start, [self.grid.start])]
        visited = set()
        
        while pq:
            self.handle_dynamic_obstacle()
            
            f, node, path = heapq.heappop(pq)
            
            if node in visited:
                continue
            
            # Check if path is blocked
            blocked_pos = self.grid.is_path_blocked(path)
            if blocked_pos:
                print(f"  🔄 Re-planning: Path blocked at {blocked_pos}")
                self.replans += 1
                visited.clear()
                g_score.clear()
                g_score[self.grid.start] = 0
                pq.clear()
                pq.append((self.heuristic(self.grid.start), self.grid.start, [self.grid.start]))
                self.frontier_added.clear()
                continue
            
            visited.add(node)
            self.explored.add(node)
            self.steps.append(('explored', node))
            
            if node == self.grid.goal:
                return path
            
            for neighbor in self.grid.get_neighbors(node[0], node[1]):
                if neighbor not in visited:
                    move_cost = self.grid.get_movement_cost(node, neighbor)
                    new_g = g_score[node] + move_cost
                    
                    if neighbor not in g_score or new_g < g_score[neighbor]:
                        g_score[neighbor] = new_g
                        h = self.heuristic(neighbor)
                        f_new = new_g + h
                        heapq.heappush(pq, (f_new, neighbor, path + [neighbor]))
                        
                        if neighbor not in self.frontier_added:
                            self.frontier_added.add(neighbor)
                            self.steps.append(('frontier', neighbor))
        
        return None