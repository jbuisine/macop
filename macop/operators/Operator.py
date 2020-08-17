"""Abstract Operator class
"""
# main imports
from enum import Enum


# enumeration which stores kind of operator
class KindOperator(Enum):
    """Enum in order to recognize kind of operators
    """
    MUTATOR = 1
    CROSSOVER = 2


class Operator():
    """Abstract Operator class which enables to update solution applying operator (computation)
    """
    def __init__(self):
        pass

    def apply(self, _solution):
        """Apply the current operator transformation

        Args:
            _solution: {Solution} -- Solution instance

        Raises:
            NotImplementedError: if method not implemented into child class
        """
        raise NotImplementedError

    def setAlgo(self, _algo):
        """Keep into operator reference of the whole algorithm
           The reason is to better manage operator instance

        Args:
            _algo: {Algorithm} -- the algorithm reference runned
        """
        self.algo = _algo
