"""Abstract classes for Operator Selection Strategy
"""
import logging
from abc import abstractmethod

from macop.operators.base import KindOperator


# define policy to choose `operator` function at current iteration
class Policy():
    """Abstract class which is used for applying strategy when selecting and applying operator 

    Attributes:
        operators: {[:class:`~macop.operators.base.Operator`]} -- list of selected operators for the algorithm
    """
    def __init__(self, operators):
        """Initialise new Policy instance using specific list of operators

        Args:
            operators: [{}] -- list of operators to use
        """
        self.operators = operators

    @abstractmethod
    def select(self):
        """
        Select specific operator

        Returns:
            {:class:`~macop.operators.base.Operator`}: selected operator
        """
        pass

    def apply(self, solution1, solution2=None):
        """
        Apply specific operator chosen to create new solution, compute its fitness and return solution
        
        Args:
            solution1: {:class:`~macop.solutions.base.Solution`} -- the first solution to use for generating new solution
            solution2: {:class:`~macop.solutions.base.Solution`} -- the second solution to use for generating new solution (in case of specific crossover, default is best solution from algorithm)

        Returns:
            {:class:`~macop.solutions.base.Solution`}: new generated solution
        """

        operator = self.select()

        logging.info("---- Applying %s on %s" %
                     (type(operator).__name__, solution1))

        # default value of solution2 is current best solution
        if solution2 is None and self.algo is not None:
            solution2 = self.algo.result

        # avoid use of crossover if only one solution is passed
        if solution2 is None and operator._kind == KindOperator.CROSSOVER:

            while operator._kind == KindOperator.CROSSOVER:
                operator = self.select()

        # apply operator on solution
        if operator._kind == KindOperator.CROSSOVER:
            newSolution = operator.apply(solution1, solution2)
        else:
            newSolution = operator.apply(solution1)

        logging.info("---- Obtaining %s" % (newSolution))

        return newSolution

    def setAlgo(self, algo):
        """Keep into policy reference of the whole algorithm
           The reason is to better manage the operator choices (use of rewards as example)

        Args:
            algo: {:class:`~macop.algorithms.base.Algorithm`} -- the algorithm reference runned
        """
        self.algo = algo
