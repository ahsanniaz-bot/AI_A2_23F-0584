# main.py
from grid import Grid
from search import GBFS, AStar
from viz import Visualizer, SetupScreen, EditorScreen
import sys

def run_algorithm(grid, algo_name, algorithm, heuristic_name, dynamic_mode):
    """Run algorithm and visualize"""
    print(f"\nRunning {algo_name} with {heuristic_name}")
    print(f"  Static obstacles: {sum(row.count(1) for row in grid.grid)}")
    
    path = algorithm.search()
    
    if path:
        print(f"  yup {algo_name} found path!")
        print(f"  Path length: {len(path)}")
        print(f"  Nodes explored: {len(algorithm.explored)}")
        print(f"  Dynamic obstacles encountered: {len(grid.dynamic_obstacles)}")
        print(f"  Times algorithm re-planned: {algorithm.replans}")
    else:
        print(f"  {algo_name} failed to find path")
        print(f"  Nodes explored: {len(algorithm.explored)}")
        print(f"  Dynamic obstacles encountered: {len(grid.dynamic_obstacles)}")
        print(f"  Times algorithm re-planned: {algorithm.replans}")
    
    print(f"  Opening visualization window...")
    visualizer = Visualizer(grid, cell_size=30)
    visualizer.visualize_search(algo_name, algorithm.steps, path, algorithm.replans, heuristic_name)
    visualizer.close()
    print(f"  [Window closed]")

def main():
    while True:
        # Show setup screen
        setup = SetupScreen()
        result = setup.run()
        
        if not result['running']:
            print("\nProgram end!")
            break
        
        # Create grid
        grid = Grid(width=result['cols'], height=result['rows'], 
                   obstacle_probability=result['density'],
                   dynamic_obstacle_probability=0.10)
        
        # Show map editor
        editor = EditorScreen(grid)
        if not editor.run():
            print("\nProgram end!")
            break
        
        # Create algorithm with selected heuristic
        algo_dict = {
            'GBFS': GBFS(grid, heuristic_type=result['heuristic']),
            'A*': AStar(grid, heuristic_type=result['heuristic']),
        }
        
        algorithm = algo_dict[result['algorithm']]
        
        # FIXED: Pass dynamic mode to algorithm
        algorithm.dynamic_mode_enabled = result['dynamic_mode']
        
        # Run algorithm
        run_algorithm(grid, result['algorithm'], algorithm, result['heuristic'], result['dynamic_mode'])
        
        input("\nPress Enter to return to setup")

if __name__ == "__main__":
    main()