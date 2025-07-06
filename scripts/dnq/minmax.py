import random
from dnq import DNQ, dnq

class MinMax(DNQ):

    def __init__(self, lst: list[int]):
        self.lst = lst

    def is_basic(self):
        return len(self.lst) <= 3
    
    def base_fun(self):
        n = len(self.lst)
        minimum = self.lst[0]
        maximum = self.lst[0]
        for i in range(1, n):
            minimum = min(minimum, self.lst[i])
            maximum = max(maximum, self.lst[i])
        return minimum, maximum
    
    def decompose(self):
        m = int(len(self.lst) / 2)
        a = MinMax(self.lst[:m])
        b = MinMax(self.lst[m:])
        return a, b

    def recombine(self, results):
        minimum = min(results[0][0], results[1][0])
        maximum = max(results[0][1], results[1][1])
        return minimum, maximum


if __name__ == '__main__':
    
    lst = [i for i in range(0, 10)]
    random.shuffle(lst)
    problem = MinMax(lst)
    
    print(lst)
    res = dnq(problem)
    print(res)
