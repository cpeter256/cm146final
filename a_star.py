from heapq import heappop, heappush

def path_to(start_x, start_y, target_x, target_y, grid):
    prio_q = []
    visited = set()
    distance = {}

    prev = {}

    initial_node = (start_x, start_y)
    destination = (target_x, target_y)
    distance[initial_node] = 0

    heappush(prio_q, initial_node)
    while len(prio_q) > 0:
        node = heappop(prio_q)
        if node in visited:
            continue

        if node == destination:
            path = []
            while node in prev:
                path.append(node)
                node = prev[node]
            path.append(node)
            path.reverse()
            return path

        neighbors = adj(node[0], node[1], grid)
        for n in neighbors:
            dist_through_node = distance[node]+1
            if n in distance:
                if dist_through_node < distance[n]:
                    distance[n] = dist_through_node
                    prev[n] = node
            else:
                distance[n] = dist_through_node
                prev[n] = node
            heappush(prio_q, n)
        visited.add(node)

    pass

def adj(x, y, grid):
    positions = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    valid = []
    for pos in positions:
        if not (grid[pos[0]][pos[1]]):
            valid.append(pos)
    return valid