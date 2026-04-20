# The main file that will hold the functions of the A* hint option
import heapq

def get_manhattan_dist(state, size):
    dist = 0
    for i, tile in enumerate(state):
        if tile != 0:
            # Current position
            cur_row, cur_col = i // size, i % size
            # Goal position (assuming 1, 2, 3... 0)
            goal_row, goal_col = (tile - 1) // size, (tile - 1) % size
            dist += abs(cur_row - goal_row) + abs(cur_col - goal_col)
    return dist

def a_star(start_state):
    goal = list(range(1, 9)) + [0] # [1, 2, 3, 4, 5, 6, 7, 8, 0]
    size = 3
    queue = [(get_manhattan_dist(start_state, size), 0, start_state, [])]
    visited = set()

    while queue:
        (f, g, current, path) = heapq.heappop(queue)
        
        if current == goal:
            return path[0] if path else None # Return the very next move

        state_tuple = tuple(current)
        if state_tuple in visited: continue
        visited.add(state_tuple)

        # Logic to find neighbors (empty space swaps) goes here...
        # Returns the next state we should move toward