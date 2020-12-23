"""Discrete solution classes implementations
"""
import numpy as np

# modules imports
from .base import Solution


class BinarySolution(Solution):
    """
    Binary integer solution class

    Attributes:
        data: {ndarray} --  array of binary values
        size: {int} -- size of binary array values
        score: {float} -- fitness score value
    """
    def __init__(self, data, size):
        """
        Initialize binary solution using specific data

        Args:
            data: {ndarray} --  array of binary values
            size: {int} -- size of binary array values

        >>> from macop.solutions.discrete import BinarySolution
        >>> data = [0, 1, 0, 1, 1]
        >>> solution = BinarySolution(data, len(data))
        >>> sum(solution._data) == 3
        True
        >>> solution_copy = solution.clone()
        >>> all(solution_copy._data == solution._data)
        True
        """
        super().__init__(np.array(data), size)

    @staticmethod
    def random(validator, size):
        """
        Intialize binary array with use of validator to generate valid random solution

        Args:
            validator: {function} -- specific function which validates or not a solution
            size: {int} -- expected solution size to generate

        Returns:
            {BinarySolution} -- new generated binary solution

        Example:

        >>> from macop.solutions.discrete import BinarySolution
        >>> validator = lambda solution: True if sum(solution._data) > 5 else False
        >>> solution = BinarySolution.random(validator, 10)
        >>> sum(solution._data) > 5
        True
        """

        data = np.random.randint(2, size=size)
        solution = BinarySolution(data, size)

        while not validator(solution):
            data = np.random.randint(2, size=size)
            solution = BinarySolution(data, size)

        return solution

    def __str__(self):
        return f"Binary solution {self._data}"



class CombinatoryIntegerSolution(Solution):
    """
    Combinatory integer solution class

    Attributes:
        data: {ndarray} --  array of binary values
        size: {int} -- size of binary array values
        score: {float} -- fitness score value
    """
    def __init__(self, data, size):
        """
        Initialize binary solution using specific data

        Args:
            data: {ndarray} --  array of binary values
            size: {int} -- size of binary array values

        >>> from macop.solutions.discrete import CombinatoryIntegerSolution
        >>> import numpy as np
        >>> data = np.arange(5)
        >>> solution = CombinatoryIntegerSolution(data, 5)
        >>> sum(solution._data) == 10
        True
        >>> solution_copy = solution.clone()
        >>> all(solution_copy._data == solution._data)
        True
        """
        super().__init__(data, size)

    @staticmethod
    def random(validator, size):
        """
        Intialize combinatory integer array with use of validator to generate valid random solution

        Args:
            validator: {function} -- specific function which validates or not a solution
            size: {int} -- expected solution size to generate

        Returns:
            {CombinatoryIntegerSolution} -- new generated combinatory integer solution

        Example:

        >>> from macop.solutions.discrete import CombinatoryIntegerSolution
        >>> validator = lambda solution: True if sum(solution._data) > 5 else False
        >>> solution = CombinatoryIntegerSolution.random(validator, 5)
        >>> sum(solution._data) > 5
        True
        """

        data = np.arange(size)
        np.random.shuffle(data)
        solution = CombinatoryIntegerSolution(data, size)

        while not validator(solution):
            data = np.arange(size)
            np.random.shuffle(data)
            solution = CombinatoryIntegerSolution(data, size)

        return solution

    def __str__(self):
        return f"Combinatory integer solution {self._data}"


class IntegerSolution(Solution):
    """
    Integer solution class

    Attributes:
        data: {ndarray} --  array of binary values
        size: {int} -- size of binary array values
        score: {float} -- fitness score value
    """
    def __init__(self, data, size):
        """
        Initialize integer solution using specific data

        Args:
            data: {ndarray} --  array of binary values
            size: {int} -- size of binary array values

        Example:

        >>> from macop.solutions.discrete import IntegerSolution
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> data = np.random.randint(5, size=10)
        >>> solution = IntegerSolution(data, 10)
        >>> sum(solution._data)
        28
        >>> solution_copy = solution.clone()
        >>> all(solution_copy._data == solution._data)
        True
        """
        super().__init__(data, size)

    @staticmethod
    def random(validator, size):
        """
        Intialize integer array with use of validator to generate valid random solution

        Args:
            validator: {function} -- specific function which validates or not a solution
            size: {int} -- expected solution size to generate

        Returns:
            {IntegerSolution} -- new generated integer solution

        Example:

        >>> from macop.solutions.discrete import IntegerSolution
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> validator = lambda solution: True if sum(solution._data) > 5 else False
        >>> solution = IntegerSolution.random(validator, 5)
        >>> sum(solution._data) > 10
        True
        """

        data = np.random.randint(size, size=size)
        solution = IntegerSolution(data, size)

        while not validator(solution):
            data = np.random.randint(size, size=size)
            solution = IntegerSolution(data, size)

        return solution

    def __str__(self):
        return f"Integer solution {self._data}"