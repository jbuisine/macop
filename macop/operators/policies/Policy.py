"""Abstract class which is used for applying strategy when selecting and applying operator 
"""
import logging
from abc import abstractmethod


# define policy to choose `operator` function at current iteration
class Policy():
    """Abstract class which is used for applying strategy when selecting and applying operator 

    Attributes:
        operators: {[Operator]} -- list of selected operators for the algorithm
    """
    def __init__(self, operators):
        self._operators = operators

    @abstractmethod
    def select(self):
        """
        Select specific operator

        Returns:
            {Operator} -- selected operator
        """
        pass

    def apply(self, solution):
        """
        Apply specific operator chosen to create new solution, computes its fitness and returns solution
        
        Args:
            _solution: {Solution} -- the solution to use for generating new solution

        Returns:
            {Solution} -- new generated solution
        """

        operator = self.select()

        logging.info("---- Applying %s on %s" %
                     (type(operator).__name__, solution))

        # apply operator on solution
        newSolution = operator.apply(solution)

        logging.info("---- Obtaining %s" % (solution))

        return newSolution

    def setAlgo(self, algo):
        """Keep into policy reference of the whole algorithm
           The reason is to better manage the operator choices (use of rewards as example)

        Args:
            algo: {Algorithm} -- the algorithm reference runned
        """
        self._algo = algo
