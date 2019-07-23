# main imports
import numpy as np

# modules imports
from .Solution import Solution


# Solution which stores solution data as integer array
class IntegerSolution(Solution):

    def __init__(self, _data, _size):
        """
        Initialize data of solution using specific data

        - `data` field is array of integer values
        - `size` field is the size of array integer values
        """

        self.data = _data
        self.size = _size


    def random(self, _validator):
        """
        Intialize integer array using size solution data

        Use of validator to generate valid random solution
        """

        self.data = np.random.randint(self.size, size=self.size)

        while not self.isValid(_validator):
            self.data = np.random.randint(self.size, size=self.size)

        return self


    def __str__(self):
        return "Integer solution %s" % (self.data)
        