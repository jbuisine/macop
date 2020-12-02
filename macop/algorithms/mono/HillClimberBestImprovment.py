"""Hill Climber Best Improvment algorithm starting from new solution and explore using neighborhood and loop over the best one obtained from neighborhood search space
"""

# main imports
import logging

# module imports
from ..Algorithm import Algorithm


class HillClimberBestImprovment(Algorithm):
    """Hill Climber Best Improvment used as exploitation optimisation algorithm

    This algorithm do a neighborhood exploration of a new generated solution (by doing operation on the current solution obtained) in order to find the best solution from the neighborhood space.
    Then replace the best solution found from the neighbordhood space as current solution to use.
    Do these steps until a number of evaluation (stopping criterion) is reached.

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
    def run(self, evaluations):
        """
        Run the local search algorithm

        Args:
            evaluations: {int} -- number of Local search evaluations
            
        Returns:
            {Solution} -- best solution found
        """

        # by default use of mother method to initialize variables
        super().run(evaluations)

        # initialize current solution and best solution
        self.initRun()

        solutionSize = self._currentSolution.size

        # local search algorithm implementation
        while not self.stop():

            for _ in range(solutionSize):

                # update current solution using policy
                newSolution = self.update(self._currentSolution)

                # if better solution than currently, replace it
                if self.isBetter(newSolution):
                    self._bestSolution = newSolution

                # increase number of evaluations
                self.increaseEvaluation()

                self.progress()
                logging.info(f"---- Current {newSolution} - SCORE {newSolution.fitness()}")

                # stop algorithm if necessary
                if self.stop():
                    break

            # set new current solution using best solution found in this neighbor search
            self._currentSolution = self._bestSolution

        logging.info(f"End of {type(self).__name__}, best solution found {self._bestSolution}")

        return self._bestSolution
