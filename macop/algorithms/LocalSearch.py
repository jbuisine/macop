"""Local Search algorithm
"""

# main imports
import logging

# module imports
from .Algorithm import Algorithm


class LocalSearch(Algorithm):
    """Local Search used as exploitation optimization algorithm

    Attributes:
        initalizer: {function} -- basic function strategy to initialize solution
        evaluator: {function} -- basic function in order to obtained fitness (mono or multiple objectives)
        operators: {[Operator]} -- list of operator to use when launching algorithm
        policy: {Policy} -- Policy class implementation strategy to select operators
        validator: {function} -- basic function to check if solution is valid or not under some constraints
        maximise: {bool} -- specify kind of optimization problem 
        currentSolution: {Solution} -- current solution managed for current evaluation
        bestSolution: {Solution} -- best solution found so far during running algorithm
        checkpoint: {Checkpoint} -- Checkpoint class implementation to keep track of algorithm and restart
    """
    def run(self, _evaluations):
        """
        Run the local search algorithm

        Args:
            _evaluations: {int} -- number of Local search evaluations
            
        Returns:
            {Solution} -- best solution found
        """

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
