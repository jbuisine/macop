"""Multi-objective evaluators classes 
"""
# main imports
from .base import Evaluator


class WeightedSum(Evaluator):
    """Weighted-sum sub-evaluator class which enables to compute solution using specific `_data`

    - stores into its `_data` dictionary attritute required measures when computing a solution
    - `_data['evaluators']` current evaluator to use
    - `_data['weights']` Associated weight to use
    - `compute` method enables to compute and associate a tuples of scores to a given solution
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

        return sum([scores[i] for i, w in enumerate(self._data['weights'])])