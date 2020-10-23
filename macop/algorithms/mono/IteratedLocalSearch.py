"""Iterated Local Search Algorithm implementation
"""

# main imports
import logging

# module imports
from ..Algorithm import Algorithm
from .LocalSearch import LocalSearch


class IteratedLocalSearch(Algorithm):
    """Iterated Local Search used to avoid local optima and increave EvE (Exploration vs Exploitation) compromise

    Attributes:
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
    def run(self, _evaluations, _ls_evaluations=100):
        """
        Run the iterated local search algorithm using local search (EvE compromise)

        Args:
            _evaluations: {int} -- number of global evaluations for ILS
            _ls_evaluations: {int} -- number of Local search evaluations (default: 100)

        Returns:
            {Solution} -- best solution found
        """

        # by default use of mother method to initialize variables
        super().run(_evaluations)

        # enable resuming for ILS
        self.resume()

        # initialize current solution
        self.initRun()

        # passing global evaluation param from ILS
        ls = LocalSearch(self.initializer,
                         self.evaluator,
                         self.operators,
                         self.policy,
                         self.validator,
                         self.maximise,
                         _parent=self)

        # add same callbacks
        for callback in self.callbacks:
            ls.addCallback(callback)

        # local search algorithm implementation
        while not self.stop():

            # create and search solution from local search
            newSolution = ls.run(_ls_evaluations)

            # if better solution than currently, replace it
            if self.isBetter(newSolution):
                self.bestSolution = newSolution

            # number of evaluatins increased from LocalSearch
            # increase number of evaluations and progress are then not necessary there
            #self.increaseEvaluation()
            #self.progress()

            self.information()

        logging.info("End of %s, best solution found %s" %
                     (type(self).__name__, self.bestSolution))

        self.end()
        return self.bestSolution
