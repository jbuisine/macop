# main imports
import logging
import os
import random

# module imports
from macop.solutions.discrete import BinarySolution
from macop.evaluators.discrete.mono import KnapsackEvaluator

from macop.operators.discrete.mutators import SimpleMutation
from macop.operators.discrete.mutators import SimpleBinaryMutation
from macop.operators.discrete.crossovers import SimpleCrossover
from macop.operators.discrete.crossovers import RandomSplitCrossover

from macop.policies.classicals import RandomPolicy
from macop.policies.reinforcement import UCBPolicy

from macop.algorithms.multi import MOEAD
from macop.callbacks.multi import MultiCheckpoint
from macop.callbacks.multi import ParetoCheckpoint
from macop.callbacks.policies import UCBCheckpoint

if not os.path.exists('data'):
    os.makedirs('data')

# logging configuration
logging.basicConfig(format='%(asctime)s %(message)s', filename='data/example_MOEAD_knapsack.log', level=logging.DEBUG)

random.seed(42)

elements_score1 = [ random.randint(1, 100) for _ in range(500) ]
elements_score2 = [ random.randint(1, 200) for _ in range(500) ]
elements_weight = [ random.randint(90, 100) for _ in range(500) ]

def knapsackWeight(solution):

    weight_sum = 0
    for index, elem in enumerate(solution.getData()):
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
    return BinarySolution.random(200, validator)
    

mo_checkpoint_path = "data/checkpointsMOEAD.csv"
pf_checkpoint_path = "data/pfMOEAD.csv"
ucb_checkpoint_path = "data/UCBPolicyMOEAD.csv"


def main():

    operators = [SimpleBinaryMutation(), SimpleMutation(), SimpleCrossover(), RandomSplitCrossover()]
    policy = UCBPolicy(operators, C=100, exp_rate=0.2)

    evaluator1 = KnapsackEvaluator(data={'worths': elements_score1})
    evaluator2 = KnapsackEvaluator(data={'worths': elements_score2})

    # pass list of evaluators
    algo = MOEAD(20, 5, init, [evaluator1, evaluator2], operators, policy, validator, maximise=True)
    
    algo.addCallback(MultiCheckpoint(every=5, filepath=mo_checkpoint_path))
    algo.addCallback(ParetoCheckpoint(every=5, filepath=pf_checkpoint_path))
    algo.addCallback(UCBCheckpoint(every=5, filepath=ucb_checkpoint_path))

    paretoFront = algo.run(1000)

    print("Pareto front is composed of", len(paretoFront), "solutions")

if __name__ == "__main__":
    main()