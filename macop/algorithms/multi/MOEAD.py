"""Multi-Ojective Evolutionary Algorithm with Scalar Decomposition algorithm
"""

# main imports
import logging
import math
import numpy as np

# module imports
from ..Algorithm import Algorithm
from .MOSubProblem import MOSubProblem


class MOEAD(Algorithm):
    """Multi-Ojective Evolutionary Algorithm with Scalar Decomposition

    Attributes:
        mu: {int} -- number of sub problems
        T: {[float]} -- number of neightbors for each sub problem
        initalizer: {function} -- basic function strategy to initialize solution
        evaluator: {[function]} -- list of basic function in order to obtained fitness (multiple objectives)
        operators: {[Operator]} -- list of operator to use when launching algorithm
        policy: {Policy} -- Policy class implementation strategy to select operators
        validator: {function} -- basic function to check if solution is valid or not under some constraints
        maximise: {bool} -- specify kind of optimization problem 
        currentSolution: {Solution} -- current solution managed for current evaluation
        bestSolution: {Solution} -- best solution found so far during running algorithm
        checkpoint: {Checkpoint} -- Checkpoint class implementation to keep track of algorithm and restart
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
        self.checkpoint = None
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

        if _mu < _T:
            raise ValueError('`mu` cannot be less than `T`')
        self.mu = _mu
        self.T = _T

        # initialize neighbors for each sub problem
        self.setNeighbors()

        weights = []
        for i in range(self.mu):
            angle = math.pi / 2 * i / (self.mu - 1)
            weights.append([math.cos(angle), math.sin(angle)])

        self.subProblems = []

        for i in range(self.mu):

            # compute weight sum from solution
            sub_evaluator = lambda _solution: sum(
                list([
                    eval(_solution) * weights[i][w_i]
                    for w_i, eval in enumerate(_evaluator)
                ]))

            subProblem = MOSubProblem(i, weights[i], _initalizer,
                                      sub_evaluator, _operators, _policy,
                                      _validator, _maximise, self)
            self.subProblems.append(subProblem)

        self.population = [None for n in range(self.mu)]

        # no need to initialize using sub problem
        # self.initRun()

    def initRun(self):
        """
        Method which initialiazes or re-initializes the whole algorithm context specifically for MOEAD
        """

        self.currentSolution = self.initializer()

        # evaluate current solution
        self.subProblems[0].run(1)

        # keep in memory best known solution (current solution)
        self.bestSolution = self.subProblems[0].bestSolution

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

        # enable checkpoint for MOEAD
        if self.checkpoint is not None:
            self.resume()

        # initialize each sub problem
        for i in range(self.mu):
            self.subProblems[i].run(1)

            self.population[i] = self.subProblems[i].bestSolution

        # MOEAD algorithm implementation
        while not self.stop():

            for i in range(self.mu):

                # run 1 iteration into sub problem `i`
                self.subProblems[i].run(1)

                # stop algorithm if necessary
                if self.stop():
                    break

        logging.info("End of %s, best solution found %s" %
                     (type(self).__name__, self.bestSolution))

        self.end()

        return self.bestSolution

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
