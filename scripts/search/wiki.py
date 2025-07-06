from typing import Iterator
from search import Problem, ProblemSpace
import wikipediaapi


class WikiSpace(ProblemSpace):
    def successors(self, state) -> Iterator[tuple[str, str]]:
        return super().successors(state) 
    
    def precursors(slef, state):
        raise NotImplementedError()
    
class WikiProblem(Problem):
    def __init__(self, init_url, goal_url):
        self.init_url = init_url
        self.goal_url = goal_url
        
    def init_state(self): return self.init_url
    
    def is_goal(self, state): return state == self.goal_url
    
    def goal_states(self): yield self.goal_url
    
    
if __name__ == '__main__':
    wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')

    page_py = wiki.page('Python_(programming_language)')
    page_py.backlinks[0].  