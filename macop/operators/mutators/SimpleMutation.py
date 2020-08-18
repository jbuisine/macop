"""Mutation implementation for binary solution, swap two bits randomly from solution
"""
# main imports
import random
import sys
import pkgutil

# module imports
from .Mutation import Mutation

# import all available solutions
for loader, module_name, is_pkg in pkgutil.walk_packages(
        path=['macop/solutions'], prefix='macop.solutions.'):
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module


class SimpleMutation(Mutation):
    """Mutation implementation for binary solution, swap two bits randomly from solution

    Attributes:
        kind: {KindOperator} -- specify the kind of operator
    """
    def apply(self, _solution):
        """Create new solution based on solution passed as parameter

        Args:
            _solution: {Solution} -- the solution to use for generating new solution

        Returns:
            {Solution} -- new generated solution
        """

        size = _solution.size

        firstCell = 0
        secondCell = 0

        # copy data of solution
        currentData = _solution.data.copy()

        while firstCell == secondCell:
            firstCell = random.randint(0, size - 1)
            secondCell = random.randint(0, size - 1)

        temp = currentData[firstCell]

        # swicth values
        currentData[firstCell] = currentData[secondCell]
        currentData[secondCell] = temp

        # create solution of same kind with new data
        class_name = type(_solution).__name__
        return getattr(globals()['macop.solutions.' + class_name],
                       class_name)(currentData, size)
