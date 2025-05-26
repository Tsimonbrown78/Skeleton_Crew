import time
import heapq
import itertools

# Define the distance matrix for the cities
DISTANCES = {
    'A': {'A': 0, 'B': 10, 'C': 15, 'D': 20, 'E': 30},
    'B': {'A': 10, 'B': 0, 'C': 35, 'D': 25, 'E': 40},
    'C': {'A': 15, 'B': 35, 'C': 0, 'D': 30, 'E': 50},
    'D': {'A': 20, 'B': 25, 'C': 30, 'D': 0, 'E': 60},
    'E': {'A': 30, 'B': 40, 'C': 50, 'D': 60, 'E': 0}
}

# Update the list of cities to include 'E'
CITIES = ['A', 'B', 'C', 'D', 'E']

# Calculate the Minimum Spanning Tree (MST) for a set of cities
def mst_cost(cities):
    """Calculate the cost of the Minimum Spanning Tree using a simple greedy approach."""
    if len(cities) <= 1:
        return 0
    
    total_cost = 0
    visited = set([cities[0]])
    edges = []
    
    # Create a list of all edges with distances
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            cost = DISTANCES[cities[i]][cities[j]]
            edges.append((cost, cities[i], cities[j]))
    
    # Sort edges by their weight (cost)
    edges.sort()
    
    # Kruskal's algorithm to calculate MST cost
    parent = {city: city for city in cities}
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_x] = root_y
    
    # Pick the edges in order of increasing weight
    for cost, u, v in edges:
        if find(u) != find(v):
            union(u, v)
            total_cost += cost
            visited.add(u)
            visited.add(v)
    
    return total_cost

# A* search for TSP
def a_star_tsp():
    # Priority queue: elements are tuples (f(n), g(n), state), where:
    # f(n) = g(n) + h(n), g(n) = cost of the path so far, h(n) = MST heuristic
    pq = []
    # Initial state: starting from city 'A' with no cities visited
    start_state = ('A',)
    heapq.heappush(pq, (0 + mst_cost([start_state[0]]), 0, start_state))  # f(n), g(n), state
    
    # Dictionary to store the minimum g(n) for each state
    visited = {}
    visited[start_state] = 0
    
    while pq:
        f_n, g_n, state = heapq.heappop(pq)
        
        # Goal: if the state contains all cities, complete the tour
        if len(state) == len(CITIES):
            # Return to the starting city (A)
            total_cost = g_n + DISTANCES[state[-1]][state[0]]
            return state + (state[0],), total_cost
        
        # Explore the next cities to visit
        current_city = state[-1]
        unvisited_cities = set(CITIES) - set(state)
        
        for city in unvisited_cities:
            # Calculate new state
            new_state = state + (city,)
            new_g_n = g_n + DISTANCES[current_city][city]
            
            # Calculate heuristic: MST for the unvisited cities
            remaining_cities = [c for c in CITIES if c not in new_state]
            remaining_cities_set = set(remaining_cities)  # Convert to set
            remaining_cities_list = list(remaining_cities_set)  # Convert to list
            
            # Guard against small remaining_cities_list
            if len(remaining_cities_list) <= 1:
                new_h_n = 0  # No remaining cities, so MST cost is 0
            else:
                new_h_n = mst_cost(remaining_cities_list)  # Pass as list, which can be indexed
            
            # Calculate f(n) = g(n) + h(n)
            new_f_n = new_g_n + new_h_n
            
            # Only add the new state to the queue if it's better than the previously visited one
            if new_state not in visited or new_g_n < visited[new_state]:
                visited[new_state] = new_g_n
                heapq.heappush(pq, (new_f_n, new_g_n, new_state))

# Measure the execution time
start_time = time.time()
# Run the A* TSP solver
tour, cost = a_star_tsp()
end_time = time.time()
elapsed_time = end_time - start_time
print("Optimal tour:", ' -> '.join(tour))
print("Total cost:", cost)
print(f"Elapsed time: {elapsed_time} seconds")
