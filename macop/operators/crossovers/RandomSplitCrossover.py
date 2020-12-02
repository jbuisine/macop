"""Crossover implementation which generated new solution by randomly splitting best solution and current solution
"""
# main imports
import random
import sys
import pkgutil

# module imports
from .Crossover import Crossover
from ...utils.modules import load_class


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
        secondData = self._algo._bestSolution._data.copy()

        splitIndex = random.randint(0, len(secondData))

        if random.uniform(0, 1) > 0.5:
            firstData[splitIndex:(size - 1)] = firstData[splitIndex:(size - 1)]
            currentData = firstData
        else:
            secondData[splitIndex:(size - 1)] = firstData[splitIndex:(size -
                                                                      1)]
            currentData = secondData

        # create solution of same kind with new data
        class_name = type(solution).__name__

        # dynamically load solution class if unknown
        if class_name not in sys.modules:
            load_class(class_name, globals())

        return getattr(globals()['macop.solutions.' + class_name],
                       class_name)(currentData, size)
