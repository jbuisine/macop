"""Mutation implementations for continuous solution
"""
# main imports
import random
import sys
import numpy as np

# module imports
from macop.operators.base import Mutation

class PolynomialMutation(Mutation):
    """Polynomial Mutation implementation for continuous solution

    Attributes:
        kind: {:class:`~macop.operators.base.KindOperator`} -- specify the kind of operator

    Example:

    >>> # import of solution and polynomial mutation operator
    >>> from macop.solutions.continuous import ContinuousSolution
    >>> from macop.operators.continuous.mutators import PolynomialMutation
    >>> solution = ContinuousSolution.random(5, (-2, 2))
    >>> list(solution.data)
    [-0.50183952461055, 1.8028572256396647, 0.9279757672456204, 0.3946339367881464, -1.375925438230254]
    >>> mutator = PolynomialMutation(interval=(-2, 2))
    >>> mutation_solution = mutator.apply(solution)
    >>> list(mutation_solution.data)
    [-0.50183952461055, 1.8028572256396647, 0.9279757672456204, 0.3946339367881464, -1.375925438230254]
    """

    def __init__(self, interval):
        """Polynomial Mutation initialiser in order to specify kind of Operator and interval of continuous solution

        Args:
            interval: {(float, float)} -- minimum and maximum values interval of variables in the solution
        """
        super().__init__()

        self.mini, self.maxi = interval


    def apply(self, solution):
        """Create new solution based on solution passed as parameter

        Args:
            solution: {:class:`~macop.solutions.base.Solution`} -- the solution to use for generating new solution

        Returns:
            {:class:`~macop.solutions.base.Solution`}: new generated solution
        """

        size = solution.size
        rate = float(1/size)

        copy_solution = solution.clone()

        rand = random.uniform(0, 1)

        # apply mutation over the new computed solution
        copy_solution.data = [x if rand > rate else x + self._sigma(size) * (self.maxi - (self.mini)) for x in solution.data]
        copy_solution.data = self._repair(copy_solution)

        return copy_solution

    def _repair(self, solution):
        """
        Private repair function for solutions if an element is out of bounds of an expected interval

        Args:
            solution: {:class:`~macop.solutions.base.Solution`} -- the solution to use for generating new solution

        Returns:
            {ndarray} -- repaired array of float values
        """
        return np.array([self.mini if x < self.mini else self.maxi if x > self.maxi else x for x in solution.data])

    
    def _sigma(self, size):
        """
        Compute the sigma value for polynomial mutation

        Args:
            size: {integer} -- 

        Returns:
            {float} -- expected sigma value depending on solution size
        """
        rand = random.uniform(0, 1)
        sigma = 0
        if rand < 0.5:
            sigma = pow(2 * rand, 1 / (size + 1)) - 1
        else:
            sigma = 1 - pow(2 - 2 * rand, 1 / (size - 1))
        return sigma