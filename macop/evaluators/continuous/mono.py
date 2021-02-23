"""Mono-objective evaluators classes for continuous problem
"""
# main imports
from macop.evaluators.base import Evaluator


class ZdtEvaluator(Evaluator):
    """Generic Zdt evaluator class which enables to compute custom Zdt function for continuous problem

    - stores into its `_data` dictionary attritute required measures when computing a knapsack solution
    - `_data['f']` stores lambda Zdt function 
    - `compute` method enables to compute and associate a score to a given knapsack solution

    Example:

    >>> import random
    >>>
    >>> # binary solution import
    >>> from macop.solutions.continuous import ContinuousSolution
    >>>
    >>> # evaluator import
    >>> from macop.evaluators.continuous.mono import ZdtEvaluator
    >>> solution_data = [2, 3, 4, 1, 2, 3, 3]
    >>> size = len(solution_data)
    >>> solution = ContinuousSolution(solution_data, size)
    >>>
    >>> # evaluator initialization (Shere function)
    >>> f_sphere = lambda s: sum([ x * x for x in s.data])
    >>> evaluator = ZdtEvaluator(data={'f': f_sphere})
    >>>
    >>> # compute solution score
    >>> evaluator.compute(solution)
    45
    """
    def compute(self, solution):
        """Apply the computation of fitness from solution

        Args:
            solution: {:class:`~macop.solutions.base.Solution`} -- Solution instance
    
        Returns:
            {float}: fitness score of solution
        """
        return self._data['f'](solution)