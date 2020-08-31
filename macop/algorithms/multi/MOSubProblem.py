"""MOEAD sub problem algorithm class
"""

# main imports
import logging

# module imports
from ..Algorithm import Algorithm


class MOSubProblem(Algorithm):
    """Specific MO sub problem used into MOEAD

    Attributes:
        index: {int} -- sub problem index
        weights: {[float]} -- sub problems objectives weights
        initalizer: {function} -- basic function strategy to initialize solution
        evaluator: {function} -- basic function in order to obtained fitness (mono or multiple objectives)
        operators: {[Operator]} -- list of operator to use when launching algorithm
        policy: {Policy} -- Policy class implementation strategy to select operators
        validator: {function} -- basic function to check if solution is valid or not under some constraints
        maximise: {bool} -- specify kind of optimization problem 
        currentSolution: {Solution} -- current solution managed for current evaluation
        bestSolution: {Solution} -- best solution found so far during running algorithm
        callbacks: {[Callback]} -- list of Callback class implementation to do some instructions every number of evaluations and `load` when initializing algorithm
    """
    def __init__(self,
                 _index,
                 _weights,
                 _initalizer,
                 _evaluator,
                 _operators,
                 _policy,
                 _validator,
                 _maximise=True,
                 _parent=None):

        super().__init__(_initalizer, _evaluator, _operators, _policy,
                         _validator, _maximise, _parent)

        self.index = _index
        self.weights = _weights

    def run(self, _evaluations):
        """
        Run the local search algorithm

        Args:
            _evaluations: {int} -- number of evaluations
            
        Returns:
            {Solution} -- best solution found
        """

        # by default use of mother method to initialize variables
        super().run(_evaluations)

        for _ in range(_evaluations):
            # update solution using policy
            newSolution = self.update(self.bestSolution)

            # if better solution than currently, replace it
            if self.isBetter(newSolution):
                self.bestSolution = newSolution

            # increase number of evaluations
            self.increaseEvaluation()

            self.progress()

            # stop algorithm if necessary
            if self.stop():
                break

            logging.info("---- Current %s - SCORE %s" %
                         (newSolution, newSolution.fitness()))

            logging.info("End of %s, best solution found %s" %
                         (type(self).__name__, self.bestSolution))

        return self.bestSolution
