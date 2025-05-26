import heapq

# Goal state for the 8-puzzle
GOAL_STATE = (0, 1, 2, 3, 4, 5, 6, 7, 8)

# Directions for moving the empty space (up, down, left, right)
MOVES = [(-3, "up"), (3, "down"), (-1, "left"), (1, "right")]

def manhattan_distance(state):
    """
    Calculate the total Manhattan distance of the current state from the goal state.
    """
    distance = 0
    for i in range(9):
        value = state[i]
        if value != 0:
            goal_pos = GOAL_STATE.index(value)
            current_row, current_col = divmod(i, 3)
            goal_row, goal_col = divmod(goal_pos, 3)
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

def get_neighbors(state):
    """
    Generate all possible states that can be reached by moving the empty space.
    """
    neighbors = []
    zero_pos = state.index(0)
    zero_row, zero_col = divmod(zero_pos, 3)

    for move, direction in MOVES:
        new_pos = zero_pos + move
        if 0 <= new_pos < 9:  # Valid position
            if direction == "up" and zero_row == 0:
                continue
            if direction == "down" and zero_row == 2:
                continue
            if direction == "left" and zero_col == 0:
                continue
            if direction == "right" and zero_col == 2:
                continue
            
            # Swap the empty space with the new position
            new_state = list(state)
            new_state[zero_pos], new_state[new_pos] = new_state[new_pos], new_state[zero_pos]
            neighbors.append((tuple(new_state), direction))
    
    return neighbors

def a_star_search(start_state):
    """
    A* search algorithm to solve the 8-puzzle problem.
    """
    # Priority queue to store the states with their f(n) = g(n) + h(n)
    open_list = []
    heapq.heappush(open_list, (manhattan_distance(start_state), 0, start_state, []))
    
    # Set of visited states to avoid revisiting
    visited = set()
    visited.add(start_state)
    
    while open_list:
        _, g_cost, current_state, path = heapq.heappop(open_list)

        # Check if we have reached the goal state
        if current_state == GOAL_STATE:
            return path
        
        # Generate neighbors and calculate f(n) for each
        for neighbor, move in get_neighbors(current_state):
            if neighbor not in visited:
                visited.add(neighbor)
                f_cost = g_cost + 1 + manhattan_distance(neighbor)  # f(n) = g(n) + h(n)
                heapq.heappush(open_list, (f_cost, g_cost + 1, neighbor, path + [(move, neighbor)]))
    
    return None  # No solution found

def print_solution(path):
    """
    Print the solution steps including the state and the move.
    """
    if path is None:
        print("No solution found.")
    else:
        print("Solution found in", len(path), "steps:")
        for i, (move, state) in enumerate(path):
            print(f"Step {i+1}: Move '{move}'")
            print_board(state)
            print()

def print_board(state):
    """
    Print the current board state in a 3x3 format.
    """
    for i in range(0, 9, 3):
        print(state[i:i+3])

def main():
    # Input the initial state as a 3x3 matrix (space-separated)
    print("Enter the initial state of the 8-puzzle (9 numbers separated by spaces):")
    initial_state = tuple(map(int, input().split()))

    # Call the A* search function
    solution = a_star_search(initial_state)

    # Print the solution steps
    print_solution(solution)

if __name__ == "__main__":
    main()
