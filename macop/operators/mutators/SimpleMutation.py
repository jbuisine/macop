"""Mutation implementation for binary solution, swap two bits randomly from solution
"""
# main imports
import random
import sys

# module imports
from .Mutation import Mutation
from ...utils.modules import load_class


class SimpleMutation(Mutation):
    """Mutation implementation for binary solution, swap two bits randomly from solution

    Attributes:
        kind: {KindOperator} -- specify the kind of operator
    """
    def apply(self, solution):
        """Create new solution based on solution passed as parameter

        Args:
            solution: {Solution} -- the solution to use for generating new solution

        Returns:
            {Solution} -- new generated solution
        """

        size = solution._size

        firstCell = 0
        secondCell = 0

        # copy data of solution
        currentData = solution._data.copy()

        while firstCell == secondCell:
            firstCell = random.randint(0, size - 1)
            secondCell = random.randint(0, size - 1)

        temp = currentData[firstCell]

        # swicth values
        currentData[firstCell] = currentData[secondCell]
        currentData[secondCell] = temp

        # create solution of same kind with new data
        class_name = type(solution).__name__

        # dynamically load solution class if unknown
        if class_name not in sys.modules:
            load_class(class_name, globals())

        return getattr(globals()['macop.solutions.' + class_name],
                       class_name)(currentData, size)
