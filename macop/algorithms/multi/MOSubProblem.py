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
        maximise: {bool} -- specify kind of optimisation problem 
        currentSolution: {Solution} -- current solution managed for current evaluation
        bestSolution: {Solution} -- best solution found so far during running algorithm
        callbacks: {[Callback]} -- list of Callback class implementation to do some instructions every number of evaluations and `load` when initializing algorithm
    """
    def __init__(self,
                 index,
                 weights,
                 initalizer,
                 evaluator,
                 operators,
                 policy,
                 validator,
                 maximise=True,
                 parent=None):

        super().__init__(initalizer, evaluator, operators, policy,
                         validator, maximise, parent)

        self._index = index
        self._weights = weights

    def run(self, evaluations):
        """
        Run the local search algorithm

        Args:
            evaluations: {int} -- number of evaluations
            
        Returns:
            {Solution} -- best solution found
        """

        # by default use of mother method to initialize variables
        super().run(evaluations)

        # initialize solution if necessary
        if self._bestSolution is None:
            self.initRun()

        # new operators list keep track of current sub problem
        for op in self._operators:
            op.setAlgo(self)

        for _ in range(evaluations):

            # keep reference of sub problem used
            self._policy.setAlgo(self)

            # update solution using policy
            newSolution = self.update(self._bestSolution)

            # if better solution than currently, replace it
            if self.isBetter(newSolution):
                self._bestSolution = newSolution

            # increase number of evaluations
            self.increaseEvaluation()

            self.progress()

            # stop algorithm if necessary
            if self.stop():
                break

            logging.info(f"---- Current {newSolution} - SCORE {newSolution.fitness()}")

            logging.info(f"End of {type(self).__name__}, best solution found {self._bestSolution}")

        return self._bestSolution
