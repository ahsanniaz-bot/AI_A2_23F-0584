# Dynamic Pathfinding Agent - A2 Assignment

**AI 2002: Artificial Intelligence**  
**Semester:** Spring 2026  
**Instructor:** Dr. Hashim Yaseen  
**University:** FAST-NUCES, CFD Campus

---

## Project Overview

The **Dynamic Pathfinding Agent** is an intelligent navigation system that finds optimal paths in a grid-based environment using informed search algorithms. The system can handle both static obstacles and dynamically spawning obstacles, with real-time re-planning capabilities to adapt to environmental changes.

### Key Features:
- ✅ **Two Informed Search Algorithms:** GBFS and A*
- ✅ **Two Heuristic Functions:** Manhattan Distance and Euclidean Distance
- ✅ **Dynamic Grid Sizing:** User-defined rows, columns, and obstacle density
- ✅ **Interactive Map Editor:** Click to add/remove obstacles before search
- ✅ **Real-time Visualization:** 15 FPS Pygame GUI with frontier, visited, and path visualization
- ✅ **Dynamic Obstacles:** Random obstacles spawn during search with re-planning
- ✅ **Comprehensive Metrics:** Nodes explored, path cost, execution time (milliseconds), dynamic obstacles, re-planning count

---

## Team Members

- **Muhammad Ahsan Niaz** (23F-0584)

---

## Technology Stack

- **Language:** Python 3.13.11
- **GUI Framework:** Pygame 2.6.1
- **Algorithms:** GBFS, A*
- **Heuristics:** Manhattan Distance, Euclidean Distance

---

## Requirements
```
pygame==2.6.1
```

---

## Installation

### Prerequisites
- Python 3.13 or higher installed
- pip package manager

### Step 1: Clone or Download Project
```bash
git clone https://github.com/yourusername/AI_A2_23F-0584.git
cd AI_A2_23F-0584
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install pygame directly:
```bash
pip install pygame==2.6.1
```

### Step 3: Verify Installation
```bash
python -c "import pygame; print(f'Pygame version: {pygame.version.ver}')"
```

Expected output: `Pygame version: 2.6.1`

---

## Project Structure
```
AI_A2_23F_0584/
├── main.py              # Entry point and main application flow
├── grid.py              # Grid initialization and obstacle management
├── search.py            # GBFS and A* algorithm implementations
├── viz.py               # Pygame GUI, visualization, setup/editor screens
├── config.py            # Configuration constants and colors
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| **main.py** | Application entry point, handles workflow between setup, editor, and visualization |
| **grid.py** | Grid class with static/dynamic obstacle management, neighbor finding, cost calculation |
| **search.py** | SearchAlgorithm base class, GBFS and A* implementations with heuristics |
| **viz.py** | Pygame GUI including SetupScreen, EditorScreen, and Visualizer classes |
| **config.py** | Constants: window size, colors, FPS, heuristic types, dynamic probability |

---

## How to Run

### Start the Application
```bash
python main.py
```

### User Workflow

#### Step 1: Setup Screen
1. **Select Algorithm:** Click "GBFS" or "A*"
2. **Select Heuristic:** Click "Manhattan" or "Euclidean"
3. **Dynamic Mode:** Click "OFF" (no dynamic obstacles) or "ON" (obstacles spawn during search)
4. **Grid Settings:**
   - Rows: Enter 10-30 (recommended: 15-25)
   - Cols: Enter 10-30 (recommended: 15-25)
   - Density %: Enter 5-50 (obstacle percentage)
5. **Click "CREATE GRID"**

#### Step 2: Interactive Map Editor
1. Grid is displayed with:
   - 🟩 Green cell = Start (0,0)
   - 🔴 Red cell = Goal (rows-1, cols-1)
   - ⬛ Black cells = Static obstacles
   - White cells = Walkable spaces
2. **Modify Obstacles:** Click any cell to toggle obstacle on/off
3. **View Metrics:** Obstacle count and density % update in real-time
4. **Click "START SEARCH"** when satisfied

#### Step 3: Visualization & Results
1. Algorithm runs and explores the grid
2. **Visual Elements:**
   - 🟨 Yellow cells = Explored/expanded nodes
   - 🟦 Light blue cells = Frontier nodes (in priority queue)
   - 🟦 Dark blue path = Final solution
   - 🟧 Orange cells = Dynamic obstacles (if mode ON)
3. **Statistics Panel** shows:
   - Algorithm used (GBFS/A*)
   - Heuristic used (Manhattan/Euclidean)
   - Nodes explored count
   - Path length
   - Execution time (milliseconds)
   - Dynamic obstacles encountered
   - Number of re-planning events
4. **Console Output** displays:
```
   Running [Algorithm] with [Heuristic]
   Static obstacles: XX
   ⚠️ Dynamic obstacle spawned at (X, Y)  [if dynamic mode ON]
   🔄 Re-planning: Path blocked at (X, Y) [if replanning triggered]
   yup [Algorithm] found path!
   Path length: XX
   Nodes explored: XX
   Dynamic obstacles created: XX
   Times algorithm re-planned: X
   Time taken: XXXX.XXms
```
5. **Return to Setup:** Press ENTER in console to run another test

---

## Algorithm Details

### Greedy Best-First Search (GBFS)
- **Evaluation Function:** f(n) = h(n) only
- **Strategy:** Always expands the node with lowest heuristic value
- **Advantage:** Fast, reaches goal quickly
- **Disadvantage:** May not find shortest path, explores many nodes
- **Best For:** Large grids with simple paths

### A* Algorithm
- **Evaluation Function:** f(n) = g(n) + h(n)
- **Strategy:** Balances cost from start (g) and estimated cost to goal (h)
- **Advantage:** Finds optimal path, more efficient than GBFS
- **Disadvantage:** Slightly slower, uses more memory
- **Best For:** When optimal path is required

### Heuristic Functions

#### Manhattan Distance
```
h(n) = |x_goal - x_current| + |y_goal - y_current|
```
- Assumes 4-directional movement (up, down, left, right)
- Slightly underestimates actual distance with diagonals
- Generally faster computation

#### Euclidean Distance
```
h(n) = √((x_goal - x_current)² + (y_goal - y_current)²)
```
- Straight-line distance
- Better heuristic when diagonal movement allowed
- Slightly slower computation but better guidance

---

## Testing & Results

### Test Configuration Summary

All tests performed on a machine with Python 3.13.11 and Pygame 2.6.1.

#### Test Case 1: GBFS + Manhattan (BEST CASE)
- **Grid:** 15×15 with 5% obstacles
- **Dynamic Mode:** OFF
- **Results:**
  - Nodes Explored: 19
  - Path Length: 19
  - Time Taken: 4662.51 ms
  - Dynamic Obstacles: 0
  - Re-plans: 0

**Analysis:** Sparse grid with GBFS explores quickly. Low node count indicates efficient frontier-based exploration toward goal.

---

#### Test Case 2: GBFS + Manhattan (WORST CASE)
- **Grid:** 25×25 with 40% obstacles
- **Dynamic Mode:** ON
- **Results:**
  - Nodes Explored: 37
  - Path Length: 0 (No path found)
  - Time Taken: 5604.00 ms
  - Dynamic Obstacles: 4
  - Re-plans: 0

**Analysis:** Dense grid with dynamic obstacles makes pathfinding impossible. Goal becomes unreachable as obstacles spawn. Despite dynamic obstacles, algorithm doesn't trigger re-planning (blocked areas prevent path execution).

---

#### Test Case 3: GBFS + Euclidean (BEST CASE)
- **Grid:** 15×15 with 5% obstacles
- **Dynamic Mode:** OFF
- **Results:**
  - Nodes Explored: 16
  - Path Length: 16
  - Time Taken: 4321.30 ms
  - Dynamic Obstacles: 0
  - Re-plans: 0

**Analysis:** Euclidean heuristic explores FEWER nodes (16 vs 19) than Manhattan for sparse grid. Diagonal distance estimates are more accurate, directing search more efficiently toward goal.

---

#### Test Case 4: GBFS + Euclidean (WORST CASE)
- **Grid:** 25×25 with 40% obstacles
- **Dynamic Mode:** ON
- **Results:**
  - Nodes Explored: 103
  - Path Length: 0 (No path found)
  - Time Taken: 20833.21 ms
  - Dynamic Obstacles: 15
  - Re-plans: 2

**Analysis:** Euclidean explores MORE nodes (103 vs 37) than Manhattan in worst case. More accurate heuristic explores more thoroughly but takes longer. Dynamic obstacles trigger 2 re-planning attempts.

---

#### Test Case 5: A* + Manhattan (BEST CASE)
- **Grid:** 15×15 with 5% obstacles
- **Dynamic Mode:** OFF
- **Results:**
  - Nodes Explored: 16
  - Path Length: 16
  - Time Taken: 4266.42 ms
  - Dynamic Obstacles: 0
  - Re-plans: 0

**Analysis:** A* with Manhattan explores FEWER nodes (16) than GBFS (19) for same grid. g(n) cost component prevents unnecessary exploration, finding path more directly.

---

#### Test Case 6: A* + Manhattan (WORST CASE)
- **Grid:** 25×25 with 40% obstacles
- **Dynamic Mode:** ON
- **Results:**
  - Nodes Explored: 42
  - Path Length: 0 (No path found)
  - Time Taken: 12778.86 ms
  - Dynamic Obstacles: 8
  - Re-plans: 2

**Analysis:** A* significantly better than GBFS for worst case. Explores only 42 nodes vs GBFS's 37 (similar). However, faster execution (12778ms vs 5604ms) due to better path cost guidance. 2 re-planning attempts triggered by dynamic obstacles.

---

#### Test Case 7: A* + Euclidean (BEST CASE)
- **Grid:** 15×15 with 5% obstacles
- **Dynamic Mode:** OFF
- **Results:**
  - Nodes Explored: 15
  - Path Length: 15
  - Time Taken: 4262.81 ms
  - Dynamic Obstacles: 0
  - Re-plans: 0

**Analysis:** MOST EFFICIENT combination. A* + Euclidean explores only 15 nodes (best of all). Perfect heuristic + optimal algorithm = direct path with minimal exploration.

---

#### Test Case 8: A* + Euclidean (WORST CASE)
- **Grid:** 25×25 with 40% obstacles
- **Dynamic Mode:** ON
- **Results:**
  - Nodes Explored: 89
  - Path Length: 0 (No path found)
  - Time Taken: 36184.59 ms
  - Dynamic Obstacles: 20
  - Re-plans: 3

**Analysis:** Euclidean explores more (89 vs 42) than Manhattan even in A*. More accurate diagonal heuristic explores corners thoroughly. Dynamic obstacles spawn maximum (20), triggering 3 re-planning attempts. Longest execution time due to thorough exploration.

---

## Algorithm Comparison

### Best Case Performance (15×15, 5% obstacles, No Dynamic)

| Algorithm | Heuristic | Nodes Explored | Path Length | Time (ms) |
|-----------|-----------|---|---|---|
| GBFS | Manhattan | 19 | 19 | 4662.51 |
| GBFS | Euclidean | 16 | 16 | 4321.30 |
| A* | Manhattan | 16 | 16 | 4266.42 |
| A* | Euclidean | 15 | 15 | 4262.81 |

**Winner:** A* + Euclidean (15 nodes, 4262.81ms)

### Worst Case Performance (25×25, 40% obstacles, Dynamic ON)

| Algorithm | Heuristic | Nodes Explored | Time (ms) | Dynamic Obs | Re-plans |
|-----------|-----------|---|---|---|---|
| GBFS | Manhattan | 37 | 5604.00 | 4 | 0 |
| GBFS | Euclidean | 103 | 20833.21 | 15 | 2 |
| A* | Manhattan | 42 | 12778.86 | 8 | 2 |
| A* | Euclidean | 89 | 36184.59 | 20 | 3 |

**Most Efficient:** GBFS + Manhattan (37 nodes, 5604ms)  
**Most Thorough:** A* + Euclidean (89 nodes, 20 dynamic obstacles)

---

## Key Findings

### 1. Algorithm Efficiency
- **A* > GBFS** in best case scenarios (explores fewer nodes)
- **GBFS faster** when path becomes impossible (early termination possible)
- Difference becomes significant in larger grids

### 2. Heuristic Impact
- **Manhattan** better for early termination (fewer explorations)
- **Euclidean** better for optimal guidance but explores more thoroughly
- Euclidean advantage increases with obstacle density

### 3. Dynamic Obstacles
- Dynamic obstacles spawn randomly (10% probability per step)
- **Re-planning triggered** when obstacles block current path
- **Dynamic OFF** disables spawning completely (0 obstacles)
- **Dynamic ON** causes 2-3 re-planning events in worst case

### 4. Execution Time
- Times in milliseconds vary (4000-36000ms) due to:
  - Grid size (15×15 vs 25×25)
  - Obstacle density (5% vs 40%)
  - Dynamic spawning probability
  - Number of re-planning events
  - Algorithm exploration depth

---

## Features Implemented (22 Requirements)

### Phase 1: Environment (5/5) ✅
- [x] Dynamic Grid Sizing (user input)
- [x] Fixed Start & Goal Nodes
- [x] Random Map Generation (user-defined density)
- [x] Interactive Map Editor (click to toggle)
- [x] No static .txt files (all in-memory)

### Phase 2: Algorithms (6/6) ✅
- [x] GBFS: f(n) = h(n)
- [x] A*: f(n) = g(n) + h(n)
- [x] Manhattan Distance heuristic
- [x] Euclidean Distance heuristic
- [x] GUI Algorithm Selection (buttons)
- [x] GUI Heuristic Selection (buttons)

### Phase 3: Dynamic & Re-planning (5/5) ✅
- [x] Dynamic Mode Toggle (ON/OFF)
- [x] Spawning Logic (random probability)
- [x] Re-planning Mechanism (detects & recalculates)
- [x] Efficiency Optimization (only replan if blocked)
- [x] Console feedback with emojis

### Phase 4: Visualization & Metrics (6/6) ✅
- [x] Frontier Nodes visualization (Light Blue)
- [x] Visited Nodes visualization (Yellow)
- [x] Final Path visualization (Dark Blue)
- [x] Real-time Metrics Dashboard
- [x] Path Cost display
- [x] Execution Time in milliseconds

---

## GUI Controls

### Setup Screen
- **Algorithm Buttons:** GBFS / A* (click to select)
- **Heuristic Buttons:** Manhattan / Euclidean (click to select)
- **Dynamic Mode:** OFF / ON (toggle dynamic obstacles)
- **Grid Input Fields:** Rows, Cols, Density % (click to edit)
- **CREATE GRID:** Proceed to Map Editor

### Map Editor
- **Grid Display:** Visual representation with obstacles
- **Click Cells:** Toggle obstacles white ↔ black
- **Metrics:** Live obstacle count and density percentage
- **START SEARCH:** Begin pathfinding algorithm

### Visualization
- **Real-time Animation:** 15 FPS smooth visualization
- **Legend:** Color key for frontier, explored, path, obstacles
- **Statistics Panel:** Complete metrics on right side
- **Close Window:** Press ESC or click X to return to setup

---

## Troubleshooting

### Issue: pygame module not found
**Solution:**
```bash
pip install pygame==2.6.1
```

### Issue: Window size too large for screen
**Solution:**  
Grid will auto-scale based on available screen space. If needed, reduce grid size in setup screen (rows/cols).

### Issue: Algorithm takes very long to complete
**Solution:**  
This is normal for large dense grids (25×25, 40%+). Try smaller grid (15×15) or lower density (5-10%).

### Issue: No path found (Path Length: 0)
**Solution:**  
Goal became unreachable due to obstacles. Try lower density or smaller grid.

---

## Future Enhancements

- [ ] Adjustable animation speed
- [ ] Save/load grid configurations
- [ ] Performance comparison charts
- [ ] Path cost visualization (different colors per cost)
- [ ] Bidirectional search algorithm
- [ ] More heuristic options (Chebyshev, etc.)
- [ ] Replay pathfinding animation
- [ ] Statistics export to CSV

---

## References

- Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach (4th ed.)*
- Pygame Documentation: https://www.pygame.org/docs/
- Python Documentation: https://docs.python.org/3/
- A* Pathfinding Algorithm: https://en.wikipedia.org/wiki/A*_search_algorithm

---

## License

This project was developed as part of the AI 2002 course assignment at FAST-NUCES.

---

## Contact & Support

**Student:** Muhammad Ahsan Niaz  
**Roll Number:** 23F-0584  
**Email:** f230584@cfd.nu.edu.pk  
**Course:** AI 2002 - Artificial Intelligence  
**Instructor:** Dr. Hashim Yaseen  
**University:** FAST-NUCES, CFD Campus  
**Semester:** Spring 2026

For questions or issues, please contact the course instructor or refer to the implementation documentation.

---

**Last Updated:** March 2026  
**Version:** 1.0.0 - Final Submission