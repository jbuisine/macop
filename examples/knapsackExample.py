# main imports
import logging
import os
import random

# module imports
from macop.solutions.discrete import BinarySolution
from macop.evaluators.knapsacks import KnapsackEvaluator

from macop.operators.discrete.mutators import SimpleMutation
from macop.operators.discrete.mutators import SimpleBinaryMutation
from macop.operators.discrete.crossovers import SimpleCrossover
from macop.operators.discrete.crossovers import RandomSplitCrossover

from macop.policies.classicals import RandomPolicy
from macop.policies.reinforcement import UCBPolicy

from macop.algorithms.mono import IteratedLocalSearch as ILS
from macop.callbacks.classicals import BasicCheckpoint

if not os.path.exists('data'):
    os.makedirs('data')

# logging configuration
logging.basicConfig(format='%(asctime)s %(message)s', filename='data/example.log', level=logging.DEBUG)

random.seed(42)

elements_score = [ random.randint(1, 20) for _ in range(30) ]
elements_weight = [ random.randint(2, 5) for _ in range(30) ]

def knapsackWeight(solution):

    weight_sum = 0
    for index, elem in enumerate(solution._data):
        weight_sum += elements_weight[index] * elem

    return weight_sum

# default validator
def validator(solution):

    if knapsackWeight(solution) <= 80:
        return True
    else:
        False

# define init random solution
def init():
    return BinarySolution.random(validator, 30)


filepath = "data/checkpoints.csv"

def main():

    operators = [SimpleBinaryMutation(), SimpleMutation(), SimpleCrossover(), RandomSplitCrossover()]
    policy = UCBPolicy(operators)
    callback = BasicCheckpoint(every=5, filepath=filepath)
    evaluator = KnapsackEvaluator(data={'worths': elements_score})

    algo = ILS(init, evaluator, operators, policy, validator, maximise=True, verbose=False)
    
    # add callback into callback list
    algo.addCallback(callback)

    bestSol = algo.run(1000)

    print('Solution score is {}'.format(evaluator.compute(bestSol)))
    print('Solution weigth is {}'.format(knapsackWeight(bestSol)))

if __name__ == "__main__":
    main()