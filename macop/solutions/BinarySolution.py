# main imports
import numpy as np

# modules imports
from .Solution import Solution


# Solution which stores solution data as binary array
class BinarySolution(Solution):
    def __init__(self, _data, _size):
        """
        Initialize data of solution using specific data

        - `data` field is array of binary values
        - `size` field is the size of array binary values
        """

        self.data = _data
        self.size = _size

    def random(self, _validator):
        """
        Intialize binary array using size solution data

        Use of validator to generate valid random solution
        """

        self.data = np.random.randint(2, size=self.size)

        while not self.isValid(_validator):
            self.data = np.random.randint(2, size=self.size)

        return self

    def __str__(self):
        return "Binary solution %s" % (self.data)
