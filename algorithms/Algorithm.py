import logging

# Generic algorithm class
class Algorithm():

    def __init__(self, _initalizer, _evaluator, _updators, _policy, _validator, _maximise=True):
        """
        Initialize all usefull parameters for problem to solve
        """

        self.initializer = _initalizer
        self.evaluator = _evaluator
        self.updators = _updators
        self.validator = _validator
        self.policy = _policy

        self.currentSolution = self.initializer()
        
        # evaluate current solution
        self.currentSolution.evaluate(self.evaluator)

        # keep in memory best known solution (current solution)
        self.bestSolution = self.currentSolution

        # other parameters
        self.maxEvalutations = 0 # by default
        self.numberOfEvaluations = 0
        self.maximise = _maximise


    def reinit(self):
        """
        Reinit the whole variable
        """
        self.currentSolution = self.initializer
        self.bestSolution = self.currentSolution

        self.numberOfEvaluations = 0


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

        sol = self.policy.apply(solution)

        if(sol.isValid(self.validator)):
            return sol
        else:
            print("New solution is not valid", sol)
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
        self.maxEvalutations = _evaluations

        logging.info("Run %s with %s evaluations" % (self.__str__(), _evaluations))


    def progress(self):
        logging.info("-- Evaluation n°%s of %s, %s%%" % (self.numberOfEvaluations, self.maxEvalutations, "{0:.2f}".format((self.numberOfEvaluations) / self.maxEvalutations * 100.)))


    def information(self):
        logging.info("-- Found %s with score of %s" % (self.bestSolution, self.bestSolution.fitness()))


    def __str__(self):
        return "%s using %s" % (type(self).__name__, type(self.bestSolution).__name__)


