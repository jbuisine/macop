# main imports
import logging


# Generic algorithm class
class Algorithm():
    def __init__(self,
                 _initalizer,
                 _evaluator,
                 _operators,
                 _policy,
                 _validator,
                 _maximise=True,
                 _parent=None):
        """
        Initialize all usefull parameters for problem to solve
        """

        self.initializer = _initalizer
        self.evaluator = _evaluator
        self.operators = _operators
        self.validator = _validator
        self.policy = _policy
        self.checkpoint = None
        self.bestSolution = None

        # other parameters
        self.parent = _parent  # parent algorithm if it's sub algorithm
        #self.maxEvaluations = 0 # by default
        self.maximise = _maximise

        self.initRun()

    def addCheckpoint(self, _class, _every, _filepath):
        self.checkpoint = _class(self, _every, _filepath)

    def setCheckpoint(self, _checkpoint):
        self.checkpoint = _checkpoint

    def resume(self):
        if self.checkpoint is None:
            raise ValueError(
                "Need to `addCheckpoint` or `setCheckpoint` is you want to use this process"
            )
        else:
            print('Checkpoint loading is called')
            self.checkpoint.load()

    def initRun(self):
        """
        Reinit the whole variables
        """

        # add track reference of algo into operator (keep an eye into best solution)
        for operator in self.operators:
            operator.setAlgo(self)

        self.currentSolution = self.initializer()

        # evaluate current solution
        self.currentSolution.evaluate(self.evaluator)

        # keep in memory best known solution (current solution)
        self.bestSolution = self.currentSolution

    def increaseEvaluation(self):
        self.numberOfEvaluations += 1

        if self.parent is not None:
            self.parent.numberOfEvaluations += 1

    def getGlobalEvaluation(self):

        if self.parent is not None:
            return self.parent.numberOfEvaluations

        return self.numberOfEvaluations

    def stop(self):
        """
        Global stopping criteria (check for inner algorithm too)
        """
        if self.parent is not None:
            return self.parent.numberOfEvaluations >= self.parent.maxEvaluations or self.numberOfEvaluations >= self.maxEvaluations

        return self.numberOfEvaluations >= self.maxEvaluations

    def evaluate(self, solution):
        """
        Returns: 
            fitness score of solution which is not already evaluated or changed

        Note: 
            if multi-objective problem this method can be updated using array of `evaluator`
        """
        return solution.evaluate(self.evaluator)

    def update(self, solution):
        """
        Apply update function to solution using specific `policy`

        Check if solution is valid after modification and returns it

        Returns:
            updated solution
        """

        # two parameters are sent if specific crossover solution are wished
        sol = self.policy.apply(solution)

        if (sol.isValid(self.validator)):
            return sol
        else:
            logging.info("-- New solution is not valid %s" % sol)
            return solution

    def isBetter(self, solution):
        """
        Check if solution is better than best found

        Returns:
            `True` if better
        """
        # depending of problem to solve (maximizing or minimizing)
        if self.maximise:
            if self.evaluate(solution) > self.bestSolution.fitness():
                return True
        else:
            if self.evaluate(solution) < self.bestSolution.fitness():
                return True

        # by default
        return False

    def run(self, _evaluations):
        """
        Run the specific algorithm following number of evaluations to find optima
        """

        self.maxEvaluations = _evaluations

        self.initRun()

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

        if self.checkpoint is not None:
            self.checkpoint.run()

        logging.info("-- %s evaluation %s of %s (%s%%) - BEST SCORE %s" %
                     (type(self).__name__, self.numberOfEvaluations,
                      self.maxEvaluations, "{0:.2f}".format(
                          (self.numberOfEvaluations) / self.maxEvaluations *
                          100.), self.bestSolution.fitness()))

    def information(self):
        logging.info("-- Best %s - SCORE %s" %
                     (self.bestSolution, self.bestSolution.fitness()))

    def __str__(self):
        return "%s using %s" % (type(self).__name__, type(
            self.bestSolution).__name__)
