"""Knapsack evaluators classes
"""
# main imports
from macop.evaluators.base import Evaluator


class KnapsackEvaluator(Evaluator):
    """Knapsack evaluator class which enables to compute solution using specific `_data`

    - stores into its `_data` dictionary attritute required measures when computing a knapsack solution
    - `_data['worths']` stores knapsack objects worths information
    - `compute` method enables to compute and associate a score to a given knapsack solution

    Example:

    >>> import random
    >>> # binary solution import
    >>> from macop.solutions.discrete import BinarySolution
    >>> # evaluator import
    >>> from macop.evaluators.discrete.mono import KnapsackEvaluator
    >>> solution_data = [1, 0, 0, 1, 1, 0, 1, 0]
    >>> size = len(solution_data)
    >>> solution = BinarySolution(solution_data, size)
    >>> # evaluator initialization (worths objects passed into data)
    >>> worths = [ random.randint(5, 20) for i in range(size) ]
    >>> evaluator = KnapsackEvaluator(data={'worths': worths})
    >>> # compute solution score
    >>> evaluator.compute(solution)
    40
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