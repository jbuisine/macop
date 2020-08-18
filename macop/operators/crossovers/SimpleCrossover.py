"""Crossover implementation which generated new solution by splitting at mean size best solution and current solution
"""
# main imports
import random
import sys
import pkgutil

# module imports
from .Crossover import Crossover

# import all available solutions
for loader, module_name, is_pkg in pkgutil.walk_packages(
        path=['macop/solutions'], prefix='macop.solutions.'):
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module


class SimpleCrossover(Crossover):
    """Crossover implementation which generated new solution by splitting at mean size best solution and current solution

    Attributes:
        kind: {Algorithm} -- specify the kind of operator
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

        splitIndex = int(size / 2)

        if random.uniform(0, 1) > 0.5:
            firstData[splitIndex:(size - 1)] = firstData[splitIndex:(size - 1)]
            currentData = firstData
        else:
            secondData[splitIndex:(size - 1)] = firstData[splitIndex:(size -
                                                                      1)]
            currentData = secondData

        # create solution of same kind with new data
        class_name = type(_solution).__name__
        return getattr(globals()['macop.solutions.' + class_name],
                       class_name)(currentData, size)
