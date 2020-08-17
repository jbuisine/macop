"""Binary solution class implementation
"""
import numpy as np

# modules imports
from .Solution import Solution


# Solution which stores solution data as binary array
class BinarySolution(Solution):
    """
    Binary integer solution class

    Attributes:
        data: {ndarray} --  array of binary values
        size: {int} -- size of binary array values
        score: {float} -- fitness score value
    """
    def __init__(self, _data, _size):
        """
        Initialize binary solution using specific data

        Args:
            data: {ndarray} --  array of binary values
            size: {int} -- size of binary array values
        """

        self.data = _data
        self.size = _size

    def random(self, _validator):
        """
        Intialize binary array with use of validator to generate valid random solution

        Args:
            _validator: {function} -- specific function which validates or not a solution

        Returns:
            {BinarySolution} -- new generated binary solution
        """

        self.data = np.random.randint(2, size=self.size)

        while not self.isValid(_validator):
            self.data = np.random.randint(2, size=self.size)

        return self

    def __str__(self):
        return "Binary solution %s" % (self.data)
