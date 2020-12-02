# main imports
import logging
import os
import random

# module imports
from macop.solutions.BinarySolution import BinarySolution
from macop.evaluators.EvaluatorExample import evaluatorExample

from macop.operators.mutators.SimpleMutation import SimpleMutation
from macop.operators.mutators.SimpleBinaryMutation import SimpleBinaryMutation
from macop.operators.crossovers.SimpleCrossover import SimpleCrossover
from macop.operators.crossovers.RandomSplitCrossover import RandomSplitCrossover

from macop.operators.policies.RandomPolicy import RandomPolicy
from macop.operators.policies.UCBPolicy import UCBPolicy

from macop.algorithms.mono.IteratedLocalSearch import IteratedLocalSearch as ILS
from macop.callbacks.BasicCheckpoint import BasicCheckpoint

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
    return BinarySolution([], 30).random(validator)

def evaluator(solution):

    fitness = 0
    for index, elem in enumerate(solution._data):
        fitness += (elements_score[index] * elem)

    return fitness

filepath = "data/checkpoints.csv"

def main():

    operators = [SimpleBinaryMutation(), SimpleMutation(), SimpleCrossover(), RandomSplitCrossover()]
    policy = UCBPolicy(operators)
    callback = BasicCheckpoint(every=5, filepath=filepath)

    algo = ILS(init, evaluator, operators, policy, validator, maximise=True)
    
    # add callback into callback list
    algo.addCallback(callback)

    bestSol = algo.run(1000)

    print('Solution score is {}'.format(evaluator(bestSol)))
    print('Solution weigth is {}'.format(knapsackWeight(bestSol)))

if __name__ == "__main__":
    main()