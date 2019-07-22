# main imports
import random

# module imports
from .Policy import Policy

class RandomPolicy(Policy):

    def apply(self, solution):  

        # TODO : implement for mutator (need two parameters)

        # choose updator randomly
        index = random.randint(0, len(self.updators) - 1)
        updator = self.updators[index]
        
        return solution.apply(updator)