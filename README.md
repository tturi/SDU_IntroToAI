# Introduction to Artificial Intelligence - Sokoban task
The uploaded solvers has two different algorithms utilized. Both code is lacking automation and require to hardcode the Sokoban map into its code. Another thing to know that it was made for the purpose of assignment, and the code does not follow clear code requirements (i.e. oversized lines, using variables ease reading the code etc.) Also it is following Concept 2 in the enclosed report (IntroToAI_Final_Report_tatur19_aspaz19_Group51.pdf), therefore it cannot be used straigth to solve classic Sokoban maps with these scripts as the bool conditions for ending searching a node in the graphs are different then for a normal Sokoban. However it could be changed to "normal" Sokoban rules easily. Also I have uploaded a Lego Mindstorm EV3 microPython line follower script, which executes the code on a map.
## Breadth First Search implementation
#### filename = Breadth First Search - Maze.py
This is a classical maze, or labirinth solution with Breadth First Search algorithm.
#### filename = Sokoban_BFS_Quick_test_map.py
This is a mini map, solving a Sokoban like problem with two box. I have used it to test the algorithm (Note: this is again, not following the classical Sokoban rules (see report).
#### filename = Sokoban_BFS_Reduced_map.py
This test was done with a simplified competition map, where the computational time is realitly short. No meaningful routes are simple removed from map.
#### filename = Sokoban_BFS_Competition_map.py
This is the setup for the full competition map. It will run into performance issues and it clearly shows that C++ or any other compiled language might be a better alternative then Python when implementing BFS on such big graphs.
## A* search implementation
#### filename = Sokoban_A-star_Quick_test_map.py
This is the implementaiton of A* algorithm on the same Sokoban map (following same rules as above). Test shows quicker solution in that scale.
#### filename = Sokoban_A-star_Reduced_map.py
Same compeition map, with removed nonsense routes. It works with ok speed to calculate the solution
#### filename = Sokoban_A-star_Competition_map.py, Sokoban_A-star_Competition_map(1box).py, Sokoban_A-star_Competition_map(2box).py
Same compeition map with full and with reduced challeneges. All these implementaion has performance issues unfortunatly, and just another proof that a compiled implementation would probably a better idea.
## Lego Mindstorm EV3 line follower script
#### filename = Lego_line_follower.py
It is a far from perfect line following algorith written in microPython (see more info about the implementation: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3
Video about the performance of the code:
https://www.youtube.com/watch?v=DleCN5NC1Oc
