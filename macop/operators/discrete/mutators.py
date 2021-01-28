"""Mutation implementations for discrete solution
"""
# main imports
import random
import sys

# module imports
from macop.operators.base import Mutation


class SimpleMutation(Mutation):
    """Mutation implementation for binary solution, swap two bits randomly from solution

    Attributes:
        kind: {:class:`~macop.operators.base.KindOperator`} -- specify the kind of operator

    Example:

    >>> # import of solution and simple mutation operator
    >>> from macop.solutions.discrete import BinarySolution
    >>> from macop.operators.discrete.mutators import SimpleMutation
    >>> solution = BinarySolution.random(5)
    >>> list(solution.data)
    [1, 0, 0, 0, 1]
    >>> mutator = SimpleMutation()
    >>> mutation_solution = mutator.apply(solution)
    >>> list(mutation_solution.data)
    [0, 0, 1, 0, 1]
    """
    def apply(self, solution):
        """Create new solution based on solution passed as parameter

        Args:
            solution: {:class:`~macop.solutions.base.Solution`} -- the solution to use for generating new solution

        Returns:
            {:class:`~macop.solutions.base.Solution`}: new generated solution
        """

        size = solution._size

        firstCell = 0
        secondCell = 0

        # copy of solution
        copy_solution = solution.clone()

        while firstCell == secondCell:
            firstCell = random.randint(0, size - 1)
            secondCell = random.randint(0, size - 1)

        temp = copy_solution.data[firstCell]

        # swicth values
        copy_solution.data[firstCell] = copy_solution.data[secondCell]
        copy_solution.data[secondCell] = temp

        return copy_solution


class SimpleBinaryMutation(Mutation):
    """Mutation implementation for binary solution, swap bit randomly from solution

    Attributes:
        kind: {:class:`~macop.operators.base.KindOperator`} -- specify the kind of operator

    Example:

    >>> # import of solution and simple binary mutation operator
    >>> from macop.solutions.discrete import BinarySolution
    >>> from macop.operators.discrete.mutators import SimpleBinaryMutation
    >>> solution = BinarySolution.random(5)
    >>> list(solution.data)
    [0, 1, 0, 0, 0]
    >>> mutator = SimpleBinaryMutation()
    >>> mutation_solution = mutator.apply(solution)
    >>> list(mutation_solution.data)
    [1, 1, 0, 0, 0]
    """
    def apply(self, solution):
        """Create new solution based on solution passed as parameter

        Args:
            solution: {:class:`~macop.solutions.base.Solution`} -- the solution to use for generating new solution

        Returns:
            {:class:`~macop.solutions.base.Solution`}: new generated solution
        """

        size = solution._size
        cell = random.randint(0, size - 1)

        # copy of solution
        copy_solution = solution.clone()

        # swicth values
        if copy_solution.data[cell]:
            copy_solution.data[cell] = 0
        else:
            copy_solution.data[cell] = 1

        return copy_solution
