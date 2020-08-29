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
from macop.callbacks.MultiCheckpoint import MultiCheckpoint
from macop.callbacks.ParetoCheckpoint import ParetoCheckpoint

if not os.path.exists('data'):
    os.makedirs('data')

# logging configuration
logging.basicConfig(format='%(asctime)s %(message)s', filename='data/exampleMOEAD.log', level=logging.DEBUG)

random.seed(42)

elements_score1 = [ random.randint(1, 100) for _ in range(500) ]
elements_score2 = [ random.randint(1, 200) for _ in range(500) ]
elements_weight = [ random.randint(90, 100) for _ in range(500) ]

def knapsackWeight(_solution):

    weight_sum = 0
    for index, elem in enumerate(_solution.data):
        weight_sum += elements_weight[index] * elem

    return weight_sum

# default validator
def validator(_solution):

    if knapsackWeight(_solution) <= 15000:
        return True
    else:
        False

# define init random solution
def init():
    return BinarySolution([], 200).random(validator)

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


mo_checkpoint_path = "data/checkpointsMOEAD.csv"
pf_checkpoint_path = "data/pfMOEAD.csv"


def main():

    operators = [SimpleBinaryMutation(), SimpleMutation(), SimpleCrossover(), RandomSplitCrossover()]
    policy = RandomPolicy(operators)

    # pass list of evaluators
    algo = MOEAD(20, 5, init, [evaluator1, evaluator2, evaluator2, evaluator2], operators, policy, validator, _maximise=True)
    print(algo.weights)
    algo.addCallback(MultiCheckpoint(_every=5, _filepath=mo_checkpoint_path))
    algo.addCallback(ParetoCheckpoint(_every=5, _filepath=pf_checkpoint_path))

    paretoFront = algo.run(10000)

    print("Pareto front is composed of", len(paretoFront), "solutions")

if __name__ == "__main__":
    main()