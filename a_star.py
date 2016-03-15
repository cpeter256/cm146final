from heapq import heappop, heappush
from math import sqrt

def path_to(start_x, start_y, target_x, target_y, grid, avoid=False, los=None, state = None):
    initial_position = (start_x, start_y)
    destination = (target_x, target_y)
    

    distances = {initial_position: 0}           # Table of distances to cells 
    previous_cell = {initial_position: None}    # Back links from cells to predecessors
    queue = [(0, initial_position)]             # The heap/priority queue used

    # Initial distance for starting position
    distances[initial_position] = 0

    while queue:
        # Continue with next min unvisited node
        current_prio, current_node = heappop(queue)
        current_distance = distances[current_node]
        
        # Early termination check: if the destination is found, return the path
        if ((not avoid) and (current_node == destination)) or \
           (avoid and not los(current_node[0], current_node[1], destination[0], destination[1], state)):
            node = current_node
            path = []
            while node is not None:
                path.append(node)
                node = previous_cell[node]
            return path[::-1]
        
        # Calculate tentative distances to adjacent cells
        for adjacent_node, edge_cost in adj(grid, current_node):
            new_distance = current_distance + edge_cost

            if adjacent_node not in distances or new_distance < distances[adjacent_node]:
                # Assign new distance and update link to previous cell
                distances[adjacent_node] = new_distance
                previous_cell[adjacent_node] = current_node
                heuristic = 0
                if not avoid:
                    heuristic = sqrt(((adjacent_node[0]-target_x)**2) + ((adjacent_node[1]-target_y)**2))
                heappush(queue, (new_distance+heuristic, adjacent_node))
                    
    # Failed to find a path
    print("Failed to find a path from", initial_position, "to", destination)
    return None

def adj(grid, node):
    nodes = []
    x, y = node
    moves = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    for move in moves:
        if not grid[move[0]][move[1]]:
            nodes.append((move, 1))
    return nodes
