"""Multi-Ojective Evolutionary Algorithm with Scalar Decomposition algorithm
"""

# main imports
import pkgutil
import logging
import math
import numpy as np
import sys
from ...utils.color import macop_text, macop_line, macop_progress

# module imports
from ..Algorithm import Algorithm
from .MOSubProblem import MOSubProblem

# import all available solutions
for loader, module_name, is_pkg in pkgutil.walk_packages(
        path=['macop/solutions'], prefix='macop.solutions.'):
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module


def moEvaluator(_solution, _evaluator, _weights):

    scores = [eval(_solution) for eval in _evaluator]

    # associate objectives scores to solution
    _solution.scores = scores

    return sum([scores[i] for i, w in enumerate(_weights)])


class MOEAD(Algorithm):
    """Multi-Ojective Evolutionary Algorithm with Scalar Decomposition

    Attributes:
        mu: {int} -- number of sub problems
        T: {[float]} -- number of neightbors for each sub problem
        nObjectives: {int} -- number of objectives (based of number evaluator)
        initalizer: {function} -- basic function strategy to initialize solution
        evaluator: {[function]} -- list of basic function in order to obtained fitness (multiple objectives)
        operators: {[Operator]} -- list of operator to use when launching algorithm
        policy: {Policy} -- Policy class implementation strategy to select operators
        validator: {function} -- basic function to check if solution is valid or not under some constraints
        maximise: {bool} -- specify kind of optimization problem 
        population: [{Solution}] -- population of solution, one for each sub problem
        pfPop: [{Solution}] -- pareto front population
        weights: [[{float}]] -- random weights used for custom mu sub problems
        callbacks: {[Callback]} -- list of Callback class implementation to do some instructions every number of evaluations and `load` when initializing algorithm
    """
    def __init__(self,
                 _mu,
                 _T,
                 _initalizer,
                 _evaluator,
                 _operators,
                 _policy,
                 _validator,
                 _maximise=True,
                 _parent=None):

        # redefinition of constructor to well use `initRun` method
        self.initializer = _initalizer
        self.evaluator = _evaluator
        self.operators = _operators
        self.policy = _policy
        self.validator = _validator
        self.callbacks = []

        # by default
        self.numberOfEvaluations = 0
        self.maxEvaluations = 0
        self.nObjectives = len(_evaluator)

        # other parameters
        self.parent = _parent  # parent algorithm if it's sub algorithm

        #self.maxEvaluations = 0 # by default
        self.maximise = _maximise

        # track reference of algo into operator (keep an eye into best solution)
        for operator in self.operators:
            operator.setAlgo(self)

        # also track reference for policy
        self.policy.setAlgo(self)

        if _mu < _T:
            raise ValueError('`mu` cannot be less than `T`')

        self.mu = _mu
        self.T = _T

        # initialize neighbors for each sub problem
        self.setNeighbors()

        weights = []

        if self.nObjectives == 2:

            for i in range(self.mu):
                angle = math.pi / 2 * i / (self.mu - 1)
                weights.append([math.cos(angle), math.sin(angle)])

        elif self.nObjectives >= 3:

            # random weights using uniform
            for i in range(self.mu):
                w_i = np.random.uniform(0, 1, self.nObjectives)
                weights.append(w_i / sum(w_i))
        else:
            raise ValueError('Unvalid number of objectives')

        self.weights = weights

        self.subProblems = []

        for i in range(self.mu):

            # compute weight sum from solution
            sub_evaluator = lambda _solution: moEvaluator(
                _solution, _evaluator, weights[i])

            # intialize each sub problem
            subProblem = MOSubProblem(i, weights[i], _initalizer,
                                      sub_evaluator, _operators, _policy,
                                      _validator, _maximise, self)

            self.subProblems.append(subProblem)

        self.population = [None for n in range(self.mu)]
        self.pfPop = []

        # ref point based on number of evaluators
        if self.maximise:
            self.refPoint = [0 for _ in range(self.nObjectives)]
        else:
            self.refPoint = [
                sys.float_info.max for _ in range(self.nObjectives)
            ]

    def initRun(self):
        """
        Method which initialiazes or re-initializes the whole algorithm context specifically for MOEAD
        """
        # initialization is done during run method
        pass

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

        # initialize each sub problem
        for i in range(self.mu):
            self.subProblems[i].run(1)

            self.population[i] = self.subProblems[i].bestSolution
            self.pfPop.append(self.subProblems[i].bestSolution)

        # enable callback resume for MOEAD
        self.resume()

        # MOEAD algorithm implementation
        while not self.stop():

            for i in range(self.mu):

                # run 1 iteration into sub problem `i`
                self.subProblems[i].run(1)
                spBestSolution = self.subProblems[i].bestSolution

                self.updateRefPoint(spBestSolution)

                # for each neighbor of current sub problem update solution if better
                improvment = False
                for j in self.neighbors[i]:
                    if spBestSolution.fitness(
                    ) > self.subProblems[j].bestSolution.fitness():

                        # create new solution based on current new if better, computes fitness associated to new solution for sub problem
                        class_name = type(spBestSolution).__name__
                        newSolution = getattr(
                            globals()['macop.solutions.' + class_name],
                            class_name)(spBestSolution.data,
                                        len(spBestSolution.data))

                        # evaluate solution for new sub problem and update as best solution
                        self.subProblems[j].evaluate(newSolution)
                        self.subProblems[j].bestSolution = newSolution

                        # update population solution for this sub problem
                        self.population[j] = newSolution

                        improvment = True

                # add new solution if improvment is idenfity
                if improvment:
                    self.pfPop.append(spBestSolution)

                # update pareto front
                self.pfPop = self.paretoFront(self.pfPop)

                # add progress here
                self.progress()

                # stop algorithm if necessary
                if self.stop():
                    break

        logging.info("End of %s, best solution found %s" %
                     (type(self).__name__, self.population))

        self.end()

        return self.pfPop

    def progress(self):
        """
        Log progress and apply callbacks if necessary
        """
        if len(self.callbacks) > 0:
            for callback in self.callbacks:
                callback.run()

        macop_progress(self.getGlobalEvaluation(),
                       self.getGlobalMaxEvaluation())

        logging.info(
            "-- %s evaluation %s of %s (%s%%)" %
            (type(self).__name__, self.numberOfEvaluations,
             self.maxEvaluations, "{0:.2f}".format(
                 (self.numberOfEvaluations) / self.maxEvaluations * 100.)))

    def setNeighbors(self):

        dmin = dmax = 0

        if self.T % 2 == 1:
            dmin = -int(self.T / 2)
            dmax = int(self.T / 2) + 1
        else:
            dmin = -int(self.T / 2) + 1
            dmax = +self.T / 2

        # init neighbord list
        self.neighbors = [[] for n in range(self.mu)]

        for direction in range(0, -dmin):
            for i in range(self.T):
                self.neighbors[direction].append(i)

        for direction in range(-dmin, self.mu - dmax):
            for i in range(direction + dmin, direction + dmax):
                self.neighbors[direction].append(i)

        for direction in range(self.mu - dmax, self.mu):
            for i in range(self.mu - self.T, self.mu):
                self.neighbors[direction].append(i)

    def updateRefPoint(self, _solution):

        if self.maximise:
            for i in range(len(self.evaluator)):
                if _solution.scores[i] > self.refPoint[i]:
                    self.refPoint[i] = _solution.scores[i]
        else:
            for i in range(len(self.evaluator)):
                if _solution.scores[i] < self.refPoint[i]:
                    self.refPoint[i] = _solution.scores[i]

    def paretoFront(self, _population):

        paFront = []
        indexes = []
        nObjectives = len(self.evaluator)
        nSolutions = len(_population)

        # find dominated solution
        for i in range(nSolutions):
            for j in range(nSolutions):

                if j in indexes:
                    continue

                nDominated = 0

                # check number of dominated objectives of current solution by the others solution
                for k in range(len(self.evaluator)):
                    if self.maximise:
                        if _population[i].scores[k] < _population[j].scores[k]:
                            nDominated += 1
                    else:
                        if _population[i].scores[k] > _population[j].scores[k]:
                            nDominated += 1

                if nDominated == nObjectives:
                    indexes.append(i)
                    break

        # store the non dominated solution into pareto front
        for i in range(nSolutions):
            if i not in indexes:
                paFront.append(_population[i])

        return paFront

    def end(self):
        """Display end message into `run` method
        """

        print(
            macop_text('({}) Found after {} evaluations'.format(
                type(self).__name__, self.numberOfEvaluations)))

        for i, solution in enumerate(self.pfPop):
            print('  - [{}] {} : {}'.format(i, solution.scores, solution))

        print(macop_line())

    def information(self):

        logging.info("-- Pareto front :")

        for i, solution in enumerate(self.pfPop):
            logging.info("-- %s] SCORE %s - %s" %
                         (i, solution.scores, solution))

    def __str__(self):
        return "%s using %s" % (type(self).__name__, type(
            self.population).__name__)
