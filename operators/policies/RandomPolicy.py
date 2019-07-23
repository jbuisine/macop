# main imports
import random

# module imports
from .Policy import Policy

class RandomPolicy(Policy):

    def select(self):  

        # choose operator randomly
        index = random.randint(0, len(self.operators) - 1)
        return self.operators[index]


        