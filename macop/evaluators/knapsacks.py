"""Knapsack evaluators classes
"""
# main imports
from abc import abstractmethod
from .base import Evaluator


class KnapsackEvaluator(Evaluator):
    """Knapsack evaluator class which enables to compute solution using specific `_data`

    - stores into its `_data` dictionary attritute required measures when computing a knapsack solution
    - `_data['worths']` stores knapsack objects worths information
    - `_data['weights']` stores knapsack objects weights information
    - `compute` method enables to compute and associate a score to a given knapsack solution
    """

    def compute(self, solution):
        """Apply the computation of fitness from solution

        Args:
            solution: {Solution} -- Solution instance
    
        Returns:
            {float} -- fitness score of solution
        """
        fitness = 0
        for index, elem in enumerate(solution._data):
            fitness += self._data['worths'][index] * elem

        return fitness


class KnapsackMultiEvaluator(Evaluator):
    """Knapsack multi-objective evaluator class which enables to compute solution using specific `_data` 

    - stores into its `_data` dictionary attritute required measures when computing a knapsack solution
    - `_data['worths1']` stores knapsack objects worths information
    - `_data['worths2']` stores knapsack objects worths information
    - `_data['weights']` stores knapsack objects weights information
    - `compute` method enables to compute and associate a score to a given knapsack solution
    """

    def compute(self, solution):
        """Apply the computation of fitness from solution

        Args:
            solution: {Solution} -- Solution instance
    
        Returns:
            {float} -- fitness score of solution
        """
        fitness = 0
        for index, elem in enumerate(solution._data):
            fitness += self._data['worths1'][index] * elem

        return fitness