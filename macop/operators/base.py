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
        """Abstract Operator initialiser
        """
        pass

    @abstractmethod
    def apply(self, solution):
        """Apply the current operator transformation

        Args:
            solution: {:class:`~macop.solutions.base.Solution`} -- Solution instance
        """
        pass

    def setAlgo(self, algo):
        """Keep into operator reference of the whole algorithm
           The reason is to better manage operator instance

        Args:
            algo: {:class:`~macop.algorithms.base.Algorithm`} -- the algorithm reference runned
        """
        self._algo = algo


class Mutation(Operator):
    """Abstract Mutation extend from Operator

    Attributes:
        kind: {:class:`~macop.operators.base.KindOperator`} -- specify the kind of operator
    """
    def __init__(self):
        """Mutation initialiser in order to specify kind of Operator
        """
        self._kind = KindOperator.MUTATOR

    def apply(self, solution):
        """Apply mutation over solution in order to obtained new solution

        Args:
            solution: {:class:`~macop.solutions.base.Solution`} -- solution to use in order to create new solution

        Return:
            {:class:`~macop.solutions.base.Solution`} -- new generated solution
        """
        raise NotImplementedError


class Crossover(Operator):
    """Abstract crossover extend from Operator

    Attributes:
        kind: {:class:`~macop.operators.base.KindOperator`} -- specify the kind of operator
    """
    def __init__(self):
        """Crossover initialiser in order to specify kind of Operator
        """
        self._kind = KindOperator.CROSSOVER

    def apply(self, solution1, solution2=None):
        """Apply crossover using two solutions in order to obtained new solution

        Args:
            solution1: {:class:`~macop.solutions.base.Solution`} -- the first solution to use for generating new solution
            solution2: {:class:`~macop.solutions.base.Solution`} -- the second solution to use for generating new solution

        Return:
            {:class:`~macop.solutions.base.Solution`} -- new generated solution
        """
        raise NotImplementedError
