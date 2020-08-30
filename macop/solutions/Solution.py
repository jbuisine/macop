"""Abstract solution class
"""

from abc import abstractmethod


class Solution():
    def __init__(self, _data, _size):
        """
        Binary integer solution class

        Attributes:
            data: {ndarray} --  array of binary values
            size: {int} -- size of binary array values
            score: {float} -- fitness score value
        """
        self.data = _data
        self.size = _size
        self.score = None

    def isValid(self, _validator):
        """
        Use of custom method which validates if solution is valid or not

        Args:
            _validator: {function} -- specific function which validates or not a solution

        Returns:
            {bool} -- `True` is solution is valid
        """
        return _validator(self)

    def evaluate(self, _evaluator):
        """
        Evaluate solution using specific `_evaluator`

        Args:
            _evaluator: {function} -- specific function which computes fitness of solution

        Returns:
            {float} -- fitness score value
        """
        self.score = _evaluator(self)
        return self.score

    def fitness(self):
        """
        Returns fitness score

        Returns:
            {float} -- fitness score value
        """
        return self.score

    @abstractmethod
    def random(self, _validator):
        """
        Initialize solution using random data

        Args:
            _validator: {function} -- specific function which validates or not a solution

        Returns:
            {Solution} -- generated solution
        """
        pass

    def __str__(self):
        print("Generic solution with ", self.data)
