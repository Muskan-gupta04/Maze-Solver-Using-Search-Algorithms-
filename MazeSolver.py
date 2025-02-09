import matplotlib.pyplot as plt
from queue import PriorityQueue, Queue

# Maze definition (0 = free space, 1 = obstacle)
maze = [
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (5, 5)


def visualize_path(maze, path):
    """Visualize the maze and the solution path."""
    maze_copy = [[1 if maze[i][j] == 1 else 0 for j in range(len(maze[0]))] for i in range(len(maze))]
    
    for (x, y) in path:
        maze_copy[x][y] = 0.5  # Mark path
    
    plt.imshow(maze_copy, cmap='ocean')
    plt.show()


def get_adjNodes(maze, state):
    """Get valid adjacent nodes for the current state."""
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    adjNodes = []
    x, y = state
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0:
            adjNodes.append((nx, ny))
    
    return adjNodes


def bfs(maze, start, goal):
    """Breadth-First Search."""
    queue = Queue()
    queue.put((start, [start]))
    vis = set()

    while not queue.empty():
        node, path = queue.get()

        if node == goal:
            return path

        if node in vis:
            continue

        vis.add(node)

        for adj_node in get_adjNodes(maze, node):
            queue.put((adj_node, path + [adj_node]))

    return None


def dfs(maze, start, goal):
    """Depth-First Search."""
    stack = [(start, [start])]
    vis = set()

    while stack:
        node, path = stack.pop()

        if node == goal:
            return path

        if node in vis:
            continue

        vis.add(node)

        for adj_node in get_adjNodes(maze, node):
            stack.append((adj_node, path + [adj_node]))

    return None


def heuristic(state, goal):
    """Manhattan distance heuristic."""
    return abs(state[0] - goal[0]) + abs(state[1] - goal[1])


def a_star(maze, start, goal):
    """A* Search."""
    queue = PriorityQueue()
    queue.put((0, start, [start]))
    vis = set()

    while not queue.empty():
        cost, node, path = queue.get()

        if node == goal:
            return path

        if node in vis:
            continue

        vis.add(node)

        for adj_node in get_adjNodes(maze, node):
            new_cost = cost + 1
            queue.put((new_cost + heuristic(adj_node, goal), adj_node, path + [adj_node]))

    return None


def greedy_bfs(maze, start, goal):
    """Greedy Best-First Search."""
    queue = PriorityQueue()
    queue.put((heuristic(start, goal), start, [start]))
    vis = set()

    while not queue.empty():
        _, node, path = queue.get()

        if node == goal:
            return path

        if node in vis:
            continue

        vis.add(node)

        for adj_node in get_adjNodes(maze, node):
            queue.put((heuristic(adj_node, goal), adj_node, path + [adj_node]))

    return None


# User selection
print("Select the maze-solving algorithm:")
print("1. BFS (Breadth-First Search)")
print("2. DFS (Depth-First Search)")
print("3. A* Search")
print("4. Greedy Best-First Search")
choice = int(input("Enter your choice (1-4): "))

if choice == 1:
    print("Solving maze with BFS...")
    bfs_path = bfs(maze, start, goal)
    visualize_path(maze, bfs_path)
elif choice == 2:
    print("Solving maze with DFS...")
    dfs_path = dfs(maze, start, goal)
    visualize_path(maze, dfs_path)
elif choice == 3:
    print("Solving maze with A*...")
    astar_path = a_star(maze, start, goal)
    visualize_path(maze, astar_path)
elif choice == 4:
    print("Solving maze with Greedy Best-First Search...")
    greedy_path = greedy_bfs(maze, start, goal)
    visualize_path(maze, greedy_path)
else:
    print("Invalid choice!")
