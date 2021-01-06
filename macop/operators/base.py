"""Abstract Operator classes
"""
# main imports
from enum import Enum
from abc import abstractmethod


class KindOperator(Enum):
    """Enum in order to recognize kind of operators
    """
    MUTATOR = 1
    CROSSOVER = 2


class Operator():
    """Abstract Operator class which enables to update solution applying operator (computation)
    """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def apply(self, solution):
        """Apply the current operator transformation

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


class Mutation(Operator):
    """Abstract Mutation extend from Operator

    Attributes:
        kind: {KindOperator} -- specify the kind of operator
    """
    def __init__(self):
        self._kind = KindOperator.MUTATOR

    def apply(self, solution):
        raise NotImplementedError



class Crossover(Operator):
    """Abstract crossover extend from Operator

    Attributes:
        kind: {KindOperator} -- specify the kind of operator
    """
    def __init__(self):
        self._kind = KindOperator.CROSSOVER

    def apply(self, solution1, solution2=None):
        raise NotImplementedError