"""Combinatory integer solution class implementation
"""
# main imports
import numpy as np

# modules imports
from .Solution import Solution


# Solution which stores solution data as combinatory integer array
class CombinatoryIntegerSolution(Solution):
    """
    Combinatory integer solution class

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
        Intialize combinatory integer array with use of validator to generate valid random solution

        Args:
            _validator: {function} -- specific function which validates or not a solution

        Returns:
            {CombinatoryIntegerSolution} -- new generated combinatory integer solution
        """

        self.data = np.random.shuffle(np.arange(self.size))

        while not self.isValid(_validator):
            self.data = np.random.shuffle(np.arange(self.size))

        return self

    def __str__(self):
        return "Combinatory integer solution %s" % (self.data)
