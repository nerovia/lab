from typing import Any, Self
from abc import ABC, abstractmethod

class DNQ(ABC):

    @abstractmethod
    def is_basic(self) -> bool:
        pass

    @abstractmethod
    def base_fun(self) -> Any:
        pass

    @abstractmethod
    def decompose(self) -> list[Self]:
        pass

    @abstractmethod
    def recombine(results: list[Any]) -> Any:
        pass


def dnq(problem: DNQ):
    if problem.is_basic():
        return problem.base_fun()
    sub_problems = problem.decompose()
    results = list(map(dnq, sub_problems))
    return problem.recombine(results)
