# main imports
import logging

# module imports
from .Algorithm import Algorithm


class LocalSearch(Algorithm):
    def run(self, _evaluations):

        # by default use of mother method to initialize variables
        super().run(_evaluations)

        solutionSize = self.bestSolution.size

        # local search algorithm implementation
        while not self.stop():

            for _ in range(solutionSize):

                # update solution using policy
                newSolution = self.update(self.bestSolution)

                # if better solution than currently, replace it
                if self.isBetter(newSolution):
                    self.bestSolution = newSolution

                # increase number of evaluations
                self.increaseEvaluation()

                self.progress()
                logging.info("---- Current %s - SCORE %s" %
                             (newSolution, newSolution.fitness()))

                # stop algorithm if necessary
                if self.stop():
                    break

        logging.info("End of %s, best solution found %s" %
                     (type(self).__name__, self.bestSolution))

        return self.bestSolution
