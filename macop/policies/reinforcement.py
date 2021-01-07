"""Reinforcement learning policy classes implementations for Operator Selection Strategy
"""
# main imports
import logging
import random
import math
import numpy as np

# module imports
from macop.policies.base import Policy
from macop.operators.base import KindOperator


class UCBPolicy(Policy):
    """Upper Confidence Bound (UCB) policy class which is used for applying UCB strategy when selecting and applying operator

    Rather than performing exploration by simply selecting an arbitrary action, chosen with a probability that remains constant,
    the UCB algorithm changes its exploration-exploitation balance as it gathers more knowledge of the environment.
    It moves from being primarily focused on exploration, when actions that have been tried the least are preferred,
    to instead concentrate on exploitation, selecting the action with the highest estimated reward.

    - Resource link: https://banditalgs.com/2016/09/18/the-upper-confidence-bound-algorithm/

    Attributes:
        operators: {[Operator]} -- list of selected operators for the algorithm
        C: {float} -- The second half of the UCB equation adds exploration, with the degree of exploration being controlled by the hyper-parameter `C`.
        exp_rate: {float} -- exploration rate (probability to choose randomly next operator)
        rewards: {[float]} -- list of summed rewards obtained for each operator
        occurrences: {[int]} -- number of use (selected) of each operator

    Example:

    >>> # operators import
    >>> from macop.operators.discrete.crossovers import SimpleCrossover
    >>> from macop.operators.discrete.mutators import SimpleMutation
    >>> # policy import
    >>> from macop.policies.reinforcement import UCBPolicy
    >>> # solution and algorithm
    >>> from macop.solutions.discrete import BinarySolution
    >>> from macop.algorithms.mono import IteratedLocalSearch
    >>> from macop.algorithms.mono import HillClimberFirstImprovment
    >>> # evaluator import
    >>> from macop.evaluators.discrete.mono import KnapsackEvaluator
    >>> # evaluator initialization (worths objects passed into data)
    >>> worths = [ random.randint(0, 20) for i in range(20) ]
    >>> evaluator = KnapsackEvaluator(data={'worths': worths})
    >>> # validator specification (based on weights of each objects)
    >>> weights = [ random.randint(5, 30) for i in range(20) ]
    >>> validator = lambda solution: True if sum([weights[i] for i, value in enumerate(solution._data) if value == 1]) < 200 else False
    >>> # initializer function with lambda function
    >>> initializer = lambda x=20: BinarySolution.random(x, validator)
    >>> # operators list with crossover and mutation
    >>> operators = [SimpleCrossover(), SimpleMutation()]
    >>> policy = UCBPolicy(operators)
    >>> local_search = HillClimberFirstImprovment(initializer, evaluator, operators, policy, validator, maximise=True, verbose=False)
    >>> algo = IteratedLocalSearch(initializer, evaluator, operators, policy, validator, localSearch=local_search, maximise=True, verbose=False)
    >>> policy._occurences
    [0, 0]
    >>> solution = algo.run(100)
    >>> type(solution).__name__
    'BinarySolution'
    >>> policy._occurences # one more due to first evaluation
    [51, 53]
    """
    def __init__(self, operators, C=100., exp_rate=0.5):
        self._operators = operators
        self._rewards = [0. for o in self._operators]
        self._occurences = [0 for o in self._operators]
        self._C = C
        self._exp_rate = exp_rate


    def select(self):
        """Select using Upper Confidence Bound the next operator to use (using acquired rewards)

        Returns:
            {Operator}: the selected operator
        """

        indices = [i for i, o in enumerate(self._occurences) if o == 0]

        # random choice following exploration rate
        if np.random.uniform(0, 1) <= self._exp_rate:

            index = random.choice(range(len(self._operators)))
            return self._operators[index]

        elif len(indices) == 0:

            # if operator have at least be used one time
            ucbValues = []
            nVisits = sum(self._occurences)

            for i in range(len(self._operators)):

                ucbValue = self._rewards[i] + self._C * math.sqrt(
                    math.log(nVisits) / (self._occurences[i] + 0.1))
                ucbValues.append(ucbValue)

            return self._operators[ucbValues.index(max(ucbValues))]

        else:
            return self._operators[random.choice(indices)]

    def apply(self, solution1, solution2=None):
        """
        Apply specific operator chosen to create new solution, computes its fitness and returns solution

        - fitness improvment is saved as rewards
        - selected operator occurence is also increased

        Args:
            solution1: {Solution} -- the first solution to use for generating new solution
            solution2: {Solution} -- the second solution to use for generating new solution (in case of specific crossover, default is best solution from algorithm)

        Returns:
            {Solution} -- new generated solution
        """

        operator = self.select()

        logging.info("---- Applying %s on %s" %
                     (type(operator).__name__, solution1))

        # default value of solution2 is current best solution
        if solution2 is None and self._algo is not None:
            solution2 = self._algo._bestSolution

        # avoid use of crossover if only one solution is passed
        if solution2 is None and operator._kind == KindOperator.CROSSOVER:

            while operator._kind == KindOperator.CROSSOVER:            
                operator = self.select()

        # apply operator on solution
        if operator._kind == KindOperator.CROSSOVER:
            newSolution = operator.apply(solution1, solution2)
        else:
            newSolution = operator.apply(solution1)

        # compute fitness of new solution
        newSolution.evaluate(self._algo._evaluator)

        # compute fitness improvment rate
        if self._algo._maximise:
            fir = (newSolution.fitness() -
                   solution1.fitness()) / solution1.fitness()
        else:
            fir = (solution1.fitness() -
                   newSolution.fitness()) / solution1.fitness()

        operator_index = self._operators.index(operator)

        if fir > 0:
            self._rewards[operator_index] += fir

        self._occurences[operator_index] += 1

        logging.info("---- Obtaining %s" % (newSolution))

        return newSolution
