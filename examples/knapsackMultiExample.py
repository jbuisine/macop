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
from macop.callbacks.UCBCheckpoint import UCBCheckpoint

if not os.path.exists('data'):
    os.makedirs('data')

# logging configuration
logging.basicConfig(format='%(asctime)s %(message)s', filename='data/exampleMOEAD.log', level=logging.DEBUG)

random.seed(42)

elements_score1 = [ random.randint(1, 100) for _ in range(500) ]
elements_score2 = [ random.randint(1, 200) for _ in range(500) ]
elements_weight = [ random.randint(90, 100) for _ in range(500) ]

def knapsackWeight(solution):

    weight_sum = 0
    for index, elem in enumerate(solution._data):
        weight_sum += elements_weight[index] * elem

    return weight_sum

# default validator
def validator(solution):

    if knapsackWeight(solution) <= 15000:
        return True
    else:
        False

# define init random solution
def init():
    return BinarySolution([], 200).random(validator)

def evaluator1(solution):

    fitness = 0
    for index, elem in enumerate(solution._data):
        fitness += (elements_score1[index] * elem)

    return fitness

def evaluator2(solution):

    fitness = 0
    for index, elem in enumerate(solution._data):
        fitness += (elements_score2[index] * elem)

    return fitness


mo_checkpoint_path = "data/checkpointsMOEAD.csv"
pf_checkpoint_path = "data/pfMOEAD.csv"
ucb_checkpoint_path = "data/UCBPolicyMOEAD.csv"


def main():

    operators = [SimpleBinaryMutation(), SimpleMutation(), SimpleCrossover(), RandomSplitCrossover()]
    policy = UCBPolicy(operators, C=100, exp_rate=0.2)

    # pass list of evaluators
    algo = MOEAD(20, 5, init, [evaluator1, evaluator2], operators, policy, validator, maximise=True)
    
    algo.addCallback(MultiCheckpoint(every=5, filepath=mo_checkpoint_path))
    algo.addCallback(ParetoCheckpoint(every=5, filepath=pf_checkpoint_path))
    algo.addCallback(UCBCheckpoint(every=5, filepath=ucb_checkpoint_path))

    paretoFront = algo.run(1000)

    print("Pareto front is composed of", len(paretoFront), "solutions")

if __name__ == "__main__":
    main()