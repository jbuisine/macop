"""Mono-objective evaluators classes
"""
# main imports
from macop.evaluators.base import Evaluator


class KnapsackEvaluator(Evaluator):
    """Knapsack evaluator class which enables to compute knapsack solution using specific `_data`

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


class QAPEvaluator(Evaluator):
    """QAP evaluator class which enables to compute qap solution using specific `_data`

    Solutions use for this evaluator are with type of `macop.solutions.discrete.CombinatoryIntegerSolution`

    - stores into its `_data` dictionary attritute required measures when computing a QAP solution
    - `_data['F']` matrix of size n x n with flows data between facilities (stored as numpy array)
    - `_data['D']` matrix of size n x n with distances data between locations (stored as numpy array)
    - `compute` method enables to compute and associate a score to a given QAP solution

    Example:

    >>> import random
    >>> # combinatory solution import
    >>> from macop.solutions.discrete import CombinatoryIntegerSolution
    >>> # evaluator import
    >>> from macop.evaluators.discrete.QAPEvaluator import QAPEvaluator
    >>> # define problem data using QAP example instance
    >>> qap_instance_file = '../../../examples/instances/qap/qap_instance.txt'
    >>> n = 100 # problem size
    >>> size = len(solution_data)
    >>> # loading data
    >>> f = open(qap_instance_file, 'r')
    >>> file_data = f.readlines()
    >>> D_lines = file_data[1:n + 1]
    >>> D_data = ''.join(D_lines).replace('\\n', '')
    >>> F_lines = file_data[n:2 * n + 1]
    >>> F_data = ''.join(F_lines).replace('\\n', '')
    >>> D_matrix = np.fromstring(D_data, dtype=float, sep=' ').reshape(n, n)
    >>> F_matrix = np.fromstring(F_data, dtype=float, sep=' ').reshape(n, n)
    >>> f.close()    
    >>> # create evaluator instance using loading data
    >>> evaluator = QAPEvaluator(data={'F': F_matrix, 'D': D_matrix})
    >>> # create new random combinatory solution using n, the instance QAP size
    >>> solution = CombinatoryIntegerSolution.random(n)
    >>> # compute solution score
    >>> evaluator.compute(solution)
    40
    """
    def compute(self, solution):
        """Apply the computation of fitness from solution

        Args:
            solution: {Solution} -- QAP solution instance
    
        Returns:
            {float} -- fitness score of solution
        """
        fitness = 0
        for index_i, val_i in enumerate(solution._data):
            for index_j, val_j in enumerate(solution._data):
                fitness += self._data['F'][index_i, index_j] * self._data['D'][val_i, val_j]

        return fitness
