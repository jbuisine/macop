"""Crossover implementations for continuous solutions kind
"""
# main imports
import random
import sys
import numpy as np

# module imports
from macop.operators.base import Crossover

class BasicDifferentialEvolutionCrossover(Crossover):
    """Basic Differential Evolution implementation for continuous solution

    Attributes:
        kind: {:class:`~macop.operators.base.KindOperator`} -- specify the kind of operator

    Example:

    >>> # import of solution and polynomial mutation operator
    >>> from macop.solutions.continuous import ContinuousSolution
    >>> from macop.operators.continuous.crossovers import BasicDifferentialEvolutionCrossover
    >>> solution = ContinuousSolution.random(5, (-2, 2))
    >>> list(solution.data)
    [-1.3760219186551894, -1.7676655513272022, 1.4647045830997407, 0.4044600469728352, 0.832290311184182]
    >>> crossover = BasicDifferentialEvolutionCrossover(interval=(-2, 2))
    >>> crossover_solution = crossover.apply(solution)
    >>> list(crossover_solution.data)
    [-1.7016619497704522, -0.43633033292228895, 2.0, -0.034751768954844, 0.6134819652022994]
    """

    def __init__(self, interval, CR=1.0, F=0.5):
        """"Basic Differential Evolution crossover initialiser in order to specify kind of Operator and interval of continuous solution

        Args:
            interval: {(float, float)} -- minimum and maximum values interval of variables in the solution
            CR: {float} -- probability to use of new generated solutions when modifying a value of current solution
            F: {float} -- degree of impact of the new generated solutions on the current solution when obtaining new solution
        """
        super().__init__()

        self.mini, self.maxi = interval
        self.CR = CR
        self.F = F


    def apply(self, solution):
        """Create new solution based on solution passed as parameter

        Args:
            solution: {:class:`~macop.solutions.base.Solution`} -- the solution to use for generating new solution

        Returns:
            {:class:`~macop.solutions.base.Solution`}: new continuous generated solution
        """

        size = solution.size

        solution1 = solution.clone()

        # create two new random solutions using instance and its static method
        solution2 = solution.random(size, interval=(self.mini, self.maxi))
        solution3 = solution.random(size, interval=(self.mini, self.maxi))

        # apply crossover on the new computed solution
        for i in range(len(solution1.data)):

            # use of CR to change or not the current value of the solution using new solutions
            if random.uniform(0, 1) < self.CR:
                solution1.data[i] = solution1.data[i] + self.F * (solution2.data[i] - solution3.data[i])

        # repair solution if necessary
        solution1.data = self._repair(solution1)

        return solution1

    def _repair(self, solution):
        """
        Private repair function for solutions if an element is out of bounds of an expected interval 

        Args:
            solution: {:class:`~macop.solutions.base.Solution`} -- the solution to use for generating new solution

        Returns:
            {ndarray} -- repaired array of float values
        """
        return np.array([self.mini if x < self.mini else self.maxi if x > self.maxi else x for x in solution.data])