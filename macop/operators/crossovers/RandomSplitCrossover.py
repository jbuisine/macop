"""Crossover implementation which generated new solution by randomly splitting best solution and current solution
"""
# main imports
import random
import sys

# module imports
from .Crossover import Crossover

# need to import the specify kind of solution
from ...solutions.BinarySolution import BinarySolution
from ...solutions.Solution import Solution


class RandomSplitCrossover(Crossover):
    """Crossover implementation which generated new solution by randomly splitting best solution and current solution

    Attributes:
        kind: {KindOperator} -- specify the kind of operator
    """
    def apply(self, _solution):
        """Create new solution based on best solution found and solution passed as parameter

        Args:
            _solution: {Solution} -- the solution to use for generating new solution

        Returns:
            {Solution} -- new generated solution
        """
        size = _solution.size

        # copy data of solution
        firstData = _solution.data.copy()
        # get best solution from current algorithm
        secondData = self.algo.bestSolution.data.copy()

        splitIndex = random.randint(0, len(secondData))

        if random.uniform(0, 1) > 0.5:
            firstData[splitIndex:(size - 1)] = firstData[splitIndex:(size - 1)]
            currentData = firstData
        else:
            secondData[splitIndex:(size - 1)] = firstData[splitIndex:(size -
                                                                      1)]
            currentData = secondData

        # create solution of same kind with new data
        return globals()[type(_solution).__name__](currentData, size)
