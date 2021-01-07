"""Multi-objetive classes algorithm
"""

# main imports
import logging
import math
import numpy as np
import sys
from macop.utils.progress import macop_text, macop_line, macop_progress

# module imports
from macop.algorithms.base import Algorithm
from macop.evaluators.discrete.multi import WeightedSum


class MOEAD(Algorithm):
    """Multi-Ojective Evolutionary Algorithm with Scalar Decomposition

    Attributes:
        mu: {int} -- number of sub problems
        T: {[float]} -- number of neightbors for each sub problem
        nObjectives: {int} -- number of objectives (based of number evaluator)
        initializer: {function} -- basic function strategy to initialize solution
        evaluator: {[function]} -- list of basic function in order to obtained fitness (multiple objectives)
        operators: {[Operator]} -- list of operator to use when launching algorithm
        policy: {Policy} -- Policy class implementation strategy to select operators
        validator: {function} -- basic function to check if solution is valid or not under some constraints
        maximise: {bool} -- specify kind of optimisation problem
        verbose: {bool} -- verbose or not information about the algorithm
        population: [{Solution}] -- population of solution, one for each sub problem
        pfPop: [{Solution}] -- pareto front population
        weights: [[{float}]] -- random weights used for custom mu sub problems
        callbacks: {[Callback]} -- list of Callback class implementation to do some instructions every number of evaluations and `load` when initializing algorithm

    >>> import random
    >>> # operators import
    >>> from macop.operators.discrete.crossovers import SimpleCrossover
    >>> from macop.operators.discrete.mutators import SimpleMutation
    >>> # policy import
    >>> from macop.policies.classicals import RandomPolicy
    >>> # solution and algorithm
    >>> from macop.solutions.discrete import BinarySolution
    >>> from macop.algorithms.multi import MOEAD
    >>> # evaluator import
    >>> from macop.evaluators.discrete.mono import KnapsackEvaluator
    >>> # evaluator initialization (worths objects passed into data)
    >>> problem_size = 20
    >>> worths1 = [ random.randint(0, 20) for i in range(problem_size) ]
    >>> evaluator1 = KnapsackEvaluator(data={'worths': worths1})
    >>> worths2 = [ random.randint(10, 15) for i in range(problem_size) ]
    >>> evaluator2 = KnapsackEvaluator(data={'worths': worths2})
    >>> # validator specification (based on weights of each objects)
    >>> weights = [ random.randint(5, 30) for i in range(problem_size) ]
    >>> validator = lambda solution: True if sum([weights[i] for i, value in enumerate(solution._data) if value == 1]) < 200 else False
    >>> # initializer function with lambda function
    >>> initializer = lambda x=20: BinarySolution.random(x, validator)
    >>> # operators list with crossover and mutation
    >>> operators = [SimpleCrossover(), SimpleMutation()]
    >>> policy = RandomPolicy(operators)
    >>> # MOEAD use multi-objective, hence list of evaluators with mu=100 and T=10
    >>> algo = MOEAD(20, 5, initializer, [evaluator1, evaluator2], operators, policy, validator, maximise=True, verbose=False)
    >>> # run the algorithm and get the pareto front obtained
    >>> pf_solutions = algo.run(100)
    >>> # check size of expected pareto
    >>> len(pf_solutions)
    33
    """
    def __init__(self,
                 mu,
                 T,
                 initializer,
                 evaluator,
                 operators,
                 policy,
                 validator,
                 maximise=True,
                 parent=None,
                 verbose=True):

        # redefinition of constructor to well use `initRun` method
        self._initializer = initializer
        self._evaluator = evaluator
        self._operators = operators
        self._policy = policy
        self._validator = validator
        self._callbacks = []

        # by default
        self._numberOfEvaluations = 0
        self._maxEvaluations = 0
        self._nObjectives = len(evaluator)

        # other parameters
        self._parent = parent  # parent algorithm if it's sub algorithm

        #self.maxEvaluations = 0 # by default
        self._maximise = maximise

        self._verbose = verbose

        # track reference of algo into operator (keep an eye into best solution)
        for operator in self._operators:
            operator.setAlgo(self)

        # by default track reference for policy
        self._policy.setAlgo(self)

        if mu < T:
            raise ValueError('`mu` cannot be less than `T`')
            
        if mu < T:
            raise ValueError('`mu` cannot be less than `T`')

        self._mu = mu
        self._T = T

        # initialize neighbors for each sub problem
        self.setNeighbors()

        weights = []

        if self._nObjectives == 2:

            for i in range(self._mu):
                angle = math.pi / 2 * i / (self._mu - 1)
                weights.append([math.cos(angle), math.sin(angle)])

        elif self._nObjectives >= 3:

            # random weights using uniform
            for i in range(self._mu):
                w_i = np.random.uniform(0, 1, self._nObjectives)
                weights.append(w_i / sum(w_i))
        else:
            raise ValueError('Unvalid number of objectives')

        self._weights = weights

        self._subProblems = []

        for i in range(self._mu):

            # compute weight sum from solution
            sub_evaluator = WeightedSum(data={'evaluators': evaluator, 'weights': weights[i]})

            # intialize each sub problem
            # use copy of list to keep track for each sub problem
            subProblem = MOSubProblem(i, weights[i],
                                      initializer, sub_evaluator,
                                      operators.copy(), policy, validator,
                                      maximise, self, verbose=self._verbose)

            self._subProblems.append(subProblem)

        self._population = [None for n in range(self._mu)]
        self._pfPop = []

        # ref point based on number of evaluators
        if self._maximise:
            self._refPoint = [0 for _ in range(self._nObjectives)]
        else:
            self._refPoint = [
                sys.float_info.max for _ in range(self._nObjectives)
            ]

    def initRun(self):
        """
        Method which initialiazes or re-initializes the whole algorithm context specifically for MOEAD
        """
        # initialization is done during run method
        pass

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

        # enable callback resume for MOEAD
        self.resume()

        # initialize each sub problem if no backup
        for i in range(self._mu):

            if self._subProblems[i]._bestSolution is None:
                self._subProblems[i].run(1)
                self._population[i] = self._subProblems[i]._bestSolution

        # if no backup for pf population
        if len(self._pfPop) == 0:
            for i in range(self._mu):
                self._pfPop.append(self._subProblems[i]._bestSolution)

        # MOEAD algorithm implementation
        while not self.stop():

            for i in range(self._mu):

                # run 1 iteration into sub problem `i`
                self._subProblems[i].run(1)
                spBestSolution = self._subProblems[i]._bestSolution

                self.updateRefPoint(spBestSolution)

                # for each neighbor of current sub problem update solution if better
                improvment = False
                for j in self._neighbors[i]:
                    if spBestSolution.fitness() > self._subProblems[j]._bestSolution.fitness():

                        # create new solution based on current new if better, computes fitness associated to new solution for sub problem
                        newSolution = spBestSolution.clone()

                        # evaluate solution for new sub problem and update as best solution
                        self._subProblems[j].evaluate(newSolution)
                        self._subProblems[j]._bestSolution = newSolution

                        # update population solution for this sub problem
                        self._population[j] = newSolution

                        improvment = True

                # add new solution if improvment is idenfity
                if improvment:
                    self._pfPop.append(spBestSolution)

                # update pareto front
                self._pfPop = self.paretoFront(self._pfPop)

                # add progress here
                self.progress()

                # stop algorithm if necessary
                if self.stop():
                    break

        logging.info(f"End of {type(self).__name__}, best solution found {self._population}")

        self.end()

        return self._pfPop

    def progress(self):
        """
        Log progress and apply callbacks if necessary
        """
        if len(self._callbacks) > 0:
            for callback in self._callbacks:
                callback.run()

        macop_progress(self, self.getGlobalEvaluation(), self.getGlobalMaxEvaluation())

        logging.info(f"-- {type(self).__name__} evaluation {self._numberOfEvaluations} of {self._maxEvaluations} ({((self._numberOfEvaluations) / self._maxEvaluations * 100.):.2f}%)")

    def setNeighbors(self):

        if self._T % 2 == 1:
            dmin = -int(self._T / 2)
            dmax = int(self._T / 2) + 1
        else:
            dmin = -int(self._T / 2) + 1
            dmax = int(+self._T / 2)

        # init neighbord list
        self._neighbors = [[] for n in range(self._mu)]

        for direction in range(0, -dmin):
            for i in range(self._T):
                self._neighbors[direction].append(i)

        for direction in range(-dmin, self._mu - dmax):
            for i in range(direction + dmin, direction + dmax - 1):
                self._neighbors[direction].append(i)

        for direction in range(self._mu - dmax, self._mu):
            for i in range(self._mu - self._T, self._mu):
                self._neighbors[direction].append(i)

    def updateRefPoint(self, solution):

        if self._maximise:
            for i in range(len(self._evaluator)):
                if solution._scores[i] > self._refPoint[i]:
                    self._refPoint[i] = solution._scores[i]
        else:
            for i in range(len(self._evaluator)):
                if solution.scores[i] < self._refPoint[i]:
                    self._refPoint[i] = solution._scores[i]

    def paretoFront(self, population):

        paFront = []
        indexes = []
        nObjectives = len(self._evaluator)
        nSolutions = len(population)

        # find dominated solution
        for i in range(nSolutions):
            for j in range(nSolutions):

                if j in indexes:
                    continue

                # check if solutions are the same
                if all([
                        population[i]._data[k] == population[j]._data[k]
                        for k in range(len(population[i]._data))
                ]):
                    continue

                nDominated = 0

                # check number of dominated objectives of current solution by the others solution
                for k in range(len(self._evaluator)):
                    if self._maximise:
                        if population[i]._scores[k] < population[j]._scores[k]:
                            nDominated += 1
                    else:
                        if population[i]._scores[k] > population[j]._scores[k]:
                            nDominated += 1

                if nDominated == nObjectives:
                    indexes.append(i)
                    break

        # store the non dominated solution into pareto front
        for i in range(nSolutions):
            if i not in indexes:
                paFront.append(population[i])

        return paFront

    def end(self):
        """Display end message into `run` method
        """ 

        macop_text(self, f'({type(self).__name__}) Found after {self._numberOfEvaluations} evaluations')

        for i, solution in enumerate(self._pfPop):
            macop_text(self, f'  - [{i}] {solution._scores} : {solution}')

        macop_line(self)

    def information(self):

        logging.info("-- Pareto front :")

        for i, solution in enumerate(self._pfPop):
            logging.info(f"-- {i}] SCORE {solution._scores} - {solution}")

    def __str__(self):
        return f"{type(self).__name__} using {type(self._population).__name__}"


class MOSubProblem(Algorithm):
    """Specific MO sub problem used into MOEAD

    Attributes:
        index: {int} -- sub problem index
        weights: {[float]} -- sub problems objectives weights
        initalizer: {function} -- basic function strategy to initialize solution
        evaluator: {function} -- basic function in order to obtained fitness (mono or multiple objectives)
        operators: {[Operator]} -- list of operator to use when launching algorithm
        policy: {Policy} -- Policy class implementation strategy to select operators
        validator: {function} -- basic function to check if solution is valid or not under some constraints
        maximise: {bool} -- specify kind of optimisation problem 
        verbose: {bool} -- verbose or not information about the algorithm
        currentSolution: {Solution} -- current solution managed for current evaluation
        bestSolution: {Solution} -- best solution found so far during running algorithm
        callbacks: {[Callback]} -- list of Callback class implementation to do some instructions every number of evaluations and `load` when initializing algorithm
    
    Example:

    >>> import random
    >>> # operators import
    >>> from macop.operators.discrete.crossovers import SimpleCrossover
    >>> from macop.operators.discrete.mutators import SimpleMutation
    >>> # policy import
    >>> from macop.policies.classicals import RandomPolicy
    >>> # solution and algorithm
    >>> from macop.solutions.discrete import BinarySolution
    >>> from macop.algorithms.multi import MOEAD, MOSubProblem
    >>> # evaluator import
    >>> from macop.evaluators.discrete.mono import KnapsackEvaluator
    >>> # evaluator initialization (worths objects passed into data)
    >>> problem_size = 20
    >>> worths1 = [ random.randint(0, 20) for i in range(problem_size) ]
    >>> evaluator1 = KnapsackEvaluator(data={'worths': worths1})
    >>> worths2 = [ random.randint(10, 15) for i in range(problem_size) ]
    >>> evaluator2 = KnapsackEvaluator(data={'worths': worths2})
    >>> # validator specification (based on weights of each objects)
    >>> weights = [ random.randint(5, 30) for i in range(problem_size) ]
    >>> validator = lambda solution: True if sum([weights[i] for i, value in enumerate(solution._data) if value == 1]) < 200 else False
    >>> # initializer function with lambda function
    >>> initializer = lambda x=20: BinarySolution.random(x, validator)
    >>> # operators list with crossover and mutation
    >>> operators = [SimpleCrossover(), SimpleMutation()]
    >>> policy = RandomPolicy(operators)
    >>> algo = MOEAD(20, 5, initializer, [evaluator1, evaluator2], operators, policy, validator, maximise=True, verbose=False)
    >>> # weights of the sub problem
    >>> sub_problem_weights = [0.4, 0.6]
    >>> sub_evaluator = WeightedSum(data={'evaluators': [evaluator1, evaluator2], 'weights': sub_problem_weights})
    >>> # first parameter is the index of the MOSubProblem
    >>> subProblem = MOSubProblem(0, sub_problem_weights, initializer, sub_evaluator, operators, policy, validator, maximise=True, parent=algo, verbose=False)
    >>> # run the algorithm
    >>> solution = subProblem.run(100)
    >>> solution._score
    133.0
    """
    def __init__(self,
                 index,
                 weights,
                 initalizer,
                 evaluator,
                 operators,
                 policy,
                 validator,
                 maximise=True,
                 parent=None,
                 verbose=True):

        super().__init__(initalizer, evaluator, operators, policy,
                         validator, maximise, parent)

        self._index = index
        self._weights = weights

        self._verbose = verbose

    def run(self, evaluations):
        """
        Run the local search algorithm

        Args:
            evaluations: {int} -- number of evaluations
            
        Returns:
            {Solution} -- best solution found
        """

        # by default use of mother method to initialize variables
        super().run(evaluations)

        # initialize solution if necessary
        if self._bestSolution is None:
            self.initRun()

        # new operators list keep track of current sub problem
        for op in self._operators:
            op.setAlgo(self)

        for _ in range(evaluations):

            # keep reference of sub problem used
            self._policy.setAlgo(self)

            # update solution using policy
            newSolution = self.update(self._bestSolution)

            # if better solution than currently, replace it
            if self.isBetter(newSolution):
                self._bestSolution = newSolution

            # increase number of evaluations
            self.increaseEvaluation()

            self.progress()

            # stop algorithm if necessary
            if self.stop():
                break

            logging.info(f"---- Current {newSolution} - SCORE {newSolution.fitness()}")

            logging.info(f"End of {type(self).__name__}, best solution found {self._bestSolution}")

        return self._bestSolution
