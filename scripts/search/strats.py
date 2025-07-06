from heapq import *
from typing import Any, Callable, Self
from search import Problem, ProblemSpace, SearchStrategy


class Step:
    def __init__(self, state: Any, action: str=None, prev: Self=None, cost: int=1):
        self.state = state
        self.action = action
        self.prev = prev
        self.depth = (prev.depth if prev else 0) + 1
        self.acc_cost = (prev.acc_cost if prev else 0) + cost


class BreadthFirstSearch(SearchStrategy):
    """
    Implements a depth first search strategy
    """
    def search(self, space: ProblemSpace, problem: Problem):
        queue = [Step(problem.init_state())]
        
        while 0 < len(queue):
            step = queue.pop(0)
            if problem.is_goal(step.state): return step
            for action, state in space.successors(step.state):
                queue.append(Step(state, action, step))
            
        return None


class DepthLimitedSearch(SearchStrategy):
    """
    Implements a depth limited search strategy
    - correct
    """
    
    def __init__(self, depth_limit, deepening_rate=2, max_iter=float('inf')):
        self.depth_limit = depth_limit
        self.max_iter = max_iter
        self.deepening_rate = deepening_rate
        
        
    def search(self, space: ProblemSpace, problem: Problem):
        stack = [Step(problem.init_state())]
        limit = self.depth_limit
        i = 0
        while (i := i+1) <= self.max_iter:
            while 0 < len(stack):
                step = stack.pop()
                if problem.is_goal(step.state): return step
                if limit <= step.depth: continue                
                for action, state in space.successors(step.state):
                    stack.append(Step(state, action, step))
            limit *= self.deepening_rate
        return None
    

class BoundedSearch(SearchStrategy):
    """
    Implements a branch and bound search strategy
    """
    def __init__(self, prune: Callable[[Any, Any], bool]):
        self.prune = prune

    def search(self, space: ProblemSpace, problem: Problem):
        queue = [Step(problem.init_state())]
        
        while 0 < len(queue):
            step = queue.pop(0)
            if problem.is_goal(step.state): return step
            
            for action, state in space.successors(step.state):
                if self.prune(step.state, action): continue
                queue.append(Step(state, action, step))

        return None


class AStarSearch(SearchStrategy):
    
    def __init__(self, heuristic: Callable[[Any], float]):
        self.heuristic = heuristic
    

    """
    Implement an a-star search strategy
    """
    def search(self, space: ProblemSpace, problem: Problem):
        heap = []
        heappush(heap, Step(Transition('init', problem.init_state())))
        
        while 0 < len(heap):
            step = heappop(heap)
            if problem.is_goal(step.succ.state): return step
            
            
        return None

class BiDirSearch(SearchStrategy):
    """
    Implements a bi-directional search strategy
    """
    def search(self, space: ProblemSpace, problem: Problem):
        pass