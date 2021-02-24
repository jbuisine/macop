"""Continuous solution classes implementation
"""
import numpy as np

# modules imports
from macop.solutions.base import Solution

class ContinuousSolution(Solution):
    """
    Continuous solution class

    - store solution as a float array (example: [0.5, 0.2, 0.17, 0.68, 0.42])
    - associated size is the size of the array
    - mainly use for selecting or not an element in a list of valuable objects

    Attributes:
        data: {ndarray} --  array of float values
        size: {int} -- size of float array values
        score: {float} -- fitness score value
    """
    def __init__(self, data, size):
        """
        initialise continuous solution using specific data

        Args:
            data: {ndarray} --  array of float values
            size: {int} -- size of float array values

        Example:

        >>> from macop.solutions.continuous import ContinuousSolution
        >>>
        >>> # build of a solution using specific data and size
        >>> data = [0.2, 0.4, 0.6, 0.8, 1]
        >>> solution = ContinuousSolution(data, len(data))
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
    def random(size, interval, validator=None):
        """
        Intialize float array with use of validator to generate valid random solution

        Args:
            size: {int} -- expected solution size to generate
            interval: {(float, float)} -- tuple with min and max expected interval value for current solution
            validator: {function} -- specific function which validates or not a solution (if None, not validation is applied)

        Returns:
            {:class:`~macop.solutions.discrete.Continuous`}: new generated continuous solution

        Example:

        >>> from macop.solutions.continuous import ContinuousSolution
        >>>
        >>> # generate random solution using specific validator
        >>> validator = lambda solution: True if sum(solution.data) > 5 else False
        >>> solution = ContinuousSolution.random(10, (-2, 2), validator)
        >>> sum(solution.data) > 5
        True
        """

        mini, maxi = interval

        data = np.random.random(size=size) * (maxi - mini) + mini
        solution = ContinuousSolution(data, size)

        if not validator:
            return solution

        while not validator(solution):
            data = np.random.random(size=size) * (maxi - mini) + mini
            solution = ContinuousSolution(data, size)

        return solution

    def __str__(self):
        return f"Continuous solution {self._data}"