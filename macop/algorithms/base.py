"""Basic Algorithm class
"""

# main imports
import logging
import sys, os
from macop.utils.progress import macop_text, macop_line, macop_progress


# Generic algorithm class
class Algorithm():
    """Abstract Algorithm class used as basic algorithm implementation with some specific initialization

    This class enables to manage some common usages of operation research algorithms:
    - initialization function of solution
    - validator function to check if solution is valid or not (based on some criteria)
    - evaluation function to give fitness score to a solution
    - operators used in order to update solution during search process
    - policy process applied when choosing next operator to apply
    - callbacks function in order to do some relative stuff every number of evaluation or reload algorithm state
    - parent algorithm associated to this new algorithm instance (hierarchy management)


    Attributes:
        initialiser: {function} -- basic function strategy to initialise solution
        evaluator: {:class:`~macop.evaluators.base.Evaluator`} -- evaluator instance in order to obtained fitness (mono or multiple objectives)
        operators: {[:class:`~macop.operators.base.Operator`]} -- list of operator to use when launching algorithm
        policy: {:class:`~macop.policies.base.Policy`} -- Policy implementation strategy to select operators
        validator: {function} -- basic function to check if solution is valid or not under some constraints
        maximise: {bool} -- specify kind of optimisation problem 
        verbose: {bool} -- verbose or not information about the algorithm
        currentSolution: {:class:`~macop.solutions.base.Solution`} -- current solution managed for current evaluation comparison
        bestSolution: {:class:`~macop.solutions.base.Solution`} -- best solution found so far during running algorithm
        callbacks: {[:class:`~macop.callbacks.base.Callback`]} -- list of Callback class implementation to do some instructions every number of evaluations and `load` when initialising algorithm
        parent: {:class:`~macop.algorithms.base.Algorithm`} -- parent algorithm reference in case of inner Algorithm instance (optional)
    """
    def __init__(self,
                 initialiser,
                 evaluator,
                 operators,
                 policy,
                 validator,
                 maximise=True,
                 parent=None,
                 verbose=True):
        """Basic Algorithm initialisation

        Args:
            initialiser: {function} -- basic function strategy to initialise solution
            evaluator: {:class:`~macop.evaluators.base.Evaluator`} -- evaluator instance in order to obtained fitness (mono or multiple objectives)
            operators: {[:class:`~macop.operators.base.Operator`]} -- list of operator to use when launching algorithm
            policy: {:class:`~macop.policies.base.Policy`} -- Policy implementation strategy to select operators
            validator: {function} -- basic function to check if solution is valid or not under some constraints
            maximise: {bool} -- specify kind of optimisation problem 
            parent: {:class:`~macop.algorithms.base.Algorithm`} -- parent algorithm reference in case of inner Algorithm instance (optional)
            verbose: {bool} -- verbose or not information about the algorithm
        """

        # public members intialization
        self.initialiser = initialiser
        self.evaluator = evaluator
        self.validator = validator
        self.policy = policy

        # protected members intialization
        self._operators = operators
        self._callbacks = []
        self._bestSolution = None
        self._currentSolution = None

        # by default
        self._numberOfEvaluations = 0
        self._maxEvaluations = 0

        # other parameters
        self._parent = parent  # parent algorithm if it's sub algorithm

        #self.maxEvaluations = 0 # by default
        self._maximise = maximise

        self._verbose = verbose

        # track reference of algorihtm into operator (keep an eye into best solution)
        for operator in self._operators:
            if self._parent is not None:
                operator.setAlgo(self.getParent())
            else:
                operator.setAlgo(self)

        # also track reference for policy
        if self._parent is not None:
            self.policy.setAlgo(self.getParent())
        else:
            self.policy.setAlgo(self)

    def addCallback(self, callback):
        """Add new callback to algorithm specifying usefull parameters

        Args:
            callback: {:class:`~macop.callbacks.base.Callback`} -- specific Callback instance
        """
        # specify current main algorithm reference for callback
        if self._parent is not None:
            callback.setAlgo(self.getParent())
        else:
            callback.setAlgo(self)

        # set as new
        self._callbacks.append(callback)

    def resume(self):
        """Resume algorithm using Callback instances
        """

        # load every callback if many things are necessary to do before running algorithm
        for callback in self._callbacks:
            callback.load()

    def getParent(self):
        """Recursively find the main parent algorithm attached of the current algorithm

        Returns:
            {:class:`~macop.algorithms.base.Algorithm`}: main algorithm set for this algorithm
        """

        current_algorithm = self
        parent_alrogithm = None

        # recursively find the main algorithm parent
        while current_algorithm._parent is not None:
            parent_alrogithm = current_algorithm._parent
            current_algorithm = current_algorithm._parent

        return parent_alrogithm

    def setParent(self, parent):
        """Set parent algorithm to current algorithm

        Args:
            parent: {:class:`~macop.algorithms.base.Algorithm`} -- main algorithm set for this algorithm
        """
        self._parent = parent

    @property
    def result(self):
        """Get the expected result of the current algorithm

        By default the best solution (but can be anything you want)

        Returns:
            {object}: expected result data of the current algorithm
        """
        return self._bestSolution

    @result.setter
    def result(self, result):
        """Set current default result of the algorithm

        Args:
            result: {object} -- expected result data of the current algorithm
        """
        self._bestSolution = result

    def initRun(self):
        """
        initialise the current solution and best solution using the `initialiser` function
        """

        self._currentSolution = self.initialiser()

        # evaluate current solution
        self._currentSolution.evaluate(self.evaluator)
        self.increaseEvaluation()

        # keep in memory best known solution (current solution)
        if self._bestSolution is None:
            self._bestSolution = self._currentSolution

    def increaseEvaluation(self):
        """
        Increase number of evaluation once a solution is evaluated for each dependant algorithm (parents hierarchy)
        """

        current_algorithm = self

        while current_algorithm is not None:

            current_algorithm._numberOfEvaluations += 1
            current_algorithm = current_algorithm._parent

    def getGlobalEvaluation(self):
        """Get the global number of evaluation (if inner algorithm)

        Returns:
            {int}: current global number of evaluation
        """
        parent_algorithm = self.getParent()

        if parent_algorithm is not None:
            return parent_algorithm.getGlobalEvaluation()

        return self._numberOfEvaluations

    def getEvaluation(self):
        """Get the current number of evaluation

        Returns:
            {int}: current number of evaluation
        """
        return self._numberOfEvaluations

    def setEvaluation(self, evaluations):
        """Set the current number of evaluation

        Args:
            evaluations: {int} -- current expected number of evaluation
        """
        self._numberOfEvaluations = evaluations

    def getGlobalMaxEvaluation(self):
        """Get the global max number of evaluation (if inner algorithm)

        Returns:
            {int}: current global max number of evaluation
        """

        parent_algorithm = self.getParent()

        if parent_algorithm is not None:
            return parent_algorithm.getGlobalMaxEvaluation()

        return self._maxEvaluations

    def stop(self):
        """
        Global stopping criteria (check for parents algorithm hierarchy too)
        """
        parent_algorithm = self.getParent()

        # based on global stopping creteria or on its own stopping critera
        if parent_algorithm is not None:
            return parent_algorithm._numberOfEvaluations >= parent_algorithm._maxEvaluations or self._numberOfEvaluations >= self._maxEvaluations

        return self._numberOfEvaluations >= self._maxEvaluations

    def evaluate(self, solution):
        """
        Evaluate a solution using evaluator passed when intialize algorithm

        Args:
            solution: {:class:`~macop.solutions.base.Solution`} -- solution to evaluate

        Returns: 
            {float}: fitness score of solution which is not already evaluated or changed

        Note: 
            if multi-objective problem this method can be updated using array of `evaluator`
        """
        return solution.evaluate(self.evaluator)

    def update(self, solution):
        """
        Apply update function to solution using specific `policy`
        Check if solution is valid after modification and returns it
        
        Args:
            solution: {:class:`~macop.solutions.base.Solution`} -- solution to update using current policy

        Returns:
            {:class:`~macop.solutions.base.Solution`}: updated solution obtained by the selected operator
        """

        # two parameters are sent if specific crossover solution are wished
        sol = self.policy.apply(solution)

        # compute fitness of new solution if not already computed
        if sol._score is None:
            sol.evaluate(self.evaluator)

        if (sol.isValid(self.validator)):
            return sol
        else:
            logging.info("-- New solution is not valid %s" % sol)
            return solution

    def isBetter(self, solution):
        """
        Check if solution is better than best found

        - if the new solution is not valid then the fitness comparison is not done
        - fitness comparison is done using problem nature (maximising or minimising)

        Args:
            solution: {:class:`~macop.solutions.base.Solution`} -- solution to compare with best one

        Returns:
            {bool}:`True` if better
        """
        if not solution.isValid(self.validator):
            return False

        # depending of problem to solve (maximizing or minimizing)
        if self._maximise:
            if solution.fitness > self._bestSolution.fitness:
                return True
        else:
            if solution.fitness < self._bestSolution.fitness:
                return True

        # by default
        return False

    def run(self, evaluations):
        """
        Run the specific algorithm following number of evaluations to find optima
        """

        # append number of max evaluation if multiple run called
        self._maxEvaluations += evaluations

        # check if global evaluation is used or not
        if self.getParent() is not None and self.getGlobalEvaluation() != 0:

            # init number evaluations of inner algorithm depending of globalEvaluation
            # allows to restart from `checkpoint` last evaluation into inner algorithm
            rest = self.getGlobalEvaluation() % self._maxEvaluations
            self._numberOfEvaluations = rest

        else:
            self._numberOfEvaluations = 0

        logging.info(
            f"Run {self.__str__()} with {(self.__str__(), evaluations)} evaluations"
        )

    def progress(self):
        """
        Log progress and apply callbacks if necessary
        """
        if len(self._callbacks) > 0:
            for callback in self._callbacks:
                callback.run()

        if self._verbose:
            macop_progress(self, self.getGlobalEvaluation(),
                           self.getGlobalMaxEvaluation())

        logging.info(
            f"-- {type(self).__name__} evaluation {self._numberOfEvaluations} of {self._maxEvaluations} - BEST SCORE {self._bestSolution._score}"
        )

    def end(self):
        """Display end message into `run` method
        """

        macop_text(
            self,
            f'({type(self).__name__}) Found after {self._numberOfEvaluations} evaluations \n   - {self._bestSolution}'
        )
        macop_line(self)

    def information(self):
        logging.info(
            f"-- Best {self._bestSolution} - SCORE {self._bestSolution.fitness}"
        )

    def __str__(self):
        return f"{type(self).__name__} using {type(self._bestSolution).__name__}"
