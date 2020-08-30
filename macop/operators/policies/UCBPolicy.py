"""Policy class implementation which is used for selecting operator using Upper Confidence Bound
"""
# main imports
import logging
import random
import math

# module imports
from .Policy import Policy


class UCBPolicy(Policy):
    """UCB policy class which is used for applying UCB strategy when selecting and applying operator 

    Attributes:
        operators: {[Operator]} -- list of selected operators for the algorithm
        C: {float} -- tradeoff between EvE parameter for UCB
        rewards: {[float]} -- list of summed rewards obtained for each operator
        occurences: {[int]} -- number of use (selected) of each operator
    """
    def __init__(self, _operators, _C=100.):
        self.operators = _operators
        self.rewards = [0. for o in self.operators]
        self.occurences = [0 for o in self.operators]
        self.C = _C

    def select(self):
        """Select randomly the next operator to use

        Returns:
            {Operator}: the selected operator
        """

        indices = [i for i, o in enumerate(self.occurences) if o == 0]

        # if operator have at least be used one time
        if len(indices) == 0:

            ucbValues = []
            nVisits = sum(self.occurences)

            for i in range(len(self.operators)):

                ucbValue = self.rewards[i] + self.C * math.sqrt(
                    math.log(nVisits) / self.occurences[i])
                ucbValues.append(ucbValue)

            return self.operators[ucbValues.index(max(ucbValues))]

        else:
            return self.operators[random.choice(indices)]

    def apply(self, _solution):
        """
        Apply specific operator chosen to create new solution, computes its fitness and returns solution
        
        Args:
            _solution: {Solution} -- the solution to use for generating new solution

        Returns:
            {Solution} -- new generated solution
        """

        operator = self.select()

        logging.info("---- Applying %s on %s" %
                     (type(operator).__name__, _solution))

        # apply operator on solution
        newSolution = operator.apply(_solution)

        # compute fitness of new solution
        newSolution.evaluate(self.algo.evaluator)

        # compute fitness improvment rate
        if self.algo.maximise:
            fir = (newSolution.fitness() -
                   _solution.fitness()) / _solution.fitness()
        else:
            fir = (_solution.fitness() -
                   newSolution.fitness()) / _solution.fitness()

        if fir > 0:
            operator_index = self.operators.index(operator)
            self.rewards[operator_index] += fir
            self.occurences[operator_index] += 1

        logging.info("---- Obtaining %s" % (_solution))

        return newSolution
