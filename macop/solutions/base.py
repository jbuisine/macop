"""Abstract solution class
"""

from abc import abstractmethod
from copy import deepcopy

class Solution():
    """Base abstract solution class structure
    
    - stores solution data representation into `data` attribute
    - get size (shape) of specific data representation
    - stores the score of the solution
    """

    def __init__(self, data, size):
        """
        Abstract solution class constructor

        Attributes:
            data: {ndarray} --  array of binary values
            size: {int} -- size of binary array values
            score: {float} -- fitness score value
        """
        self._data = data
        self._size = size
        self._score = None

    def isValid(self, validator):
        """
        Use of custom function which checks if a solution is valid or not

        Args:
            validator: {function} -- specific function which validates or not a solution

        Returns:
            {bool} -- `True` is solution is valid
        """
        return validator(self)

    def evaluate(self, evaluator):
        """
        Evaluate solution using specific `evaluator`

        Args:
            _evaluator: {function} -- specific function which computes fitness of solution

        Returns:
            {float} -- fitness score value
        """
        self._score = evaluator.compute(self)
        return self._score

    def fitness(self):
        """
        Returns fitness score

        Returns:
            {float} -- fitness score value
        """
        return self._score

    @staticmethod
    def random(size, validator=None):
        """
        Initialize solution using random data with validator or not

        Args:
            size: {int} -- expected solution size to generate
            validator: {function} -- specific function which validates or not a solution (if None, not validation is applied)

        Returns:
            {Solution} -- generated solution
        """
        return None

    def clone(self):
        """Clone the current solution and its data, but without keeping evaluated `_score`

        Returns:
            {Solution} -- clone of current solution
        """
        copy_solution = deepcopy(self)
        copy_solution._score = None

        return copy_solution

    def __str__(self):
        print("Generic solution with ", self._data)
