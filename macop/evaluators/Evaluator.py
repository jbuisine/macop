"""Abstract Evaluator class
"""
# main imports
from abc import abstractmethod


class Evaluator():
    """Abstract Operator class which enables to update solution applying operator (computation)
    """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def apply(self, solution):
        """Apply the computation of fitness from solution

        Args:
            solution: {Solution} -- Solution instance
        """
        pass

    def setAlgo(self, algo):
        """Keep into operator reference of the whole algorithm
           The reason is to better manage operator instance

        Args:
            algo: {Algorithm} -- the algorithm reference runned
        """
        self._algo = algo
