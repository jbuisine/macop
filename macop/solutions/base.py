"""Abstract solution class
"""

from abc import abstractmethod
from copy import deepcopy


class Solution():
    """Base abstract solution class structure
    
    - stores solution data representation into ndarray `data` attribute
    - get size (shape) of specific data representation
    - stores the score of the solution
    """
    def __init__(self, data, size):
        """
        Abstract solution class constructor

        Attributes:
            data: {ndarray} --  ndarray of values
            size: {int} -- size of ndarray values
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
            {bool}: `True` is solution is valid
        """
        return validator(self)

    def evaluate(self, evaluator):
        """
        Evaluate solution using specific `evaluator`

        Args:
            _evaluator: {function} -- specific function which computes fitness of solution

        Returns:
            {float}: fitness score value
        """
        self._score = evaluator.compute(self)
        return self._score

    @property
    def fitness(self):
        """
        Returns fitness score (by default `score` private attribute)

        Returns:
            {float}: fitness score value
        """
        return self._score

    @fitness.setter
    def fitness(self, score):
        """
        Set solution score as wished (by default `score` private attribute)
        """
        self._score = score

    @property
    def data(self):
        """
        Returns solution data (by default `data` private attribute)

        Returns:
            {object}: data values
        """
        return self._data

    @data.setter
    def data(self, data):
        """
        Set solution data (by default `data` private attribute)
        """
        self._data = data

    @staticmethod
    def random(size, validator=None):
        """
        initialise solution using random data with validator or not

        Args:
            size: {int} -- expected solution size to generate
            validator: {function} -- specific function which validates or not a solution (if None, not validation is applied)

        Returns:
            {:class:`~macop.solutions.base.Solution`}: generated solution
        """
        return None

    def clone(self):
        """Clone the current solution and its data, but without keeping evaluated `_score`

        Returns:
            {:class:`~macop.solutions.base.Solution`}: clone of current solution
        """
        copy_solution = deepcopy(self)
        copy_solution._score = None

        return copy_solution

    def __str__(self):
        print("Generic solution with ", self._data)
