# **INSTRUCTIONS:**

1. This runs on a command line interface.
2. Make sure that you install the pygame package or you can do that by just pasting the command in your terminal 
    - pip install pygame
    - python -m pip install pygame
    - python3 -m pip install pygame
3. You can also run it in a python virtual virtual environment (optional).
4. Run it by writing "python astar.py" and "python astar-diag.py" respectively in terminal.

**This piece of code include 2 python programs for A-star search**

**1. One uses manhattan heuristic - for straight line shortest distance**

**2. Another uses octile heuristic - for diagonal shortest distance**

# Points to remenber:-
    - WHITE color says that the path is unvisited 
    - RED color says that we already visited that grid box
    - BLACK color says that this block is a barrier, it needs to be avoided by the algorithm
    - ORANGE means the start node
    - TURQUOISE means the end node
    - PURPLE is the path followed by A*
    - GREEN checks on the Open Set - which determines the path, consider it to be a backtracked set containing the path information from starting to ending node

# **Rules for the game**
1. Left Click for the first time to mark starting point - it will be orange.
2. For 2nd click it will mark the destination point - it will be turqouise.
3. Right Click any block for the removal of the marked point.
4. After selecting start and end point, you can draw the barriers (mousedrag or you can select individual block) - or avoidable blocks in search - it will be marked in black.
5. After your selection, enter space for the operation to begin.
6. Red will be the visited section, green will mark the boundaries for expansion and checking, purple will be the shortest distance found.
7. If path is not found a popup appears.
8. If you want the grid cleared, just press backspace in your keyboard.

***You're good to go!!!!***
