"""Integer solution class implementation
"""
# main imports
import numpy as np

# modules imports
from .Solution import Solution


# Solution which stores solution data as integer array
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
        """

        self._data = data
        self._size = size

    def random(self, validator):
        """
        Intialize integer array with use of validator to generate valid random solution

        Args:
            validator: {function} -- specific function which validates or not a solution

        Returns:
            {IntegerSolution} -- new generated integer solution
        """

        self._data = np.random.randint(self._size, size=self._size)

        while not self.isValid(validator):
            self._data = np.random.randint(self._size, size=self._size)

        return self

    def __str__(self):
        return "Integer solution %s" % (self._data)
