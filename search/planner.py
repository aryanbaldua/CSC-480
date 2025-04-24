import sys
import heapq

# Directions: (delta_row, delta_col, action)
directions = [(-1, 0, 'N'), (1, 0, 'S'), (0, -1, 'W'), (0, 1, 'E')]


# input file reading
def read_world(filename):
    with open(filename, 'r') as f:
        cols = int(f.readline())
        rows = int(f.readline())
        world = [list(f.readline().strip()) for _ in range(rows)]

    start = None
    dirty = []
    for r in range(rows):
        for c in range(cols):
            if world[r][c] == '@':
                start = (r, c)
            elif world[r][c] == '*':
                dirty.append((r, c))
    return world, start, dirty


# ensure move is allowed
def is_valid(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] != '#'


# dfs implementation
def depth_first_search(grid, start, dirt_cell):
    stack = [(start, tuple(dirt_cell), [])]
    visited = set()
    nodes_generated = 0
    nodes_expanded = 0

    # print(f" Starting DFS from {start} with dirt at: {dirt_cell}")

    while stack:
        pos, remaining, path = stack.pop()
        state = (pos, remaining)
        if state in visited:
            continue
        visited.add(state)
        nodes_expanded += 1

    # print(f" Visiting {pos}, Remaining dirt: {remaining}")

        if pos in remaining:
            remaining = tuple(d for d in remaining if d != pos)
            path = path + ['V']

        if not remaining:
            # print(" All dirt cleaned. Return path.")
            return path, nodes_generated, nodes_expanded

        for dr, dc, action in directions:
            nr, nc = pos[0] + dr, pos[1] + dc
            if is_valid(grid, nr, nc):
                new_state = ((nr, nc), remaining, path + [action])
                stack.append(new_state)
                nodes_generated += 1
    return [], nodes_generated, nodes_expanded


# ucs implementation
def uniform_cost_search(grid, start, dirt_cell):
    heap = [(0, start, tuple(dirt_cell), [])]
    visited = set()
    nodes_generated = 0
    nodes_expanded = 0

    # print(f" Starting UCS from {start} with dirt at: {dirt_cell}")

    while heap:
        cost, pos, remaining, path = heapq.heappop(heap)
        state = (pos, remaining)
        if state in visited:
            # print(f"Already visited: {state}")
            continue
        visited.add(state)
        nodes_expanded += 1

        if pos in remaining:
            remaining = tuple(d for d in remaining if d != pos)
            path = path + ['V']

        if not remaining:
            return path, nodes_generated, nodes_expanded

        for dr, dc, action in directions:
            nr, nc = pos[0] + dr, pos[1] + dc
            if is_valid(grid, nr, nc):
                new_path = path + [action]
                heapq.heappush(heap, (cost + 1, (nr, nc), remaining, new_path))
                nodes_generated += 1
    # print("No path found")
    return [], nodes_generated, nodes_expanded


# Main entry point
def main():
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py [uniform-cost|depth-first] [world-file.txt]")
        sys.exit(1)

    algorithm = sys.argv[1]
    filename = sys.argv[2]

    grid, start, dirt = read_world(filename)

    if algorithm == "depth-first":
        actions, nodes_gen, nodes_exp = depth_first_search(grid, start, dirt)
    elif algorithm == "uniform-cost":
        actions, nodes_gen, nodes_exp = uniform_cost_search(grid, start, dirt)
    else:
        print("Choose either depth-first or uniform-cost as searching algorithm", algorithm)
        sys.exit(1)

    for action in actions:
        print(action)

    print(f"{nodes_gen} nodes generated")
    print(f"{nodes_exp} nodes expanded")


if __name__ == "__main__":
    main()
