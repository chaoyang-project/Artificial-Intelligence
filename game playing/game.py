import sys

case = "((4 (7 9 8) 8) (((3 6 4) 2 6) ((9 2 9) 4 7 (6 4 5))))"
# case = "(((1 4) (3 (5 2 8 0) 7 (5 7 1)) (8 3)) (((3 6 4) 2 (9 3 0)) ((8 1 9) 8 (3 4 ))))"
# case = "(5 (((4 7 -2) 7) 6))"
# case = "((8 (7 9 8) 4) (((3 6 4) 2 1) ((6 2 9) 4 7 (6 4 5))))"
# case = "(((1(4 7)) (3 ((5 2) (2 8 9) 0 -2) 7 (5 7 1)) (8 3)) (((8 (9 3 2) 5) 2 (9 (3 2) 0)) ((3 1 9) 8 (3 4))))"


def tree_to_list(root_node, list):
    if root_node.children == None:
        list.append(str(root_node.value))
        return
    list.append('(')
    for child in root_node.children:
        tree_to_list(child, list)
    list.append(')')


def list_to_tree(list):
    tree_string = []
    nums = "0123456789"
    i = 0
    while i < len(list):
        char = list[i]
        if char == '(':
            tree_string.append(char)
        if char == ')':
            tree_string.append(build_node(tree_string))
        if char == '-':
            sign = char
            j = i + 1
            number = ""
            while list[j] in nums:
                number += list[j]
                j += 1
            i = j - 1
            number = sign + number
            node = Node(int(number))
            tree_string.append(node)
        if char in nums:
            number = char
            j = i + 1
            while list[j] in nums:
                number += list[j]
                j += 1
            i = j - 1
            node = Node(int(number))
            tree_string.append(node)
        i += 1
    return tree_string.pop()


def format_cut(node):
    list = []
    tree_to_list(node, list)
    list1 = " ".join(list)
    return list1


class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children


def build_node(tree_string):
    nodes_list = []
    char = tree_string.pop()
    while char != '(':
        nodes_list.append(char)
        char = tree_string.pop()
    nodes_list.reverse()
    return Node(0, nodes_list)


def min_value(root_node, alpha=None, beta=None):
    if root_node.children == None:
        return root_node.value
    value = sys.maxsize
    for node in root_node.children:
        value = min(value, max_value(node, alpha, beta))
        if alpha != None:
            if value <= alpha:
                list1 = format_cut(node)
                list2 = format_cut(root_node)
                print("min cut after ", list1, " in subtree ", list2)
                return value
            beta = min(beta, value)
    root_node.value = value
    return value


def max_value(root_node, alpha=None, beta=None):
    if root_node.children == None:
        return root_node.value
    value = (-1)*sys.maxsize
    for node in root_node.children:
        value = max(value, min_value(node, alpha, beta))
        if alpha != None:
            if value >= beta:
                list1 = format_cut(node)
                list2 = format_cut(root_node)
                print("max cut after ", list1, " in subtree ", list2)
                return value
            alpha = max(alpha, value)
    root_node.value = value
    return value


def minimax(root_node):
    return max_value(root_node)


def alpha_beta(root_node):
    return max_value(root_node, (-1) * sys.maxsize, sys.maxsize)


def print_path(root_node, list):
    if root_node.children == None:
        return
    number = 0
    for node in root_node.children:
        number += 1
        if node.value == root_node.value:
            list.append(number)
            print_path(node, list)


if __name__ == '__main__':

# MINIMAX
    tree = list_to_tree(case)
    print("MINIMAX:")
    minimax_value = minimax(tree)
    print("maximum value : ", minimax_value)
    list = []
    print_path(tree, list)
    print("path : ", list)
    print()
# ALPHA-BETA
    print("ALPHA-BETA:")
    alpha_beta_value = alpha_beta(tree)
    print("maximum value : ", alpha_beta_value)
