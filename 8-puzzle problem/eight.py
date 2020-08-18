import copy
import time

initial_matrix = [[1, 3, 4], [8, 6, 2], [7, 0, 5]]
final_matrix = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

# initial_matrix = [[2, 8, 1], [0, 4, 3], [7, 6, 5]]
# initial_matrix = [[5, 6, 7], [4, 0, 8], [3, 2, 1]]


def heuristic(node):
    return manhattanDist_heur(node)


def move(node, i, j, x, y):
    new_matrix = copy.deepcopy(node.matrix)
    new_matrix[i][j] = new_matrix[i + x][j + y]
    new_matrix[i + x][j + y] = 0
    return Node(new_matrix, node.depth + 1, node)


class Node:
    def __init__(self, matrix, depth=None, parent=None):
        self.matrix = matrix
        self.depth = depth
        self.parent = parent

        for i in range(3):
            for j in range(3):
                if self.matrix[i][j] == 0:
                    self.blank_tile = (i, j)

        self.numbers_string = ""
        for i in range(3):
            for j in range(3):
                self.numbers_string += str(matrix[i][j])

    def next_movements(self):
        children = []
        i, j = self.blank_tile
        if i < 2:
            child = move(self, i, j, +1, 0)
            children.append(child)
        if i > 0:
            child = move(self, i, j, -1, 0)
            children.append(child)
        if j < 2:
            child = move(self, i, j, 0, +1)
            children.append(child)
        if j > 0:
            child = move(self, i, j, 0, -1)
            children.append(child)
        return children


class Result:
    def __init__(self, node, memory_needed, number_nodes_visited):
        self.node = node
        self.memory_needed = memory_needed
        self.number_nodes_visited = number_nodes_visited

    def update(self, other):
        self.node = other.node
        self.memory_needed = max(self.memory_needed, other.memory_needed)
        self.number_nodes_visited += other.number_nodes_visited


def final_pos(node):
    finalpos = {}
    for i in range(3):
        for j in range(3):
            finalpos[node.matrix[i][j]] = (i, j)
    return finalpos


def dfs_queue(nodes_list, new_nodes, depth=None):
    new_nodes.extend(nodes_list)
    return new_nodes


def bfs_queue(nodes_list, new_nodes, depth=None):
    nodes_list.extend(new_nodes)
    return nodes_list


def ids_queue(nodes_list, new_nodes, depth):
    if (new_nodes[0].depth <= depth):
        new_nodes.extend(nodes_list)
        return new_nodes
    return nodes_list


def greedy_queue(nodes_list, new_nodes, depth=None):
    nodes_list.extend(new_nodes)
    nodes_list = sorted(nodes_list, key=eval_func_greedy)
    return nodes_list


def astar_queque(nodes_list, new_nodes, depth=None):
    nodes_list.extend(new_nodes)
    nodes_list = sorted(nodes_list, key=eval_func_astar)
    return nodes_list


def idastar_queque(nodes_list, new_nodes, depth=None):
    if (new_nodes[0].depth <= depth):
        nodes_list.extend(new_nodes)
    nodes_list = sorted(nodes_list, key=eval_func_astar)
    return nodes_list


def manhattanDist_heur(node):
    cost = 0
    for i in range(3):
        for j in range(3):
            i_final, j_final = finalpos_map[node.matrix[i][j]]
            cost += abs(i_final - i) + (j_final - j)
    return cost


def outOfPlace_heur(node):
    cost = 0
    for i in range(3):
        for j in range(3):
            if (i, j) != finalpos_map[node.matrix[i][j]]:
                cost += 1
    return cost


def eval_func_greedy(node):
    return heuristic(node)


def eval_func_astar(node):
    return heuristic(node) + node.depth


def search(initial_node, queue, depth=None):
    memory_needed = 1
    number_nodes_visited = 0
    nodes_list = [initial_node]
    nodes_visited = set()
    while nodes_list:
        node = nodes_list.pop(0)
        if node.numbers_string in nodes_visited:
            continue
        nodes_visited.add(node.numbers_string)
        if node.matrix == final_node.matrix:
            print("goal found")
            return Result(node, memory_needed, number_nodes_visited)
        next_nodes = node.next_movements()
        nodes_list = queue(nodes_list, next_nodes, depth)
        memory_needed = max(memory_needed, len(nodes_list))
        number_nodes_visited += 1
    print("goal not found")
    return Result(None, memory_needed, number_nodes_visited)


def dfs(initial_node):
    return search(initial_node, dfs_queue)


def bfs(initial_node):
    return search(initial_node, bfs_queue)


def ids(initial_node, max_depth):
    result = Result(None, 0, 0)
    for depth in range(max_depth + 1):
        temp_result = search(initial_node, ids_queue, depth)
        result.update(temp_result)
        if result.node:
            break
    return result


def greedy(initial_node):
    return search(initial_node, greedy_queue)


def astar(initial_node):
    return search(initial_node, astar_queque)


def idastar(initial_node, max_depth):
    result = Result(None, 0, 0)
    for depth in range(max_depth + 1):
        temp_result = search(initial_node, idastar_queque, depth)
        result.update(temp_result)
        if result.node:
            break
    return result


def print_path(node, path):
    while node != None and node.parent != None:
        i, j = node.blank_tile
        ip, jp = node.parent.blank_tile
        if i == ip + 1:
            path.append("DOWN")
        elif i == ip - 1:
            path.append("UP")
        elif j == jp + 1:
            path.append("RIGHT")
        else:
            path.append("LEFT")
        node = node.parent
    path.reverse()


final_node = Node(final_matrix)
finalpos_map = final_pos(final_node)
initial_node = Node(initial_matrix, 0)


# dfs
print("dfs:")
begin = time.time()
result = dfs(initial_node)
end = time.time()
time_needed = end - begin
print("memory needed:", result.memory_needed)
print("nodes visited:", result.number_nodes_visited)
print("time needed:", time_needed)
path = []
print_path(result.node, path)
print("path:", path)
print()

# bfs
print("bfs:")
begin = time.time()
result = bfs(initial_node)
end = time.time()
time_needed = end - begin
print("memory needed:", result.memory_needed)
print("nodes visited:", result.number_nodes_visited)
print("time needed:", time_needed)
path = []
print_path(result.node, path)
print("path:", path)
print()

# ids
depth_ids = 50
print("ids:")
begin = time.time()
result = ids(initial_node, depth_ids)
end = time.time()
time_needed = end - begin
print("memory needed:", result.memory_needed)
print("nodes visited:", result.number_nodes_visited)
print("time needed:", time_needed)
path = []
print_path(result.node, path)
print("path:", path)
print()

# greedy
print("greedy:")
begin = time.time()
result = greedy(initial_node)
end = time.time()
time_needed = end - begin
print("memory needed:", result.memory_needed)
print("nodes visited:", result.number_nodes_visited)
print("time needed:", time_needed)
path = []
print_path(result.node, path)
print("path:", path)
print()

# astar
print("astar:")
begin = time.time()
result = astar(initial_node)
end = time.time()
time_needed = end - begin
print("memory needed:", result.memory_needed)
print("nodes visited:", result.number_nodes_visited)
print("time needed:", time_needed)
path = []
print_path(result.node, path)
print("path:", path)
print()

# idastar
depth_ids = 50
print("idastar:")
begin = time.time()
result = idastar(initial_node, depth_ids)
end = time.time()
time_needed = end - begin
print("memory needed:", result.memory_needed)
print("nodes visited:", result.number_nodes_visited)
print("time needed:", time_needed)
path = []
print_path(result.node, path)
print("path:", path)
print()
