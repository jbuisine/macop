"""Mono-objective available algorithms
"""

# main imports
import logging

# module imports
from macop.algorithms.base import Algorithm


class HillClimberFirstImprovment(Algorithm):
    """Hill Climber First Improvment used as quick exploration optimisation algorithm

    - First, this algorithm do a neighborhood exploration of a new generated solution (by doing operation on the current solution obtained) in order to find a better solution from the neighborhood space;
    - Then replace the current solution by the first one from the neighbordhood space which is better than the current solution;
    - And do these steps until a number of evaluation (stopping criterion) is reached.

    Attributes:
        initalizer: {function} -- basic function strategy to initialise solution
        evaluator: {:class:`~macop.evaluators.base.Evaluator`} -- evaluator instance in order to obtained fitness (mono or multiple objectives)
        operators: {[:class:`~macop.operators.base.Operator`]} -- list of operator to use when launching algorithm
        policy: {:class:`~macop.policies.base.Policy`} -- Policy class implementation strategy to select operators
        validator: {function} -- basic function to check if solution is valid or not under some constraints
        maximise: {bool} -- specify kind of optimisation problem 
        currentSolution: {:class:`~macop.solutions.base.Solution`} -- current solution managed for current evaluation
        bestSolution: {:class:`~macop.solutions.base.Solution`} -- best solution found so far during running algorithm
        callbacks: {[:class:`~macop.callbacks.base.Callback`]} -- list of Callback class implementation to do some instructions every number of evaluations and `load` when initialising algorithm
        parent: {:class:`~macop.algorithms.base.Algorithm`} -- parent algorithm reference in case of inner Algorithm instance (optional)
    
    Example:

    >>> import random
    >>>
    >>> # operators import
    >>> from macop.operators.discrete.crossovers import SimpleCrossover
    >>> from macop.operators.discrete.mutators import SimpleMutation
    >>>
    >>> # policy import
    >>> from macop.policies.classicals import RandomPolicy
    >>>
    >>> # solution and algorithm imports
    >>> from macop.solutions.discrete import BinarySolution
    >>> from macop.algorithms.mono import HillClimberFirstImprovment
    >>>
    >>> # evaluator import
    >>> from macop.evaluators.discrete.mono import KnapsackEvaluator
    >>>
    >>> # evaluator initialization (worths objects passed into data)
    >>> problem_size = 20
    >>> worths = [ random.randint(0, 20) for i in range(problem_size) ]
    >>> evaluator = KnapsackEvaluator(data={'worths': worths})
    >>>
    >>> # validator specification (based on weights of each objects)
    >>> weights = [ random.randint(5, 30) for i in range(problem_size) ]
    >>> validator = lambda solution: True if sum([weights[i] for i, value in enumerate(solution.data) if value == 1]) < 200 else False
    >>>
    >>> # initialiser function for binary solution using specific solution size
    >>> initialiser = lambda x=20: BinarySolution.random(x, validator)
    >>>
    >>> # operators list with crossover and mutation
    >>> operators = [SimpleCrossover(), SimpleMutation()]
    >>> policy = RandomPolicy(operators)
    >>> algo = HillClimberFirstImprovment(initialiser, evaluator, operators, policy, validator, maximise=True, verbose=False)
    >>>
    >>> # run the algorithm
    >>> solution = algo.run(100)
    >>> solution._score
    128
    """
    def run(self, evaluations):
        """
        Run the local search algorithm

        Args:
            evaluations: {int} -- number of Local search evaluations
            
        Returns:
            {:class:`~macop.solutions.base.Solution`}: best solution found
        """

        # by default use of mother method to initialise variables
        super().run(evaluations)

        # initialise current solution and best solution
        self.initRun()

        solutionSize = self._currentSolution.size

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
                logging.info(
                    f"---- Current {newSolution} - SCORE {newSolution.fitness}"
                )

                # stop algorithm if necessary
                if self.stop():
                    break

            # set new current solution using best solution found in this neighbor search
            self._currentSolution = self._bestSolution

        logging.info(
            f"End of {type(self).__name__}, best solution found {self._bestSolution}"
        )

        return self._bestSolution


class HillClimberBestImprovment(Algorithm):
    """Hill Climber Best Improvment used as exploitation optimisation algorithm

    - First, this algorithm do a neighborhood exploration of a new generated solution (by doing operation on the current solution obtained) in order to find the best solution from the neighborhood space;
    - Then replace the best solution found from the neighbordhood space as current solution to use;
    - And do these steps until a number of evaluation (stopping criterion) is reached.

    Attributes:
        initalizer: {function} -- basic function strategy to initialise solution
        evaluator: {:class:`~macop.evaluators.base.Evaluator`} -- evaluator instance in order to obtained fitness (mono or multiple objectives)
        operators: {[:class:`~macop.operators.base.Operator`]} -- list of operator to use when launching algorithm
        policy: {:class:`~macop.policies.base.Policy`} -- Policy class implementation strategy to select operators
        validator: {function} -- basic function to check if solution is valid or not under some constraints
        maximise: {bool} -- specify kind of optimisation problem 
        currentSolution: {:class:`~macop.solutions.base.Solution`} -- current solution managed for current evaluation
        bestSolution: {:class:`~macop.solutions.base.Solution`} -- best solution found so far during running algorithm
        callbacks: {[:class:`~macop.callbacks.base.Callback`]} -- list of Callback class implementation to do some instructions every number of evaluations and `load` when initialising algorithm
        parent: {:class:`~macop.algorithms.base.Algorithm`} -- parent algorithm reference in case of inner Algorithm instance (optional)
    
    Example:

    >>> import random
    >>>
    >>> # operators import
    >>> from macop.operators.discrete.crossovers import SimpleCrossover
    >>> from macop.operators.discrete.mutators import SimpleMutation
    >>>
    >>> # policy import
    >>> from macop.policies.classicals import RandomPolicy
    >>>
    >>> # solution and algorithm imports
    >>> from macop.solutions.discrete import BinarySolution
    >>> from macop.algorithms.mono import HillClimberBestImprovment
    >>>
    >>> # evaluator import
    >>> from macop.evaluators.discrete.mono import KnapsackEvaluator
    >>>
    >>> # evaluator initialization (worths objects passed into data)
    >>> problem_size = 20
    >>> worths = [ random.randint(0, 20) for i in range(problem_size) ]
    >>> evaluator = KnapsackEvaluator(data={'worths': worths})
    >>>
    >>> # validator specification (based on weights of each objects)
    >>> weights = [ random.randint(5, 30) for i in range(problem_size) ]
    >>> validator = lambda solution: True if sum([weights[i] for i, value in enumerate(solution.data) if value == 1]) < 200 else False
    >>>
    >>> # initialiser function for binary solution using specific solution size
    >>> initialiser = lambda x=20: BinarySolution.random(x, validator)
    >>>
    >>> # operators list with crossover and mutation
    >>> operators = [SimpleCrossover(), SimpleMutation()]
    >>> policy = RandomPolicy(operators)
    >>> algo = HillClimberBestImprovment(initialiser, evaluator, operators, policy, validator, maximise=True, verbose=False)
    >>>
    >>> # run the algorithm
    >>> solution = algo.run(100)
    >>> solution._score
    104
    """
    def run(self, evaluations):
        """
        Run the local search algorithm

        Args:
            evaluations: {int} -- number of Local search evaluations
            
        Returns:
            {:class:`~macop.solutions.base.Solution`}: best solution found
        """

        # by default use of mother method to initialise variables
        super().run(evaluations)

        # initialise current solution and best solution
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
                logging.info(
                    f"---- Current {newSolution} - SCORE {newSolution.fitness}"
                )

                # stop algorithm if necessary
                if self.stop():
                    break

            # set new current solution using best solution found in this neighbor search
            self._currentSolution = self._bestSolution

        logging.info(
            f"End of {type(self).__name__}, best solution found {self._bestSolution}"
        )

        return self._bestSolution


class IteratedLocalSearch(Algorithm):
    """Iterated Local Search (ILS) used to avoid local optima and increave EvE (Exploration vs Exploitation) compromise

    - A number of evaluations (`ls_evaluations`) is dedicated to local search process, here `HillClimberFirstImprovment` algorithm;
    - Starting with the new generated solution, the local search algorithm will return a new solution;
    - If the obtained solution is better than the best solution known into `IteratedLocalSearch`, then the solution is replaced;
    - Restart this process until stopping critirion (number of expected evaluations).

    Attributes:
        initalizer: {function} -- basic function strategy to initialise solution
        evaluator: {function} -- basic function in order to obtained fitness (mono or multiple objectives)
        operators: {[:class:`~macop.operators.base.Operator`]} -- list of operator to use when launching algorithm
        policy: {:class:`~macop.policies.base.Policy`} -- Policy class implementation strategy to select operators
        validator: {function} -- basic function to check if solution is valid or not under some constraints
        maximise: {bool} -- specify kind of optimisation problem 
        currentSolution: {:class:`~macop.solutions.base.Solution`} -- current solution managed for current evaluation
        bestSolution: {:class:`~macop.solutions.base.Solution`} -- best solution found so far during running algorithm
        localSearch: {:class:`~macop.algorithms.base.Algorithm`} -- current local search into ILS
        callbacks: {[:class:`~macop.callbacks.base.Callback`]} -- list of Callback class implementation to do some instructions every number of evaluations and `load` when initialising algorithm
        parent: {:class:`~macop.algorithms.base.Algorithm`} -- parent algorithm reference in case of inner Algorithm instance (optional)
    
    Example:

    >>> import random
    >>>
    >>> # operators import
    >>> from macop.operators.discrete.crossovers import SimpleCrossover
    >>> from macop.operators.discrete.mutators import SimpleMutation
    >>>
    >>> # policy import
    >>> from macop.policies.classicals import RandomPolicy
    >>>
    >>> # import for solution and algorithm
    >>> from macop.solutions.discrete import BinarySolution
    >>> from macop.algorithms.mono import IteratedLocalSearch
    >>> from macop.algorithms.mono import HillClimberFirstImprovment
    >>>
    >>> # evaluator import
    >>> from macop.evaluators.discrete.mono import KnapsackEvaluator
    >>>
    >>> # evaluator initialization (worths objects passed into data)
    >>> problem_size = 20
    >>> worths = [ random.randint(0, 20) for i in range(problem_size) ]
    >>> evaluator = KnapsackEvaluator(data={'worths': worths})
    >>>
    >>> # validator specification (based on weights of each objects)
    >>> weights = [ random.randint(5, 30) for i in range(problem_size) ]
    >>> validator = lambda solution: True if sum([weights[i] for i, value in enumerate(solution.data) if value == 1]) < 200 else False
    >>>
    >>> # initialiser function with lambda function
    >>> initialiser = lambda x=20: BinarySolution.random(x, validator)
    >>>
    >>> # operators list with crossover and mutation
    >>> operators = [SimpleCrossover(), SimpleMutation()]
    >>> policy = RandomPolicy(operators)
    >>> local_search = HillClimberFirstImprovment(initialiser, evaluator, operators, policy, validator, maximise=True, verbose=False)
    >>> algo = IteratedLocalSearch(initialiser, evaluator, operators, policy, validator, localSearch=local_search, maximise=True, verbose=False)
    >>>
    >>> # run the algorithm using specific number of evaluations for local search
    >>> solution = algo.run(100, ls_evaluations=10)
    >>> solution._score
    137
    """
    def __init__(self,
                 initialiser,
                 evaluator,
                 operators,
                 policy,
                 validator,
                 localSearch,
                 maximise=True,
                 parent=None,
                 verbose=True):
        """Iterated Local Search Algorithm initialisation with use of specific LocalSearch {:class:`~macop.algorithms.base.Algorithm`} instance

        Args:
            initialiser: {function} -- basic function strategy to initialise solution
            evaluator: {:class:`~macop.evaluators.base.Evaluator`} -- evaluator instance in order to obtained fitness (mono or multiple objectives)
            operators: {[:class:`~macop.operators.base.Operator`]} -- list of operator to use when launching algorithm
            policy: {:class:`~macop.policies.base.Policy`} -- Policy implementation strategy to select operators
            validator: {function} -- basic function to check if solution is valid or not under some constraints
            localSearch: {:class:`~macop.algorithms.base.Algorithm`} -- current local search into ILS
            maximise: {bool} -- specify kind of optimisation problem 
            parent: {:class:`~macop.algorithms.base.Algorithm`} -- parent algorithm reference in case of inner Algorithm instance (optional)
            verbose: {bool} -- verbose or not information about the algorithm
        """

        super().__init__(initialiser, evaluator, operators, policy, validator,
                         maximise, parent, verbose)

        # specific local search associated with current algorithm
        self._localSearch = localSearch
        # need to attach current algorithm as parent
        self._localSearch.setParent(self)

    def run(self, evaluations, ls_evaluations=100):
        """
        Run the iterated local search algorithm using local search (EvE compromise)

        Args:
            evaluations: {int} -- number of global evaluations for ILS
            ls_evaluations: {int} -- number of Local search evaluations (default: 100)

        Returns:
            {:class:`~macop.solutions.base.Solution`}: best solution found
        """

        # by default use of mother method to initialise variables
        super().run(evaluations)

        # add same callbacks
        for callback in self._callbacks:
            self._localSearch.addCallback(callback)

        # enable resuming for ILS
        self.resume()

        # initialise current solution
        self.initRun()

        # local search algorithm implementation
        while not self.stop():

            # create and search solution from local search
            newSolution = self._localSearch.run(ls_evaluations)

            # if better solution than currently, replace it
            if self.isBetter(newSolution):
                self._bestSolution = newSolution

            # number of evaluatins increased from LocalSearch
            # increase number of evaluations and progress are then not necessary there
            #self.increaseEvaluation()
            #self.progress()

            self.information()

        logging.info(
            f"End of {type(self).__name__}, best solution found {self._bestSolution}"
        )

        self.end()

        return self._bestSolution
