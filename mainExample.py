# main imports
import logging
import os

# module imports
from macop.algorithms.IteratedLocalSearch import IteratedLocalSearch as ILS
from macop.solutions.BinarySolution import BinarySolution
from macop.evaluators.EvaluatorExample import evaluatorExample

from macop.operators.mutators.SimpleMutation import SimpleMutation
from macop.operators.mutators.SimpleBinaryMutation import SimpleBinaryMutation
from macop.operators.crossovers.SimpleCrossover import SimpleCrossover
from macop.operators.crossovers.RandomSplitCrossover import RandomSplitCrossover

from macop.operators.policies.RandomPolicy import RandomPolicy

from macop.checkpoints.BasicCheckpoint import BasicCheckpoint

if not os.path.exists('data'):
    os.makedirs('data')

# logging configuration
logging.basicConfig(format='%(asctime)s %(message)s', filename='data/example.log', level=logging.DEBUG)

# default validator
def validator(solution):
    return True

# define init random solution
def init():
    return BinarySolution([], 30).random(validator)

filepath = "data/checkpoints.csv"

def main():

    operators = [SimpleBinaryMutation(), SimpleMutation(), SimpleCrossover(), RandomSplitCrossover()]
    policy = RandomPolicy(operators)

    algo = ILS(init, evaluatorExample, operators, policy, validator, True)
    algo.addCheckpoint(_class=BasicCheckpoint, _every=5, _filepath=filepath)

    bestSol = algo.run(425)

    print("Found ", bestSol)


if __name__ == "__main__":
    main()