# viz.py
import pygame
import sys
import time
from config import *

class Visualizer:
    def __init__(self, grid, cell_size=CELL_SIZE):
        self.grid = grid
        self.cell_size = cell_size
        self.width = grid.width * cell_size + 250
        self.height = grid.height * cell_size
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font(None, 18)
        self.font_medium = pygame.font.Font(None, 22)
        self.font_large = pygame.font.Font(None, 24)
        self.font_title = pygame.font.Font(None, 28)
        
        self.start_time = time.time()
    
    def draw_grid(self):
        """Draw the grid with all cells"""
        grid_width = self.grid.width * self.cell_size
        
        for i in range(self.grid.height):
            for j in range(self.grid.width):
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                                   self.cell_size, self.cell_size)
                
                if self.grid.grid[i][j] == 4:  # Dynamic obstacle
                    pygame.draw.rect(self.screen, COLOR_DYNAMIC, rect)
                elif self.grid.grid[i][j] == 1:  # Static wall
                    pygame.draw.rect(self.screen, COLOR_WALL, rect)
                elif (i, j) == self.grid.start:  # Start
                    pygame.draw.rect(self.screen, COLOR_START, rect)
                elif (i, j) == self.grid.goal:  # Goal
                    pygame.draw.rect(self.screen, COLOR_GOAL, rect)
                else:
                    pygame.draw.rect(self.screen, COLOR_EMPTY, rect)
                
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
    
    def draw_stats(self, algorithm_name, explored_count, path_length, 
                   elapsed_time, replans, dynamic_count, heuristic_name):
        """Draw statistics panel"""
        grid_width = self.grid.width * self.cell_size
        stats_x = grid_width + 10
        stats_y = 20
        
        # Background
        stats_rect = pygame.Rect(grid_width, 0, 250, self.height)
        pygame.draw.rect(self.screen, COLOR_STATS_BG, stats_rect)
        pygame.draw.line(self.screen, (100, 100, 100), (grid_width, 0),
                         (grid_width, self.height), 2)
        
        # Title
        title = self.font_title.render("STATISTICS", True, COLOR_TEXT)
        self.screen.blit(title, (stats_x, stats_y))
        
        # Algorithm
        algo_text = self.font_large.render("Algorithm:", True, COLOR_TEXT)
        self.screen.blit(algo_text, (stats_x, stats_y + 40))
        algo_value = self.font_small.render(algorithm_name, True, (50, 150, 255))
        self.screen.blit(algo_value, (stats_x + 10, stats_y + 65))
        
        # Heuristic
        heur_text = self.font_large.render("Heuristic:", True, COLOR_TEXT)
        self.screen.blit(heur_text, (stats_x, stats_y + 90))
        heur_value = self.font_small.render(heuristic_name, True, (200, 100, 255))
        self.screen.blit(heur_value, (stats_x + 10, stats_y + 115))
        
        # Nodes explored
        explored_text = self.font_large.render("Nodes Explored:", True, COLOR_TEXT)
        self.screen.blit(explored_text, (stats_x, stats_y + 150))
        explored_value = self.font_small.render(str(explored_count), True, (255, 150, 0))
        self.screen.blit(explored_value, (stats_x + 10, stats_y + 175))
        
        # Path length
        path_text = self.font_large.render("Path Length:", True, COLOR_TEXT)
        self.screen.blit(path_text, (stats_x, stats_y + 210))
        path_value = self.font_small.render(str(path_length), True, (0, 150, 255))
        self.screen.blit(path_value, (stats_x + 10, stats_y + 235))
        
        # Time in milliseconds
        time_text = self.font_large.render("Time Taken:", True, COLOR_TEXT)
        self.screen.blit(time_text, (stats_x, stats_y + 270))
        time_ms = elapsed_time * 1000  # Convert to milliseconds
        time_value = self.font_small.render(f"{time_ms:.2f}ms", True, (150, 255, 0))
        self.screen.blit(time_value, (stats_x + 10, stats_y + 295))
        
        # Dynamic obstacles
        dynamic_text = self.font_large.render("Dynamic Obstacles:", True, COLOR_TEXT)
        self.screen.blit(dynamic_text, (stats_x, stats_y + 330))
        dynamic_value = self.font_small.render(str(dynamic_count), True, (255, 100, 0))
        self.screen.blit(dynamic_value, (stats_x + 10, stats_y + 355))
        
        # Re-plans
        replans_text = self.font_large.render("Re-plans:", True, COLOR_TEXT)
        self.screen.blit(replans_text, (stats_x, stats_y + 390))
        replans_value = self.font_small.render(str(replans), True, (200, 0, 200))
        self.screen.blit(replans_value, (stats_x + 10, stats_y + 415))
        
        # Legend
        legend_y = stats_y + 450
        legend_title = self.font_large.render("LEGEND", True, COLOR_TEXT)
        self.screen.blit(legend_title, (stats_x, legend_y))
        
        colors = [
            (COLOR_START, "Start"),
            (COLOR_GOAL, "Goal"),
            (COLOR_EXPLORED, "Explored"),
            (COLOR_FRONTIER, "Frontier"),
            (COLOR_PATH, "Path"),
            (COLOR_WALL, "Static Wall"),
        ]
        
        legend_y += 35
        for color, label in colors:
            pygame.draw.rect(self.screen, color, (stats_x, legend_y, 15, 15))
            pygame.draw.rect(self.screen, (0, 0, 0), (stats_x, legend_y, 15, 15), 1)
            label_text = self.font_small.render(label, True, COLOR_TEXT)
            self.screen.blit(label_text, (stats_x + 25, legend_y - 2))
            legend_y += 25
    
    def visualize_search(self, algorithm_name, steps, path, replans=0, heuristic_name="Manhattan"):
        """Animate search step-by-step"""
        self.screen.fill(COLOR_EMPTY)
        self.draw_grid()
        pygame.display.flip()
        pygame.time.wait(500)
        
        frontier_set = set()
        explored_set = set()
        dynamic_obstacles_set = set()
        
        for step_type, node in steps:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            
            if step_type == 'frontier':
                frontier_set.add(node)
            elif step_type == 'explored':
                if node in frontier_set:
                    frontier_set.remove(node)
                explored_set.add(node)
            elif step_type == 'dynamic_obstacle':
                dynamic_obstacles_set.add(node)
            
            self.screen.fill(COLOR_EMPTY)
            self.draw_grid()
            
            # Draw explored
            for node in explored_set:
                if node not in [self.grid.start, self.grid.goal]:
                    rect = pygame.Rect(node[1] * self.cell_size, node[0] * self.cell_size,
                                       self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, COLOR_EXPLORED, rect)
            
            # Draw frontier
            for node in frontier_set:
                if node not in [self.grid.start, self.grid.goal]:
                    rect = pygame.Rect(node[1] * self.cell_size, node[0] * self.cell_size,
                                       self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, COLOR_FRONTIER, rect)
            
            elapsed_time = time.time() - self.start_time
            path_length = len(path) if path else 0
            self.draw_stats(algorithm_name, len(explored_set), path_length,
                           elapsed_time, replans, len(dynamic_obstacles_set), heuristic_name)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        # Draw final path
        if path:
            for node in path[1:-1]:
                rect = pygame.Rect(node[1] * self.cell_size, node[0] * self.cell_size,
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, COLOR_PATH, rect)
        
        # Final frame
        self.screen.fill(COLOR_EMPTY)
        self.draw_grid()
        
        for node in explored_set:
            if node not in [self.grid.start, self.grid.goal]:
                rect = pygame.Rect(node[1] * self.cell_size, node[0] * self.cell_size,
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, COLOR_EXPLORED, rect)
        
        if path:
            for node in path[1:-1]:
                rect = pygame.Rect(node[1] * self.cell_size, node[0] * self.cell_size,
                                   self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, COLOR_PATH, rect)
        
        elapsed_time = time.time() - self.start_time
        path_length = len(path) if path else 0
        self.draw_stats(algorithm_name, len(explored_set), path_length,
                       elapsed_time, replans, len(self.grid.dynamic_obstacles), heuristic_name)
        
        pygame.display.flip()
        
        print("\n Search complete!")
        if path:
            print(f"  yup {algorithm_name} found path!")
            print(f"  Path length: {len(path)}")
            print(f"  Nodes explored: {len(explored_set)}")
            print(f"  Dynamic obstacles created: {len(self.grid.dynamic_obstacles)}")
            time_ms = elapsed_time * 1000
            print(f"  Time taken: {time_ms:.2f}ms")
        else:
            print(f"  {algorithm_name} failed to find path")
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    if event.type == pygame.KEYDOWN and event.key != pygame.K_ESCAPE:
                        continue
                    waiting = False
            self.clock.tick(30)
    
    def close(self):
        pygame.quit()


class SetupScreen:
    def __init__(self):
        self.width = 900
        self.height = 600
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)
        
        # State
        self.algorithm = "A*"
        self.heuristic = "Manhattan"
        self.dynamic_mode = False
        self.grid_rows = 20
        self.grid_cols = 20
        self.grid_density = 10
        
        self.create_buttons()
        self.running = True
        self.screen_state = 'setup'  # 'setup', 'editor', or 'done'
    
    def create_buttons(self):
        """Create button rects"""
        center_x = self.width // 2
        
        self.buttons = {
            'algo_gbfs': pygame.Rect(center_x - 200, 100, 150, 40),
            'algo_astar': pygame.Rect(center_x + 50, 100, 150, 40),
            'heur_manhattan': pygame.Rect(center_x - 200, 160, 150, 40),
            'heur_euclidean': pygame.Rect(center_x + 50, 160, 150, 40),
            'dynamic_off': pygame.Rect(center_x - 200, 220, 150, 40),
            'dynamic_on': pygame.Rect(center_x + 50, 220, 150, 40),
            'create_grid': pygame.Rect(center_x - 100, 320, 200, 50),
        }
        
        self.input_fields = {
            'rows': {'rect': pygame.Rect(center_x - 200, 420, 100, 35), 'value': str(self.grid_rows), 'active': False},
            'cols': {'rect': pygame.Rect(center_x, 420, 100, 35), 'value': str(self.grid_cols), 'active': False},
            'density': {'rect': pygame.Rect(center_x + 200, 420, 100, 35), 'value': str(self.grid_density), 'active': False},
        }
    
    def draw_setup(self):
        """Draw setup screen"""
        self.screen.fill(COLOR_EMPTY)
        
        # Title
        title = self.font_large.render("SETUP - DYNAMIC PATHFINDING AGENT", True, COLOR_TEXT)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 20))
        
        # Algorithm selection
        algo_label = self.font_medium.render("Algorithm:", True, COLOR_TEXT)
        self.screen.blit(algo_label, (self.width // 2 - 300, 105))
        
        self.draw_button('algo_gbfs', "GBFS", self.algorithm == "GBFS")
        self.draw_button('algo_astar', "A*", self.algorithm == "A*")
        
        # Heuristic selection
        heur_label = self.font_medium.render("Heuristic:", True, COLOR_TEXT)
        self.screen.blit(heur_label, (self.width // 2 - 300, 165))
        
        self.draw_button('heur_manhattan', "Manhattan", self.heuristic == "Manhattan")
        self.draw_button('heur_euclidean', "Euclidean", self.heuristic == "Euclidean")
        
        # Dynamic mode
        dynamic_label = self.font_medium.render("Dynamic Mode:", True, COLOR_TEXT)
        self.screen.blit(dynamic_label, (self.width // 2 - 340, 225))
        
        self.draw_button('dynamic_off', "OFF", not self.dynamic_mode)
        self.draw_button('dynamic_on', "ON", self.dynamic_mode)
        
        # Grid inputs
        grid_label = self.font_medium.render("Grid Settings:", True, COLOR_TEXT)
        self.screen.blit(grid_label, (self.width // 2 - 300, 375))
        
        # Rows
        rows_label = self.font_small.render("Rows:", True, COLOR_TEXT)
        self.screen.blit(rows_label, (self.width // 2 - 250, 425))
        self.draw_input('rows')
        
        # Cols (FIXED: Added label with correct positioning)
        cols_label = self.font_small.render("Cols:", True, COLOR_TEXT)
        self.screen.blit(cols_label, (self.width // 2 - 50, 425))
        self.draw_input('cols')
        
        # Density (FIXED: Added label with correct positioning)
        density_label = self.font_small.render("Density %:", True, COLOR_TEXT)
        self.screen.blit(density_label, (self.width // 2 + 125, 425))
        self.draw_input('density')
        
        # Create grid button
        self.draw_button('create_grid', "CREATE GRID", False)
        
        pygame.display.flip()
    
    def draw_button(self, key, text, is_selected):
        """Draw a button"""
        rect = self.buttons[key]
        color = (100, 100, 100) if is_selected else (200, 200, 200)
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, COLOR_TEXT, rect, 2)
        
        text_surf = self.font_medium.render(text, True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)
    
    def draw_input(self, key):
        """Draw input field"""
        field = self.input_fields[key]
        rect = field['rect']
        color = (150, 150, 255) if field['active'] else (220, 220, 220)
        
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, COLOR_TEXT, rect, 2)
        
        text_surf = self.font_small.render(field['value'], True, COLOR_TEXT)
        self.screen.blit(text_surf, (rect.x + 5, rect.y + 5))
    
    def handle_click(self, pos):
        """Handle mouse click"""
        # Algorithm buttons
        if self.buttons['algo_gbfs'].collidepoint(pos):
            self.algorithm = "GBFS"
        elif self.buttons['algo_astar'].collidepoint(pos):
            self.algorithm = "A*"
        
        # Heuristic buttons
        elif self.buttons['heur_manhattan'].collidepoint(pos):
            self.heuristic = "Manhattan"
        elif self.buttons['heur_euclidean'].collidepoint(pos):
            self.heuristic = "Euclidean"
        
        # Dynamic mode buttons
        elif self.buttons['dynamic_off'].collidepoint(pos):
            self.dynamic_mode = False
        elif self.buttons['dynamic_on'].collidepoint(pos):
            self.dynamic_mode = True
        
        # Input fields
        for key in self.input_fields:
            if self.input_fields[key]['rect'].collidepoint(pos):
                self.input_fields[key]['active'] = True
            else:
                self.input_fields[key]['active'] = False
        
        # Create grid button
        if self.buttons['create_grid'].collidepoint(pos):
            self.screen_state = 'done'
    
    def handle_key(self, event):
        """Handle keyboard input"""
        for key in self.input_fields:
            if self.input_fields[key]['active']:
                if event.key == pygame.K_BACKSPACE:
                    self.input_fields[key]['value'] = self.input_fields[key]['value'][:-1]
                elif event.unicode.isdigit():
                    self.input_fields[key]['value'] += event.unicode
    
    def run(self):
        """Run setup screen"""
        while self.running and self.screen_state == 'setup':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event)
            
            self.draw_setup()
            self.clock.tick(60)
        
        # Get values
        try:
            self.grid_rows = int(self.input_fields['rows']['value'])
            self.grid_cols = int(self.input_fields['cols']['value'])
            self.grid_density = int(self.input_fields['density']['value']) / 100.0
        except:
            self.grid_rows = 20
            self.grid_cols = 20
            self.grid_density = 0.1
        
        pygame.quit()
        
        return {
            'algorithm': self.algorithm,
            'heuristic': self.heuristic,
            'dynamic_mode': self.dynamic_mode,
            'rows': self.grid_rows,
            'cols': self.grid_cols,
            'density': self.grid_density,
            'running': self.running
        }


class EditorScreen:
    def __init__(self, grid):
        self.grid = grid
        self.width = grid.width * 30 + 250
        self.height = grid.height * 30
        self.cell_size = 30
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("MAP EDITOR - Click cells to add/remove obstacles")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font(None, 18)
        self.font_medium = pygame.font.Font(None, 24)
        
        self.start_button = pygame.Rect(self.width - 220, self.height - 60, 200, 50)
        self.running = True
        self.done = False
    
    def draw(self):
        """Draw editor"""
        self.screen.fill(COLOR_EMPTY)
        
        # Draw grid
        for i in range(self.grid.height):
            for j in range(self.grid.width):
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                
                if (i, j) == self.grid.start:
                    pygame.draw.rect(self.screen, COLOR_START, rect)
                elif (i, j) == self.grid.goal:
                    pygame.draw.rect(self.screen, COLOR_GOAL, rect)
                elif self.grid.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, COLOR_WALL, rect)
                else:
                    pygame.draw.rect(self.screen, COLOR_EMPTY, rect)
                
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
        
        # Draw info panel
        info_x = self.grid.width * self.cell_size + 10
        info_y = 20
        
        title = self.font_medium.render("MAP EDITOR", True, COLOR_TEXT)
        self.screen.blit(title, (info_x, info_y))
        
        obstacle_count = sum(row.count(1) for row in self.grid.grid)
        total_cells = self.grid.width * self.grid.height - 2
        density = (obstacle_count / total_cells) * 100 if total_cells > 0 else 0
        
        obs_text = self.font_small.render(f"Obstacles: {obstacle_count}", True, COLOR_TEXT)
        self.screen.blit(obs_text, (info_x, info_y + 40))
        
        dens_text = self.font_small.render(f"Density: {density:.1f}%", True, COLOR_TEXT)
        self.screen.blit(dens_text, (info_x, info_y + 65))
        
        instr_text = self.font_small.render("Click cells to toggle", True, COLOR_TEXT)
        self.screen.blit(instr_text, (info_x, info_y + 100))
        
        # Draw button
        pygame.draw.rect(self.screen, (100, 150, 255), self.start_button)
        pygame.draw.rect(self.screen, COLOR_TEXT, self.start_button, 2)
        button_text = self.font_medium.render("START SEARCH", True, COLOR_TEXT)
        button_text_rect = button_text.get_rect(center=self.start_button.center)
        self.screen.blit(button_text, button_text_rect)
        
        pygame.display.flip()
    
    def handle_click(self, pos):
        """Handle click on grid"""
        if self.start_button.collidepoint(pos):
            self.done = True
            return
        
        # Click on grid
        col = pos[0] // self.cell_size
        row = pos[1] // self.cell_size
        
        if 0 <= row < self.grid.height and 0 <= col < self.grid.width:
            if (row, col) not in [self.grid.start, self.grid.goal]:
                if self.grid.grid[row][col] == 1:
                    self.grid.grid[row][col] = 0
                else:
                    self.grid.grid[row][col] = 1
    
    def run(self):
        """Run editor"""
        while self.running and not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        return self.running