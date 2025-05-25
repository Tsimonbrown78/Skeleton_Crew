import random
import time  

# Queens for the board size
N = 8


def generate_random_state():
    return [random.randint(0, N-1) for _ in range(N)]


def print_board(state):
    for row in range(N):
        line = ""
        for col in range(N):
            if state[col] == row:
                line += "Q "  # Queen position
            else:
                line += ". "  # Empty space
        print(line)
    print()  


def calculate_conflicts(state):
    conflicts = 0
    for i in range(N):
        for j in range(i+1, N):
            # Check if queens i and j are attacking each other
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def generate_neighbors(state):
    neighbors = []
    for col in range(N):
        for row in range(N):
            if row != state[col]:  # Don't move the queen to its current row
                new_state = state[:]
                new_state[col] = row  # Move the queen to a new row
                neighbors.append(new_state)
    return neighbors


def hill_climbing():
    current_state = generate_random_state()
    current_conflicts = calculate_conflicts(current_state)

    print(f"Initial state (Board):")
    print_board(current_state)
    print(f"Initial conflicts: {current_conflicts}")

    if current_conflicts == 0:
        print("Solution found in the first run!")
        return current_state, 0  # No moves needed

    iterations = 0
    moves_counter = 0  
    while current_conflicts > 0:
        neighbors = generate_neighbors(current_state)
        next_state = None
        next_conflicts = float('inf')

        for neighbor in neighbors:
            neighbor_conflicts = calculate_conflicts(neighbor)
            if neighbor_conflicts < next_conflicts:
                next_conflicts = neighbor_conflicts
                next_state = neighbor
        
        if next_conflicts >= current_conflicts:
            break
        
        current_state = next_state
        current_conflicts = next_conflicts
        iterations += 1
        moves_counter += 1  
        
        print(f"Iteration {iterations}:")
        print_board(current_state)
        print(f"Conflicts: {current_conflicts}")

    if current_conflicts == 0:
        print("Solution found!")
        print(f"Number of moves {moves_counter}")
        return current_state, moves_counter  
    else:
        print("No solution found, local maximum reached.")
        print(f"Number of moves {moves_counter}")
        return None, moves_counter  


def run_multiple_trials():
    trials = 0
    solution = None
    total_moves = 0  

    while solution is None and trials < 20:
        trials += 1
        print(f"\nTrial {trials}...")
        solution, moves = hill_climbing()
        total_moves += moves  

    if solution is None:
        print("\nNo solution found in the first 20 trials. Continuing...")
    
    return solution, trials, total_moves


def main():
    start_time = time.time()  

    total_instances = 0
    successful_solutions = 0
    total_moves = 0  

    while successful_solutions == 0:
        solution, trials, moves = run_multiple_trials()
        total_instances += trials
        total_moves += moves  

        if solution is not None:
            successful_solutions += 1
            print("\nFinal solution found:")
            print_board(solution)
            break

    if total_instances > 0:
        success_percentage = (successful_solutions / total_instances) * 100
        print(f"\nTotal instances generated: {total_instances}")
        print(f"Number of successful solutions found: {successful_solutions}")
        print(f"Percentage of solved problems: {success_percentage:.2f}%")

    end_time = time.time()  
    duration = end_time - start_time
    print(f"\nTotal time taken: {duration:.4f} seconds")
    print(f"Total moves made across all trials: {total_moves}")


# Start the program
if __name__ == "__main__":
    main()
