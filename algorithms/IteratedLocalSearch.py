# main imports 
import logging

# module imports
from .Algorithm import Algorithm
from.LocalSearch import LocalSearch

class IteratedLocalSearch(Algorithm):

    def run(self, _evaluations, _lc_evaluations=100):

        # by default use of mother method to initialize variables
        super().run(_evaluations)

        ls = LocalSearch(self.initializer, self.evaluator, self.updators, self.policy, self.validator, self.maximise)

        # local search algorithm implementation
        while self.numberOfEvaluations < self.maxEvalutations:
            
            # create and search solution from local search
            newSolution = ls.run(_lc_evaluations)

            # if better solution than currently, replace it
            if self.isBetter(newSolution):
                self.bestSolution = newSolution

            # increase number of evaluations
            self.numberOfEvaluations += _lc_evaluations

            self.progress()
            self.information()            

        logging.info("End of %s, best solution found %s" % (type(self).__name__, self.bestSolution))

        return self.bestSolution
