


from dataclasses import dataclass
from search import Problem, ProblemSpace


@dataclass
class QueenState:
    queens: tuple[int]


class QueenSpace(ProblemSpace):
    def __init__(self, board_size: int):
        self.board_size = board_size
    
    def successor(state: QueenState):
        for i in state.queens:
            return 

class QueenProblem(Problem):
    def __init__(self, space: QueenSpace, init_state: QueenState):
        self.space = QueenSpace
        self._init_state = init_state
    
    def init_state(self): return self._init_state
    
    def goal_states(self):
        raise 'help'
    
    def is_goal(state):
        return super().is_goal()



        