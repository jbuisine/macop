# main imports
import logging

# module imports

# Note: you need to import from folder dependency name
# examples: `from optimization.solutions.BinarySolution import BinarySolution`

from optimization.algorithms.IteratedLocalSearch import IteratedLocalSearch as ILS
from optimization.solutions.BinarySolution import BinarySolution
from optimization.evaluators.EvaluatorExample import evaluatorExample

from optimization.updators.mutators.SimpleMutation import SimpleMutation, SimpleBinaryMutation
from optimization.updators.policies.RandomPolicy import RandomPolicy

# logging configuration
logging.basicConfig(format='%(asctime)s %(message)s', filename='example.log', level=logging.DEBUG)

# default validator
def validator(solution):
    return True

# define init random solution
def init():
    return BinarySolution([], 30).random(validator)

def main():

    updators = [SimpleBinaryMutation, SimpleMutation]
    policy = RandomPolicy(updators)

    algo = ILS(init, evaluatorExample, updators, policy, validator, True)

    bestSol = algo.run(100000)

    print("Found ", bestSol)


if __name__ == "__main__":
    main()