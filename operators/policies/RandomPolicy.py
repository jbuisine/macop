# main imports
import random

# module imports
from ..Operator import Operator
from .Policy import Policy

class RandomPolicy(Policy):

    def apply(self, solution, secondSolution=None):  

        # choose operator randomly
        index = random.randint(0, len(self.operators) - 1)
        operator = self.operators[index]

        # check kind of operator
        if operator.kind == Operator.CROSSOVER:
            return operator.apply(solution, secondSolution)
        
        if operator.kind == Operator.MUTATOR:
            return operator.apply(solution)

        # by default
        return operator.apply(solution)