"""Multi-objective evaluators classes 
"""
# main imports
from macop.evaluators.base import Evaluator


class WeightedSum(Evaluator):
    """Weighted-sum sub-evaluator class which enables to compute solution using specific `_data`

    - stores into its `_data` dictionary attritute required measures when computing a solution
    - `_data['evaluators']` current evaluator to use
    - `_data['weights']` Associated weight to use
    - `compute` method enables to compute and associate a tuples of scores to a given solution
    
    >>> import random
    >>> # binary solution import
    >>> from macop.solutions.discrete import BinarySolution
    >>> # evaluators imports
    >>> from macop.evaluators.discrete.mono import KnapsackEvaluator
    >>> from macop.evaluators.discrete.multi import WeightedSum
    >>> solution_data = [1, 0, 0, 1, 1, 0, 1, 0]
    >>> size = len(solution_data)
    >>> solution = BinarySolution(solution_data, size)
    >>> # evaluator 1 initialization (worths objects passed into data)
    >>> worths1 = [ random.randint(5, 20) for i in range(size) ]
    >>> evaluator1 = KnapsackEvaluator(data={'worths': worths1})
    >>> # evaluator 2 initialization (worths objects passed into data)
    >>> worths2 = [ random.randint(10, 15) for i in range(size) ]
    >>> evaluator2 = KnapsackEvaluator(data={'worths': worths2})
    >>> weighted_evaluator = WeightedSum(data={'evaluators': [evaluator1, evaluator2], 'weights': [0.3, 0.7]})
    >>> weighted_score = weighted_evaluator.compute(solution)
    >>> expected_score = evaluator1.compute(solution) * 0.3 + evaluator2.compute(solution) * 0.7
    >>> weighted_score == expected_score
    True
    >>> weighted_score
    50.8
    """

    def compute(self, solution):
        """Apply the computation of fitness from solution

        - Associate tuple of fitness scores for each objective to the current solution
        - Compute weighted-sum for these objectives

        Args:
            solution: {Solution} -- Solution instance
    
        Returns:
            {float} -- weighted-sum of the fitness scores
        """
        scores = [evaluator.compute(solution) for evaluator in self._data['evaluators']]

        # associate objectives scores to solution
        solution._scores = scores

        return sum([scores[i] * w for i, w in enumerate(self._data['weights'])])