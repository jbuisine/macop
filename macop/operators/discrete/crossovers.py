"""Crossover implementations for discrete solutions kind
"""
# main imports
import random
import sys

# module imports
from ..base import Crossover


class SimpleCrossover(Crossover):
    """Crossover implementation which generated new solution by splitting at mean size best solution and current solution

    Attributes:
        kind: {Algorithm} -- specify the kind of operator
    """
    def apply(self, solution):
        """Create new solution based on best solution found and solution passed as parameter

        Args:
            solution: {Solution} -- the solution to use for generating new solution

        Returns:
            {Solution} -- new generated solution
        """

        size = solution._size

        # copy data of solution
        firstData = solution._data.copy()

        # get best solution from current algorithm
        copy_solution = self._algo._bestSolution.clone()

        splitIndex = int(size / 2)

        if random.uniform(0, 1) > 0.5:
            copy_solution._data[splitIndex:] = firstData[splitIndex:]
        else:
            copy_solution._data[:splitIndex] = firstData[:splitIndex]

        return copy_solution


class RandomSplitCrossover(Crossover):
    """Crossover implementation which generated new solution by randomly splitting best solution and current solution

    Attributes:
        kind: {KindOperator} -- specify the kind of operator
    """
    def apply(self, solution):
        """Create new solution based on best solution found and solution passed as parameter

        Args:
            solution: {Solution} -- the solution to use for generating new solution

        Returns:
            {Solution} -- new generated solution
        """
        size = solution._size

        # copy data of solution
        firstData = solution._data.copy()

        # get best solution from current algorithm
        copy_solution = self._algo._bestSolution.clone()

        splitIndex = random.randint(0, size)

        if random.uniform(0, 1) > 0.5:
            copy_solution._data[splitIndex:] = firstData[splitIndex:]
        else:
            copy_solution._data[:splitIndex] = firstData[:splitIndex]

        return copy_solution
