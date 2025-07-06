from heapq import *
from dataclasses import dataclass, field
from typing import Any, Self

@dataclass()
class LeafNode:
    item: chr

@dataclass()
class BinaryNode:
    left: Self | LeafNode
    right: Self | LeafNode


@dataclass(order=True)
class PrioItem:
    prio: int
    item: Any=field(compare=False)

def huff_tree(s: str) -> BinaryNode | LeafNode:

    # count frequencies    
    f = { }
    for c in s:
        if c in f: f[c] += 1
        else: f[c] = 1

    print(sorted(f))

    # initialize heap
    q = []
    for c in f: heappush(q, PrioItem(f[c], LeafNode(c)))

    print(q)

    while len(q) > 1:
        l = heappop(q)
        r = heappop(q)
        heappush(q, PrioItem(l.prio+r.prio, BinaryNode(l.item, r.item)))
        
    return heappop(q).item


def huff_table(node: BinaryNode | LeafNode, code: str=''):
    if type(node) is BinaryNode:
        l = huff_table(node.left, code + '0')
        r = huff_table(node.right, code + '1')
        return l | r
    if type(node) is LeafNode:
        return { node.item: code }


def huff_enc(s: str) -> str:
    t = huff_tree(s)
    l = huff_table(t)
    e = ''
    for c in s: e += l[c]
    return l, e





if __name__ == '__main__':

    s = 'a fast runner need never be afraid of the dark'
    A = {
        ' ': '00',
        'a': '010',   
        'b': '10110', 
        'd': '1010', 
        'e': '100',   
        'f': '1100',  
        'h': '110111',
        'i': '111000',
        'k': '111001',
        'n': '1101',  
        'o': '111010',
        'r': '011',   
        's': '111011',
        't': '11110', 
        'u': '111110',
        'v': '111111',
    }

    l, e = huff_enc('a fast runner need never be afraid of the dark')
    print(l, e)