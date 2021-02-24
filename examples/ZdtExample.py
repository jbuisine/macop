# main imports
import logging
import os
import random
import numpy as np
import math

# module imports
from macop.solutions.continuous import ContinuousSolution
from macop.evaluators.continuous.mono import ZdtEvaluator

from macop.operators.continuous.mutators import PolynomialMutation
from macop.operators.continuous.crossovers import BasicDifferentialEvolutionCrossover

from macop.policies.classicals import RandomPolicy

from macop.algorithms.mono import IteratedLocalSearch as ILS
from macop.algorithms.mono import HillClimberFirstImprovment
from macop.callbacks.classicals import ContinuousCheckpoint

if not os.path.exists('data'):
    os.makedirs('data')

# logging configuration
logging.basicConfig(format='%(asctime)s %(message)s', filename='data/example.log', level=logging.DEBUG)

random.seed(42)

# usefull instance data
n = 10
filepath = "data/checkpoints_zdt_Rosenbrock.csv"
problem_interval = -10, 10 # fixed value interval (avoid infinite)


# check each value in order to validate
def validator(solution):

    mini, maxi = problem_interval

    for x in solution.data:
        if x < mini or x > maxi:
            return False

    return True

# define init random solution
def init():
    return ContinuousSolution.random(n, problem_interval, validator)

def main():

    # Rosenbrock function with a=1 and b=100 (see https://en.wikipedia.org/wiki/Rosenbrock_function)
    Rosenbrock_function = lambda s: sum([ 100 * math.pow(s.data[i + 1] - (math.pow(s.data[i], 2)), 2) + math.pow((1 - s.data[i]), 2) for i in range(len(s.data) - 1) ])

    operators = [PolynomialMutation(interval=problem_interval), BasicDifferentialEvolutionCrossover(interval=problem_interval)]
    policy = RandomPolicy(operators)
    callback = ContinuousCheckpoint(every=5, filepath=filepath)
    evaluator = ZdtEvaluator(data={'f': Rosenbrock_function})

    # passing global evaluation param from ILS
    hcfi = HillClimberFirstImprovment(init, evaluator, operators, policy, validator, maximise=False, verbose=True)
    algo = ILS(init, evaluator, operators, policy, validator, localSearch=hcfi, maximise=False, verbose=True)
    
    # add callback into callback list
    algo.addCallback(callback)

    bestSol = algo.run(100000, ls_evaluations=100)
    print(bestSol.data)

    print('Solution for Rosenbrock Zdt instance score is {}'.format(evaluator.compute(bestSol)))

if __name__ == "__main__":
    main()