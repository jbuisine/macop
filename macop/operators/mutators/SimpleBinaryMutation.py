"""Mutation implementation for binary solution, swap bit randomly from solution
"""
# main imports
import random
import sys

# module imports
from .Mutation import Mutation
from ...utils.modules import load_class


class SimpleBinaryMutation(Mutation):
    """Mutation implementation for binary solution, swap bit randomly from solution

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

        cell = random.randint(0, size - 1)

        # copy data of solution
        currentData = _solution.data.copy()

        # swicth values
        if currentData[cell]:
            currentData[cell] = 0
        else:
            currentData[cell] = 1

        # create solution of same kind with new data
        class_name = type(_solution).__name__

        # dynamically load solution class if unknown
        if class_name not in sys.modules:
            load_class(class_name, globals())

        return getattr(globals()['macop.solutions.' + class_name],
                       class_name)(currentData, size)
