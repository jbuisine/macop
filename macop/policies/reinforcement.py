"""Reinforcement learning policy classes implementations for Operator Selection Strategy
"""
# main imports
import logging
import random
import math
import numpy as np

# module imports
from .base import Policy


class UCBPolicy(Policy):
    """Upper Confidence Bound (UCB) policy class which is used for applying UCB strategy when selecting and applying operator 

    Rather than performing exploration by simply selecting an arbitrary action, chosen with a probability that remains constant, 
    the UCB algorithm changes its exploration-exploitation balance as it gathers more knowledge of the environment. 
    It moves from being primarily focused on exploration, when actions that have been tried the least are preferred, 
    to instead concentrate on exploitation, selecting the action with the highest estimated reward.

    Link: https://banditalgs.com/2016/09/18/the-upper-confidence-bound-algorithm/
    
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
