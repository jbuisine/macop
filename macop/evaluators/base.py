"""Abstract Evaluator class for computing fitness score associated to a solution

- stores into its `_data` dictionary attritute required measures when computing a solution
- `compute` abstract method enable to compute and associate a score to a given solution
"""
# main imports
from abc import abstractmethod


class Evaluator():
    """Abstract Evaluator class which enables to compute solution using specific `_data` 
    """
    def __init__(self, data: dict):
        """Initialise Evaluator instance which stores into its `_data` dictionary attritute required measures when computing a solution
        Args:
            data: {dict} -- specific data dictionnary
        """
        self._data = data

    @abstractmethod
    def compute(self, solution):
        """Apply the computation of fitness from solution

        Fitness is a float value for mono-objective or set of float values if multi-objective evaluation

        Args:
            solution: {:class:`~macop.solutions.base.Solution`} -- Solution instance

        Return:
            {float} -- computed solution score (float or set of float if multi-objective evaluation)
        """
        pass

    def setAlgo(self, algo):
        """Keep into evaluator reference of the whole algorithm
           The reason is to better manage evaluator instance if necessary

        Args:
            algo: {:class:`~macop.algorithms.base.Algorithm`} -- the algorithm reference runned
        """
        self._algo = algo
