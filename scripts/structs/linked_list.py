class Node:
    def __init__(self, item, nxt=None):
        self.item = item
        self.nxt = nxt
        

def visit(node):
    if node is None:
        print()
        return 
    print(node.item, end=' ')
    visit(node.nxt)


def reverse(cur):
    # nxt <- cur.nxt <- None
    nxt, cur.nxt = cur.nxt, None  # get next and delete it
    while nxt is not None:
        # nxt.nxt <- cur <- nxt <- nxt.nxt
        nxt.nxt, cur, nxt = cur, nxt, nxt.nxt
    return cur


if __name__ == '__main__':
    llst = Node('a', Node('b', Node('c', Node('d', Node('e')))))
    visit(llst)
    visit(reverse(llst))