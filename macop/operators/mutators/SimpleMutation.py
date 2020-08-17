"""Mutation implementation for binary solution, swap two bits randomly from solution
"""
# main imports
import random
import sys

# module imports
from .Mutation import Mutation

from ...solutions.BinarySolution import BinarySolution
from ...solutions.Solution import Solution


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
        return globals()[type(_solution).__name__](currentData, size)
