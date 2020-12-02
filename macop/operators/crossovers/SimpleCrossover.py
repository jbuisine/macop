"""Crossover implementation which generated new solution by splitting at mean size best solution and current solution
"""
# main imports
import random
import sys
import pkgutil

# module imports
from .Crossover import Crossover
from ...utils.modules import load_class

# import all available solutions
# for loader, module_name, is_pkg in pkgutil.walk_packages(
#         path=[
#             str(pathlib.Path(__file__).parent.absolute()) + '/../../solutions'
#         ],
#         prefix='macop.solutions.'):
#     _module = loader.find_module(module_name).load_module(module_name)
#     globals()[module_name] = _module


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

        size = solution.size

        # copy data of solution
        firstData = solution._data.copy()

        # get best solution from current algorithm
        secondData = self._algo._bestSolution._data.copy()

        splitIndex = int(size / 2)

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
