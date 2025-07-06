from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable


class InvalidAction(Exception):
    def __init__(self, action):
        super().__init__('invalid transition action', action)
        

class InvalidTransition(Exception):
    def __init__(self, state, action):
        super().__init__('invalid transition', state, action)


class ProblemSpace(ABC):
    """
    Describes the set of all states that the problem can assume.
    """
    @abstractmethod
    def successors(self, state) -> Iterable[tuple[Any, Any]]:
        pass
    
    @abstractmethod
    def precursors(slef, state) -> Iterable[tuple[Any, Any]]:
        pass
        

class Problem(ABC):
    """
    Describes a problem over the problem space.
    (Finding a path from the inital state to a goal state)
    """
    @abstractmethod
    def init_state(self) -> Any:
        """Returns the initial state"""
        pass
    
    @abstractmethod
    def goal_states(self) -> Iterable[Any]:
        """
        Iterates over all goal states or raises an excaption if that's too complicated.
        This is for bidirectional strategies.
        """
        pass
    
    @abstractmethod
    def is_goal(self, state) -> bool:
        """
        Checks whether a given state is a goal state.
        This is for efficiently checking states.
        """
        pass
        
        
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, space, problem):
        """
        Searches the state space (subset of the problem space) for a solution to the problem
        """
        pass
    
    
class Agent:
    def __init__(
        strategy: SearchStrategy,
        
    ):
        pass