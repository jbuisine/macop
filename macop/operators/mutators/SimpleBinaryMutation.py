"""Mutation implementation for binary solution, swap bit randomly from solution
"""
# main imports
import random
import sys

# module imports
from .Mutation import Mutation

from ...solutions.BinarySolution import BinarySolution
from ...solutions.Solution import Solution


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
        return globals()[type(_solution).__name__](currentData, size)
