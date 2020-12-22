"""Mutation implementations for discrete solution
"""
# main imports
import random
import sys

# module imports
from ..base import Mutation


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

        # copy of solution
        copy_solution = solution.clone()

        while firstCell == secondCell:
            firstCell = random.randint(0, size - 1)
            secondCell = random.randint(0, size - 1)

        temp = copy_solution._data[firstCell]

        # swicth values
        copy_solution._data[firstCell] = copy_solution._data[secondCell]
        copy_solution._data[secondCell] = temp

        return copy_solution


class SimpleBinaryMutation(Mutation):
    """Mutation implementation for binary solution, swap bit randomly from solution

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
        cell = random.randint(0, size - 1)

        # copy of solution
        copy_solution = solution.clone()

        # swicth values
        if copy_solution._data[cell]:
            copy_solution._data[cell] = 0
        else:
            copy_solution._data[cell] = 1

        return copy_solution
