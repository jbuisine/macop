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

from macop.algorithms.multi.MOEAD import MOEAD
from macop.checkpoints.BasicCheckpoint import BasicCheckpoint

if not os.path.exists('data'):
    os.makedirs('data')

# logging configuration
logging.basicConfig(format='%(asctime)s %(message)s', filename='data/exampleMOEAD.log', level=logging.DEBUG)

random.seed(42)

elements_score1 = [ random.randint(1, 20) for _ in range(30) ]
elements_score2 = [ random.randint(1, 20) for _ in range(30) ]
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

def evaluator1(_solution):

    fitness = 0
    for index, elem in enumerate(_solution.data):
        fitness += (elements_score1[index] * elem)

    return fitness

def evaluator2(_solution):

    fitness = 0
    for index, elem in enumerate(_solution.data):
        fitness += (elements_score2[index] * elem)

    return fitness


filepath = "data/checkpointsMOEAD.csv"

def main():

    operators = [SimpleBinaryMutation(), SimpleMutation(), SimpleCrossover(), RandomSplitCrossover()]
    policy = UCBPolicy(operators)

    # pass list of evaluators
    algo = MOEAD(20, 5, init, [evaluator1, evaluator2], operators, policy, validator, _maximise=True)
    algo.addCheckpoint(_class=BasicCheckpoint, _every=5, _filepath=filepath)

    bestSol = algo.run(1000)
    bestSol = algo.run(1000)

    print('Solution score1 is {}'.format(evaluator1(bestSol)))
    print('Solution score2 is {}'.format(evaluator2(bestSol)))
    print('Solution weigth is {}'.format(knapsackWeight(bestSol)))

if __name__ == "__main__":
    main()