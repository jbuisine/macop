"""Crossover implementations for discrete solutions kind
"""
# main imports
import random
import sys

# module imports
from ..base import Crossover


class SimpleCrossover(Crossover):
    """Crossover implementation which generated new solution by splitting at mean size best solution and current solution

    Attributes:
        kind: {Algorithm} -- specify the kind of operator

    Example:

    >>> # operators import
    >>> from macop.operators.discrete.crossovers import SimpleCrossover
    >>> from macop.operators.discrete.mutators import SimpleMutation
    >>> # policy import
    >>> from macop.policies.reinforcement import UCBPolicy
    >>> # solution and algorithm
    >>> from macop.solutions.discrete import BinarySolution
    >>> from macop.algorithms.mono import IteratedLocalSearch
    >>> # evaluator import
    >>> from macop.evaluators.discrete.mono import KnapsackEvaluator
    >>> # evaluator initialization (worths objects passed into data)
    >>> worths = [ random.randint(0, 20) for i in range(10) ]
    >>> evaluator = KnapsackEvaluator(data={'worths': worths})
    >>> # validator specification (based on weights of each objects)
    >>> weights = [ random.randint(20, 30) for i in range(10) ]
    >>> validator = lambda solution: True if sum([weights[i] for i, value in enumerate(solution._data) if value == 1]) < 200 else False
    >>> # initializer function with lambda function
    >>> initializer = lambda x=10: BinarySolution.random(x, validator)
    >>> # operators list with crossover and mutation
    >>> simple_crossover = SimpleCrossover()
    >>> simple_mutation = SimpleMutation()
    >>> operators = [simple_crossover, simple_mutation]
    >>> policy = UCBPolicy(operators)
    >>> algo = IteratedLocalSearch(initializer, evaluator, operators, policy, validator, maximise=True, verbose=False)
    >>> # using best solution, simple crossover is applied
    >>> best_solution = algo.run(100)
    >>> list(best_solution._data)
    [1, 1, 0, 1, 0, 1, 1, 1, 0, 1]
    >>> new_solution = initializer()
    >>> mutate_solution = simple_crossover.apply(new_solution)
    >>> list(mutate_solution._data)
    [0, 1, 0, 0, 0, 1, 1, 1, 0, 1]
    """
    def apply(self, solution):
        """Create new solution based on best solution found and solution passed as parameter

        Args:
            solution: {Solution} -- the solution to use for generating new solution

        Returns:
            {Solution} -- new generated solution
        """

        size = solution._size

        # copy data of solution
        firstData = solution._data.copy()

        # get best solution from current algorithm
        copy_solution = self._algo._bestSolution.clone()

        splitIndex = int(size / 2)

        if random.uniform(0, 1) > 0.5:
            copy_solution._data[splitIndex:] = firstData[splitIndex:]
        else:
            copy_solution._data[:splitIndex] = firstData[:splitIndex]

        return copy_solution


class RandomSplitCrossover(Crossover):
    """Crossover implementation which generated new solution by randomly splitting best solution and current solution

    Attributes:
        kind: {KindOperator} -- specify the kind of operator

    Example:

    >>> # operators import
    >>> from macop.operators.discrete.crossovers import RandomSplitCrossover
    >>> from macop.operators.discrete.mutators import SimpleMutation
    >>> # policy import
    >>> from macop.policies.reinforcement import UCBPolicy
    >>> # solution and algorithm
    >>> from macop.solutions.discrete import BinarySolution
    >>> from macop.algorithms.mono import IteratedLocalSearch
    >>> # evaluator import
    >>> from macop.evaluators.discrete.mono import KnapsackEvaluator
    >>> # evaluator initialization (worths objects passed into data)
    >>> worths = [ random.randint(0, 20) for i in range(10) ]
    >>> evaluator = KnapsackEvaluator(data={'worths': worths})
    >>> # validator specification (based on weights of each objects)
    >>> weights = [ random.randint(20, 30) for i in range(10) ]
    >>> validator = lambda solution: True if sum([weights[i] for i, value in enumerate(solution._data) if value == 1]) < 200 else False
    >>> # initializer function with lambda function
    >>> initializer = lambda x=10: BinarySolution.random(x, validator)
    >>> # operators list with crossover and mutation
    >>> random_split_crossover = RandomSplitCrossover()
    >>> simple_mutation = SimpleMutation()
    >>> operators = [random_split_crossover, simple_mutation]
    >>> policy = UCBPolicy(operators)
    >>> algo = IteratedLocalSearch(initializer, evaluator, operators, policy, validator, maximise=True, verbose=False)
    >>> # using best solution, simple crossover is applied
    >>> best_solution = algo.run(100)
    >>> list(best_solution._data)
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0]
    >>> new_solution = initializer()
    >>> mutate_solution = random_split_crossover.apply(new_solution)
    >>> list(mutate_solution._data)
    [1, 0, 0, 1, 1, 0, 0, 1, 0, 0]
    """
    def apply(self, solution):
        """Create new solution based on best solution found and solution passed as parameter

        Args:
            solution: {Solution} -- the solution to use for generating new solution

        Returns:
            {Solution} -- new generated solution
        """
        size = solution._size

        # copy data of solution
        firstData = solution._data.copy()

        # get best solution from current algorithm
        copy_solution = self._algo._bestSolution.clone()

        splitIndex = random.randint(0, size)

        if random.uniform(0, 1) > 0.5:
            copy_solution._data[splitIndex:] = firstData[splitIndex:]
        else:
            copy_solution._data[:splitIndex] = firstData[:splitIndex]

        return copy_solution
