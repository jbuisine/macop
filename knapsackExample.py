# main imports
import logging
import os
import random

# module imports
from macop.algorithms.IteratedLocalSearch import IteratedLocalSearch as ILS
from macop.solutions.BinarySolution import BinarySolution
from macop.evaluators.EvaluatorExample import evaluatorExample

from macop.operators.mutators.SimpleMutation import SimpleMutation
from macop.operators.mutators.SimpleBinaryMutation import SimpleBinaryMutation
from macop.operators.crossovers.SimpleCrossover import SimpleCrossover
from macop.operators.crossovers.RandomSplitCrossover import RandomSplitCrossover

from macop.operators.policies.RandomPolicy import RandomPolicy
from macop.operators.policies.UCBPolicy import UCBPolicy

from macop.checkpoints.BasicCheckpoint import BasicCheckpoint

if not os.path.exists('data'):
    os.makedirs('data')

# logging configuration
logging.basicConfig(format='%(asctime)s %(message)s', filename='data/example.log', level=logging.DEBUG)

random.seed(42)

elements_score = [ random.randint(1, 20) for _ in range(30) ]
elements_weight = [ random.randint(2, 5) for _ in range(30) ]

def knapsackWeight(_solution):

    weight_sum = 0
    for index, elem in enumerate(_solution.data):
        weight_sum += elements_weight[index] * elem

    return weight_sum

# default validator
def validator(_solution):

    if knapsackWeight(_solution) <= 80:
        return True
    else:
        False

# define init random solution
def init():
    return BinarySolution([], 30).random(validator)

def evaluator(_solution):

    fitness = 0
    for index, elem in enumerate(_solution.data):
        fitness += (elements_score[index] * elem)

    return fitness

filepath = "data/checkpoints.csv"

def main():

    operators = [SimpleBinaryMutation(), SimpleMutation(), SimpleCrossover(), RandomSplitCrossover()]
    policy = UCBPolicy(operators)

    algo = ILS(init, evaluator, operators, policy, validator, _maximise=True)
    algo.addCheckpoint(_class=BasicCheckpoint, _every=5, _filepath=filepath)

    bestSol = algo.run(10000)

    print('Solution score is {}'.format(evaluator(bestSol)))
    print('Solution weigth is {}'.format(knapsackWeight(bestSol)))

if __name__ == "__main__":
    main()