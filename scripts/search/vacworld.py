from dataclasses import dataclass
from typing import Any, Callable, Iterable
from strats import AStarSearch, BoundedSearch, BreadthFirstSearch, DepthLimitedSearch, Step
from search import InvalidAction, InvalidTransition, Problem, ProblemSpace


@dataclass
class VacState:
    pos: int
    dust: tuple[bool]


class VacSpace(ProblemSpace):

    def successors(self, state: VacState) -> Iterable[tuple[str, VacState]]:
        yield 'suck', VacState(state.pos, tuple(False if state.pos == idx else x for idx, x in enumerate(state.dust)))
        if 0 < state.pos:
            yield 'left', VacState(state.pos-1, state.dust)
        if state.pos < len(state.dust) - 1:
            yield 'right', VacState(state.pos+1, state.dust)
            
    def precursors(self, state: VacState) -> Iterable[tuple[str, VacState]]:
        if not state.dust[state.pos]:
            yield 'suck', VacState(state.pos, tuple(True if state.pos == idx else x for idx, x in enumerate(state.dust)))
            yield 'suck', state
        if 0 < state.pos-1:
            yield 'right', VacState(state.pos-1, state.dust)
        if state.pos+1 < len(state.dust) - 1:
            yield 'left', VacState(state.pos+1, state.dust)


class VacProblem(Problem):
    def __init__(self, init_state):
        self._init_state = init_state
        self.world_size = len(init_state.dust)

    def init_state(self): return self._init_state
    
    def goal_states(self):
        dust = (False,) * self.world_size
        return (VacState(i, dust) for i in range(self.world_size))
        
    def is_goal(self, state: VacState) -> bool:
        return not any(state.dust)
    
        


if __name__ == '__main__':

    def prune(state: VacState, action: str):
        pos, dust = state.pos, state.dust
        match action:
            case 'suck':
                if not dust[pos]: return True  # don't suck twice
            case 'left':
                if dust[pos]: return True  # don't ignore
            case 'right':
                if dust[pos]: return True  # don't ignore
        return False
        
        
    def visit(step: Step):
        if step == None:
            return
        visit(step.prev)
        print(step.action, step.state)


    n = 10

    space = VacSpace()
    problem = VacProblem(VacState(n//2, (True,)*n))
    # strategy = BreadthFirstSearch()  # n < 6
    # strategy = DepthLimitedSearch(10, 100)  # n < 5 
    strategy = BoundedSearch(prune)  # n < 11
    # strategy = AStarSearch()
    path = strategy.search(space, problem)
    
    visit(path)
    
        
    
 