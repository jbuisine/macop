"""Mono-objective available algorithms
"""

# main imports
import logging

# module imports
from .base import Algorithm


class HillClimberFirstImprovment(Algorithm):
    """Hill Climber First Improvment used as quick exploration optimisation algorithm

    - First, this algorithm do a neighborhood exploration of a new generated solution (by doing operation on the current solution obtained) in order to find a better solution from the neighborhood space.
    - Then replace the current solution by the first one from the neighbordhood space which is better than the current solution.
    - And do these steps until a number of evaluation (stopping criterion) is reached.

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

        solutionSize = self._currentSolution._size

        # local search algorithm implementation
        while not self.stop():

            for _ in range(solutionSize):

                # update current solution using policy
                newSolution = self.update(self._currentSolution)

                # if better solution than currently, replace it and stop current exploration (first improvment)
                if self.isBetter(newSolution):
                    self._bestSolution = newSolution
                    break

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
        
        self.end()

        return self._bestSolution


class HillClimberBestImprovment(Algorithm):
    """Hill Climber Best Improvment used as exploitation optimisation algorithm

    - First, this algorithm do a neighborhood exploration of a new generated solution (by doing operation on the current solution obtained) in order to find the best solution from the neighborhood space.
    - Then replace the best solution found from the neighbordhood space as current solution to use.
    - And do these steps until a number of evaluation (stopping criterion) is reached.

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

        solutionSize = self._currentSolution._size

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

        self.end()
        
        return self._bestSolution


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
    def run(self, evaluations, ls_evaluations=100):
        """
        Run the iterated local search algorithm using local search (EvE compromise)

        Args:
            evaluations: {int} -- number of global evaluations for ILS
            ls_evaluations: {int} -- number of Local search evaluations (default: 100)

        Returns:
            {Solution} -- best solution found
        """

        # by default use of mother method to initialize variables
        super().run(evaluations)

        # enable resuming for ILS
        self.resume()

        # initialize current solution
        self.initRun()

        # passing global evaluation param from ILS
        ls = HillClimberFirstImprovment(self._initializer,
                         self._evaluator,
                         self._operators,
                         self._policy,
                         self._validator,
                         self._maximise,
                         parent=self)

        # add same callbacks
        for callback in self._callbacks:
            ls.addCallback(callback)

        # local search algorithm implementation
        while not self.stop():

            # create and search solution from local search
            newSolution = ls.run(ls_evaluations)

            # if better solution than currently, replace it
            if self.isBetter(newSolution):
                self._bestSolution = newSolution

            # number of evaluatins increased from LocalSearch
            # increase number of evaluations and progress are then not necessary there
            #self.increaseEvaluation()
            #self.progress()

            self.information()

        logging.info(f"End of {type(self).__name__}, best solution found {self._bestSolution}")
        
        self.end()

        return self._bestSolution
