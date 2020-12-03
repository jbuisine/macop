"""Multi-Ojective Evolutionary Algorithm with Scalar Decomposition algorithm
"""

# main imports
import pkgutil
import logging
import math
import numpy as np
import sys
from ...utils.color import macop_text, macop_line, macop_progress
from ...utils.modules import load_class

# module imports
from ..Algorithm import Algorithm
from .MOSubProblem import MOSubProblem


def moEvaluator(solution, evaluator, weights):

    scores = [eval(solution) for eval in evaluator]

    # associate objectives scores to solution
    solution._scores = scores

    return sum([scores[i] for i, w in enumerate(weights)])


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
        maximise: {bool} -- specify kind of optimisation problem 
        population: [{Solution}] -- population of solution, one for each sub problem
        pfPop: [{Solution}] -- pareto front population
        weights: [[{float}]] -- random weights used for custom mu sub problems
        callbacks: {[Callback]} -- list of Callback class implementation to do some instructions every number of evaluations and `load` when initializing algorithm
    """
    def __init__(self,
                 mu,
                 T,
                 initalizer,
                 evaluator,
                 operators,
                 policy,
                 validator,
                 maximise=True,
                 parent=None):

        # redefinition of constructor to well use `initRun` method
        self._initializer = initalizer
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

        # track reference of algo into operator (keep an eye into best solution)
        for operator in self._operators:
            operator.setAlgo(self)

        # by default track reference for policy
        self._policy.setAlgo(self)

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
            sub_evaluator = lambda solution: moEvaluator(
                solution, evaluator, weights[i])

            # intialize each sub problem
            # use copy of list to keep track for each sub problem
            subProblem = MOSubProblem(i, weights[i],
                                      initalizer, sub_evaluator,
                                      operators.copy(), policy, validator,
                                      maximise, self)

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
                    if spBestSolution.fitness(
                    ) > self._subProblems[j]._bestSolution.fitness():

                        # create new solution based on current new if better, computes fitness associated to new solution for sub problem
                        class_name = type(spBestSolution).__name__

                        # dynamically load solution class if unknown
                        if class_name not in sys.modules:
                            load_class(class_name, globals())

                        newSolution = getattr(
                            globals()['macop.solutions.' + class_name],
                            class_name)(spBestSolution._data,
                                        len(spBestSolution._data))

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

        macop_progress(self.getGlobalEvaluation(), self.getGlobalMaxEvaluation())

        logging.info(f"-- {type(self).__name__} evaluation {self._numberOfEvaluations} of {self._maxEvaluations} ({((self._numberOfEvaluations) / self._maxEvaluations * 100.):.2f}%)")

    def setNeighbors(self):

        dmin = dmax = 0

        if self._T % 2 == 1:
            dmin = -int(self._T / 2)
            dmax = int(self._T / 2) + 1
        else:
            dmin = -int(self._T / 2) + 1
            dmax = +self._T / 2

        # init neighbord list
        self._neighbors = [[] for n in range(self._mu)]

        for direction in range(0, -dmin):
            for i in range(self._T):
                self._neighbors[direction].append(i)

        for direction in range(-dmin, self._mu - dmax):
            for i in range(direction + dmin, direction + dmax):
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

        print(macop_text(f'({type(self).__name__}) Found after {self._numberOfEvaluations} evaluations'))

        for i, solution in enumerate(self._pfPop):
            print(f'  - [{i}] {solution._scores} : {solution}')

        print(macop_line())

    def information(self):

        logging.info("-- Pareto front :")

        for i, solution in enumerate(self._pfPop):
            logging.info(f"-- {i}] SCORE {solution._scores} - {solution}")

    def __str__(self):
        return f"{type(self).__name__} using {type(self._population).__name__}"
