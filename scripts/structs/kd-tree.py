from dataclasses import dataclass

@dataclass
class Node:
    key: None
    left: None
    right: None
    value: None
    adj: None
    pass

def create_tree(lst):
    x_lst = lst
    y_lst = lst.copy()
    x_lst.sort(key=lambda it: it[0])
    y_lst.sort(key=lambda it: it[1])
    x_node = Node()
    y_node = Node()
    create_tree_rec(x_node, y_node, x_lst, lambda it: it[0])
    create_tree_rec(y_node, x_node, y_lst, lambda it: it[0])
    return x_node

def create_tree_rec(node, adj, lst, key):
    node.adj = adj
    if len(lst) == 1:
        node.value = lst[0]
        return
    m = int(len(lst) / 2)
    node.key = key(lst[m])
    node.left = Node()
    node.right = Node()
    create_tree_rec(node.left, adj, lst[:m], key)
    create_tree_rec(node.right, adj, lst[m:], key)


def print_tree(node, depth = 0):
    indent = ' ' * 4 * depth
    if hasattr(node, 'key'):
        print(indent, 'x' if depth % 2 == 0 else 'y', '<', node.key)
        print_tree(node.left, depth+1)
        print_tree(node.right, depth+1)
    else:
        print(indent, node.value)

if __name__ == "__main__":
    tree = create_tree([(1, 5), (2, 2), (4, 9), (7, 3), (8, 10), (9, 13)])
    print_tree(tree)