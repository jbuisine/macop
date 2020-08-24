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
    def __init__(self, _operators):
        self.operators = _operators

    @abstractmethod
    def select(self):
        """
        Select specific operator

        Returns:
            {Operator} -- selected operator
        """
        pass

    def apply(self, _solution):
        """
        Apply specific operator chosen to create new solution, computes its fitness and returns solution
        
        Args:
            _solution: {Solution} -- the solution to use for generating new solution

        Returns:
            {Solution} -- new generated solution
        """

        operator = self.select()

        logging.info("---- Applying %s on %s" %
                     (type(operator).__name__, _solution))

        # apply operator on solution
        newSolution = operator.apply(_solution)

        # compute fitness of new solution
        newSolution.evaluate(self.algo.evaluator)

        logging.info("---- Obtaining %s" % (_solution))

        return newSolution

    def setAlgo(self, _algo):
        """Keep into policy reference of the whole algorithm
           The reason is to better manage the operator choices (use of rewards as example)

        Args:
            _algo: {Algorithm} -- the algorithm reference runned
        """
        self.algo = _algo
