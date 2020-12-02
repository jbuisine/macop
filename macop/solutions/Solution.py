"""Abstract solution class
"""

from abc import abstractmethod


class Solution():
    def __init__(self, data, size):
        """
        Binary integer solution class

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
        Use of custom method which validates if solution is valid or not

        Args:
            validator: {function} -- specific function which validates or not a solution

        Returns:
            {bool} -- `True` is solution is valid
        """
        return validator(self)

    def evaluate(self, evaluator):
        """
        Evaluate solution using specific `_evaluator`

        Args:
            _evaluator: {function} -- specific function which computes fitness of solution

        Returns:
            {float} -- fitness score value
        """
        self._score = evaluator(self)
        return self._score

    def fitness(self):
        """
        Returns fitness score

        Returns:
            {float} -- fitness score value
        """
        return self._score

    @abstractmethod
    def random(self, validator):
        """
        Initialize solution using random data

        Args:
            validator: {function} -- specific function which validates or not a solution

        Returns:
            {Solution} -- generated solution
        """
        pass

    def __str__(self):
        print("Generic solution with ", self._data)
