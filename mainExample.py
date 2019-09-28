# main imports
import logging

# module imports

# Note: you need to import from folder dependency name
# examples: `from optimization.solutions.BinarySolution import BinarySolution`

from optimization.algorithms.IteratedLocalSearch import IteratedLocalSearch as ILS
from optimization.solutions.BinarySolution import BinarySolution
from optimization.evaluators.EvaluatorExample import evaluatorExample

from optimization.operators.mutators.SimpleMutation import SimpleMutation
from optimization.operators.mutators.SimpleBinaryMutation import SimpleBinaryMutation
from optimization.operators.crossovers.SimpleCrossover import SimpleCrossover

from optimization.operators.policies.RandomPolicy import RandomPolicy

from optimization.checkpoints.BasicCheckpoint import BasicCheckpoint

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

    operators = [SimpleBinaryMutation(), SimpleMutation(), SimpleCrossover()]
    policy = RandomPolicy(operators)

    algo = ILS(init, evaluatorExample, operators, policy, validator, True)
    algo.addCheckpoint(_class=BasicCheckpoint, _every=5, _filepath=filepath)

    bestSol = algo.run(425)

    print("Found ", bestSol)


if __name__ == "__main__":
    main()