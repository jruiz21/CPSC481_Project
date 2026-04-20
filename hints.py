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

def get_neighbors(state, size):
    neighbors = []
    blank = state.index(0)
    blank_row, blank_col = blank // size, blank % size

    moves = {
        'up': (blank_row - 1, blank_col),
        'down': (blank_row + 1, blank_col),
        'left': (blank_row, blank_col - 1),
        'right': (blank_row, blank_col + 1),
    }

    for _, (new_row, new_col) in moves.items():
        if 0 <= new_row < size and 0 <= new_col < size:
            new_blank = new_row * size + new_col
            new_state = list(state)
            new_state[blank], new_state[new_blank] = new_state[new_blank], new_state[blank]
            neighbors.append((new_state, new_blank))
    return neighbors

def a_star(start_state):
    goal = list(range(1, 9)) + [0] # [1, 2, 3, 4, 5, 6, 7, 8, 0]
    size = 3
    counter = 0
    queue = [(get_manhattan_dist(start_state, size), counter, 0, start_state, [])]
    visited = set()

    while queue:
        f, _, g, current, path = heapq.heappop(queue)
        
        if current == goal:
            return path[0] if path else None # Return the very next move

        state_tuple = tuple(current)
        if state_tuple in visited: continue
        visited.add(state_tuple)

        # Logic to find neighbors (empty space swaps) goes here...
        # Returns the next state we should move toward
        for new_state, _ in get_neighbors(current, size):
            if tuple(new_state) not in visited:
                new_g = g + 1
                new_h = get_manhattan_dist(new_state, size)
                counter += 1
                new_path = path + [new_state] if not path else path
                heapq.heappush(queue, (new_g + new_h, counter, new_g, new_state, new_path))
    return None