"""Policy class implementation which is used for selecting operator using Upper Confidence Bound
"""
# main imports
import logging
import random
import math
import numpy as np

# module imports
from .Policy import Policy


class UCBPolicy(Policy):
    """UCB policy class which is used for applying UCB strategy when selecting and applying operator 

    Attributes:
        operators: {[Operator]} -- list of selected operators for the algorithm
        C: {float} -- tradeoff between EvE parameter for UCB
        exp_rate: {float} -- exploration rate (probability to choose randomly next operator)
        rewards: {[float]} -- list of summed rewards obtained for each operator
        occurrences: {[int]} -- number of use (selected) of each operator
    """
    def __init__(self, operators, C=100., exp_rate=0.5):
        self._operators = operators
        self._rewards = [0. for o in self._operators]
        self._occurrences = [0 for o in self._operators]
        self._C = C
        self._exp_rate = exp_rate

    def select(self):
        """Select randomly the next operator to use

        Returns:
            {Operator}: the selected operator
        """

        indices = [i for i, o in enumerate(self._occurrences) if o == 0]

        # random choice following exploration rate
        if np.random.uniform(0, 1) <= self._exp_rate:

            index = random.choice(range(len(self._operators)))
            return self._operators[index]

        elif len(indices) == 0:

            # if operator have at least be used one time
            ucbValues = []
            nVisits = sum(self._occurrences)

            for i in range(len(self._operators)):

                ucbValue = self._rewards[i] + self._C * math.sqrt(
                    math.log(nVisits) / (self._occurrences[i] + 0.1))
                ucbValues.append(ucbValue)

            return self._operators[ucbValues.index(max(ucbValues))]

        else:
            return self._operators[random.choice(indices)]

    def apply(self, solution):
        """
        Apply specific operator chosen to create new solution, computes its fitness and returns solution
        
        Args:
            solution: {Solution} -- the solution to use for generating new solution

        Returns:
            {Solution} -- new generated solution
        """

        operator = self.select()

        logging.info("---- Applying %s on %s" %
                     (type(operator).__name__, solution))

        # apply operator on solution
        newSolution = operator.apply(solution)

        # compute fitness of new solution
        newSolution.evaluate(self._algo._evaluator)

        # compute fitness improvment rate
        if self._algo._maximise:
            fir = (newSolution.fitness() -
                   solution.fitness()) / solution.fitness()
        else:
            fir = (solution.fitness() -
                   newSolution.fitness()) / solution.fitness()

        operator_index = self._operators.index(operator)

        if fir > 0:
            self._rewards[operator_index] += fir

        self._occurrences[operator_index] += 1

        logging.info("---- Obtaining %s" % (solution))

        return newSolution
