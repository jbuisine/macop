# main imports 
import logging

# module imports
from .Algorithm import Algorithm
from.LocalSearch import LocalSearch

class IteratedLocalSearch(Algorithm):

    def run(self, _evaluations, _ls_evaluations=100):

        # by default use of mother method to initialize variables
        super().run(_evaluations)

        # enable checkpoint for ILS
        if self.checkpoint is not None:
            self.resume()

        # passing global evaluation param from ILS
        ls = LocalSearch(self.initializer, self.evaluator, self.operators, self.policy, self.validator, self.maximise, _parent=self)
        
        # set same checkpoint if exists
        if self.checkpoint is not None:
            ls.setCheckpoint(self.checkpoint)

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

        logging.info("End of %s, best solution found %s" % (type(self).__name__, self.bestSolution))

        return self.bestSolution
