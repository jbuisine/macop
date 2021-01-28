"""Discrete solution classes implementations
"""
import numpy as np

# modules imports
from macop.solutions.base import Solution


class BinarySolution(Solution):
    """
    Binary integer solution class

    - store solution as a binary array (example: [0, 1, 0, 1, 1])
    - associated size is the size of the array
    - mainly use for selecting or not an element in a list of valuable objects

    Attributes:
        data: {ndarray} --  array of binary values
        size: {int} -- size of binary array values
        score: {float} -- fitness score value
    """
    def __init__(self, data, size):
        """
        initialise binary solution using specific data

        Args:
            data: {ndarray} --  array of binary values
            size: {int} -- size of binary array values

        Example:

        >>> from macop.solutions.discrete import BinarySolution
        >>>
        >>> # build of a solution using specific data and size
        >>> data = [0, 1, 0, 1, 1]
        >>> solution = BinarySolution(data, len(data))
        >>>
        >>> # check data content
        >>> sum(solution.data) == 3
        True
        >>> # clone solution
        >>> solution_copy = solution.clone()
        >>> all(solution_copy.data == solution.data)
        True
        """
        super().__init__(np.array(data), size)

    @staticmethod
    def random(size, validator=None):
        """
        Intialize binary array with use of validator to generate valid random solution

        Args:
            size: {int} -- expected solution size to generate
            validator: {function} -- specific function which validates or not a solution (if None, not validation is applied)

        Returns:
            {:class:`~macop.solutions.discrete.BinarySolution`}: new generated binary solution

        Example:

        >>> from macop.solutions.discrete import BinarySolution
        >>>
        >>> # generate random solution using specific validator
        >>> validator = lambda solution: True if sum(solution.data) > 5 else False
        >>> solution = BinarySolution.random(10, validator)
        >>> sum(solution.data) > 5
        True
        """

        data = np.random.randint(2, size=size)
        solution = BinarySolution(data, size)

        if not validator:
            return solution

        while not validator(solution):
            data = np.random.randint(2, size=size)
            solution = BinarySolution(data, size)

        return solution

    def __str__(self):
        return f"Binary solution {self._data}"


class CombinatoryIntegerSolution(Solution):
    """
    Combinatory integer solution class

    - store solution as a combinatory array (example: [1, 3, 0, 2])
    - associated size is the size of the array
    - mainly use for selecting or not an element in a list of valuable objects

    Attributes:
        data: {ndarray} --  array of integer values
        size: {int} -- size of integer array values
        score: {float} -- fitness score value
    """
    def __init__(self, data, size):
        """
        initialise integer solution using specific data

        Args:
            data: {ndarray} --  array of integer values
            size: {int} -- size of integer array values

        >>> from macop.solutions.discrete import CombinatoryIntegerSolution
        >>> import numpy as np
        >>> data = np.arange(5)
        >>> solution = CombinatoryIntegerSolution(data, 5)
        >>> sum(solution.data) == 10
        True
        >>> solution_copy = solution.clone()
        >>> all(solution_copy.data == solution.data)
        True
        """
        super().__init__(data, size)

    @staticmethod
    def random(size, validator=None):
        """
        Intialize combinatory integer array with use of validator to generate valid random solution

        Args:
            size: {int} -- expected solution size to generate
            validator: {function} -- specific function which validates or not a solution (if None, not validation is applied)

        Returns:
            {:class:`~macop.solutions.discrete.CombinatoryIntegerSolution`}: new generated combinatory integer solution

        Example:

        >>> from macop.solutions.discrete import CombinatoryIntegerSolution
        >>>
        >>> # generate random solution using specific validator
        >>> validator = lambda solution: True if sum(solution.data) > 5 else False
        >>> solution = CombinatoryIntegerSolution.random(5, validator)
        >>> sum(solution.data) > 5
        True
        """

        data = np.arange(size)
        np.random.shuffle(data)
        solution = CombinatoryIntegerSolution(data, size)

        if not validator:
            return solution

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
        initialise integer solution using specific data

        Args:
            data: {ndarray} --  array of binary values
            size: {int} -- size of binary array values

        Example:

        >>> from macop.solutions.discrete import IntegerSolution
        >>> import numpy as np
        >>> np.random.seed(42)
        >>> data = np.random.randint(5, size=10)
        >>> solution = IntegerSolution(data, 10)
        >>> sum(solution.data)
        28
        >>> solution_copy = solution.clone()
        >>> all(solution_copy.data == solution.data)
        True
        """
        super().__init__(data, size)

    @staticmethod
    def random(size, validator=None):
        """
        Intialize integer array with use of validator to generate valid random solution

        Args:
            size: {int} -- expected solution size to generate
            validator: {function} -- specific function which validates or not a solution (if None, not validation is applied)

        Returns:
            {:class:`~macop.solutions.discrete.IntegerSolution`}: new generated integer solution

        Example:

        >>> from macop.solutions.discrete import IntegerSolution
        >>> import numpy as np
        >>> np.random.seed(42)
        >>>
        >>> # generate random solution using specific validator
        >>> validator = lambda solution: True if sum(solution.data) > 5 else False
        >>> solution = IntegerSolution.random(5, validator)
        >>> sum(solution.data) > 10
        True
        """

        data = np.random.randint(size, size=size)
        solution = IntegerSolution(data, size)

        if not validator:
            return solution

        while not validator(solution):
            data = np.random.randint(size, size=size)
            solution = IntegerSolution(data, size)

        return solution

    def __str__(self):
        return f"Integer solution {self._data}"
