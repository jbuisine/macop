# main imports
from enum import Enum


# enumeration which stores kind of operator
class KindOperator(Enum):
    MUTATOR = 1
    CROSSOVER = 2


class Operator():
    def __init__(self):
        pass

    def apply(self, solution):
        """Apply the current operator transformation

        Args:
            solution (Solution): Solution instance

        Raises:
            NotImplementedError: if method not implemented into child class
        """
        raise NotImplementedError

    def setAlgo(self, algo):
        """Keep into operator reference of the whole algorithm
           The reason is to better manage operator instance

        Args:
            algo (Algorithm): the algorithm reference runned
        """
        self.algo = algo
