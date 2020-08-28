"""Abstract Algorithm class used as basic algorithm implementation with some specific initialization
"""

# main imports
import logging
from ..utils.color import macop_text, macop_line, macop_progress


# Generic algorithm class
class Algorithm():
    """Algorithm class used as basic algorithm

    Attributes:
        initalizer: {function} -- basic function strategy to initialize solution
        evaluator: {function} -- basic function in order to obtained fitness (mono or multiple objectives)
        operators: {[Operator]} -- list of operator to use when launching algorithm
        policy: {Policy} -- Policy class implementation strategy to select operators
        validator: {function} -- basic function to check if solution is valid or not under some constraints
        maximise: {bool} -- specify kind of optimization problem 
        currentSolution: {Solution} -- current solution managed for current evaluation
        bestSolution: {Solution} -- best solution found so far during running algorithm
        callbacks: {[Callback]} -- list of Callback class implementation to do some instructions every number of evaluations and `load` when initializing algorithm
        parent: {Algorithm} -- parent algorithm reference in case of inner Algorithm instance (optional)
    """
    def __init__(self,
                 _initalizer,
                 _evaluator,
                 _operators,
                 _policy,
                 _validator,
                 _maximise=True,
                 _parent=None):

        self.initializer = _initalizer
        self.evaluator = _evaluator
        self.operators = _operators
        self.policy = _policy
        self.validator = _validator
        self.callbacks = []
        self.bestSolution = None

        # by default
        self.numberOfEvaluations = 0
        self.maxEvaluations = 0

        # other parameters
        self.parent = _parent  # parent algorithm if it's sub algorithm

        #self.maxEvaluations = 0 # by default
        self.maximise = _maximise

        # track reference of algo into operator (keep an eye into best solution)
        for operator in self.operators:
            operator.setAlgo(self)

        # also track reference for policy
        self.policy.setAlgo(self)

        self.initRun()

    def addCallback(self, _callback):
        """Add new callback to algorithm specifying usefull parameters

        Args:
            _callback: {Callback} -- specific Callback instance
        """
        # specify current main algorithm reference
        _callback.setAlgo(self)

        # set as new
        self.callbacks.append(_callback)

    def setCheckpoint(self, _callback):
        """Set checkpoint instance directly
        Args:
            _callback: {Callback} -- Callback instance used for checkpoint
        """
        # specify current main algorithm reference if necessary
        if _callback.algo is None:
            _callback.setAlgo(self)

        # set as checkpoint
        self.checkpoint = _callback

    def resume(self):
        """Resume algorithm using Callback instances
        """

        # load every callback if many things are necessary to do before running algorithm
        for callback in self.callbacks:
            callback.load()

    def initRun(self):
        """
        Initialize the current solution and best solution
        """

        self.currentSolution = self.initializer()

        # evaluate current solution
        self.currentSolution.evaluate(self.evaluator)

        # keep in memory best known solution (current solution)
        self.bestSolution = self.currentSolution

    def increaseEvaluation(self):
        """
        Increase number of evaluation once a solution is evaluated
        """
        self.numberOfEvaluations += 1

        if self.parent is not None:
            self.parent.numberOfEvaluations += 1

    def getGlobalEvaluation(self):
        """Get the global number of evaluation (if inner algorithm)

        Returns:
            {int} -- current global number of evaluation
        """

        if self.parent is not None:
            return self.parent.numberOfEvaluations

        return self.numberOfEvaluations

    def getGlobalMaxEvaluation(self):
        """Get the global max number of evaluation (if inner algorithm)

        Returns:
            {int} -- current global max number of evaluation
        """

        if self.parent is not None:
            return self.parent.maxEvaluations

        return self.maxEvaluations

    def stop(self):
        """
        Global stopping criteria (check for inner algorithm too)
        """
        if self.parent is not None:
            return self.parent.numberOfEvaluations >= self.parent.maxEvaluations or self.numberOfEvaluations >= self.maxEvaluations

        return self.numberOfEvaluations >= self.maxEvaluations

    def evaluate(self, _solution):
        """
        Evaluate a solution using evaluator passed when intialize algorithm

        Args:
            solution: {Solution} -- solution to evaluate

        Returns: 
            fitness score of solution which is not already evaluated or changed

        Note: 
            if multi-objective problem this method can be updated using array of `evaluator`
        """
        return _solution.evaluate(self.evaluator)

    def update(self, _solution):
        """
        Apply update function to solution using specific `policy`
        Check if solution is valid after modification and returns it
        
        Args:
            solution: {Solution} -- solution to update using current policy

        Returns:
            {Solution} -- updated solution obtained by the selected operator
        """

        # two parameters are sent if specific crossover solution are wished
        sol = self.policy.apply(_solution)

        if (sol.isValid(self.validator)):
            return sol
        else:
            logging.info("-- New solution is not valid %s" % sol)
            return _solution

    def isBetter(self, _solution):
        """
        Check if solution is better than best found

        Args:
            solution: {Solution} -- solution to compare with best one

        Returns:
            {bool} -- `True` if better
        """
        # depending of problem to solve (maximizing or minimizing)
        if self.maximise:
            if _solution.fitness() > self.bestSolution.fitness():
                return True
        else:
            if _solution.fitness() < self.bestSolution.fitness():
                return True

        # by default
        return False

    def run(self, _evaluations):
        """
        Run the specific algorithm following number of evaluations to find optima
        """

        # append number of max evaluation if multiple run called
        self.maxEvaluations += _evaluations

        # check if global evaluation is used or not
        if self.parent is not None and self.getGlobalEvaluation() != 0:

            # init number evaluations of inner algorithm depending of globalEvaluation
            # allows to restart from `checkpoint` last evaluation into inner algorithm
            rest = self.getGlobalEvaluation() % self.maxEvaluations
            self.numberOfEvaluations = rest

        else:
            self.numberOfEvaluations = 0

        logging.info("Run %s with %s evaluations" %
                     (self.__str__(), _evaluations))

    def progress(self):
        """
        Log progress and apply callbacks if necessary
        """
        if len(self.callbacks) > 0:
            for callback in self.callbacks:
                callback.run()

        macop_progress(self.getGlobalEvaluation(),
                       self.getGlobalMaxEvaluation())

        logging.info("-- %s evaluation %s of %s (%s%%) - BEST SCORE %s" %
                     (type(self).__name__, self.numberOfEvaluations,
                      self.maxEvaluations, "{0:.2f}".format(
                          (self.numberOfEvaluations) / self.maxEvaluations *
                          100.), self.bestSolution.fitness()))

    def end(self):
        """Display end message into `run` method
        """
        print(
            macop_text('({}) Found after {} evaluations \n   - {}'.format(
                type(self).__name__, self.numberOfEvaluations,
                self.bestSolution)))
        print(macop_line())

    def information(self):
        logging.info("-- Best %s - SCORE %s" %
                     (self.bestSolution, self.bestSolution.fitness()))

    def __str__(self):
        return "%s using %s" % (type(self).__name__, type(
            self.bestSolution).__name__)
