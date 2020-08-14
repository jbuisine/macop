# main imports
import logging

# module imports

# Note: you need to import from folder dependency name
# examples: `from optimization.solutions.BinarySolution import BinarySolution`

from macop.algorithms.IteratedLocalSearch import IteratedLocalSearch as ILS
from macop.solutions.BinarySolution import BinarySolution
from macop.evaluators.EvaluatorExample import evaluatorExample

from macop.operators.mutators.SimpleMutation import SimpleMutation
from macop.operators.mutators.SimpleBinaryMutation import SimpleBinaryMutation
from macop.operators.crossovers.SimpleCrossover import SimpleCrossover
from macop.operators.crossovers.RandomSplitCrossover import RandomSplitCrossover

from macop.operators.policies.RandomPolicy import RandomPolicy

from macop.checkpoints.BasicCheckpoint import BasicCheckpoint

# logging configuration
logging.basicConfig(format='%(asctime)s %(message)s', filename='example.log', level=logging.DEBUG)

# default validator
def validator(solution):
    return True

# define init random solution
def init():
    return BinarySolution([], 30).random(validator)

filepath = "checkpoints.csv"

def main():

    operators = [SimpleBinaryMutation(), SimpleMutation(), SimpleCrossover(), RandomSplitCrossover()]
    policy = RandomPolicy(operators)

    algo = ILS(init, evaluatorExample, operators, policy, validator, True)
    algo.addCheckpoint(_class=BasicCheckpoint, _every=5, _filepath=filepath)

    bestSol = algo.run(425)

    print("Found ", bestSol)


if __name__ == "__main__":
    main()