import random
from typing import Any, Self
from dnq import DNQ, dnq

class PairMergeSort(DNQ):

    def __init__(self, lst):
        self.lst = lst

    def is_basic(self):
        return len(self.lst) <= 1
    
    def base_fun(self):
        return self.lst
    
    def decompose(self) -> list[Self]:
        m = int(len(self.lst) / 2)
        a = self.lst[:m]
        b = self.lst[m:]
        return [ PairMergeSort(a), PairMergeSort(b) ]
    
    def recombine(self, results):
        a, b = results
        i, j, k = 0, 0, 0

        while i < len(a) and j < len(b):
            if a[i] < b[j]:
                self.lst[k] = a[i]
                i += 1
            else:
                self.lst[k] = b[j]
                j += 1
            k += 1

        while i < len(a):
            self.lst[k] = a[i]
            i += 1
            k += 1

        while j < len(b):
            self.lst[k] = b[j]
            j += 1
            k += 1

        return self.lst


if __name__ == '__main__':
    
    lst = [i for i in range(0, 10)]
    random.shuffle(lst)
    problem = PairMergeSort(lst)
    
    print(lst)
    res = dnq(problem)
    print(res)
