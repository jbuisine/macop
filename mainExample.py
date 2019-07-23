# module imports

# Note: you need to import from folder dependency name
# examples: `from optimization.solutions.BinarySolution import BinarySolution`

from algorithms.IteratedLocalSearch import IteratedLocalSearch as ILS
from solutions.BinarySolution import BinarySolution
from evaluators.EvaluatorExample import evaluatorExample

from updators.mutators.SimpleMutation import SimpleMutation, SimpleBinaryMutation
from updators.policies.RandomPolicy import RandomPolicy

# define init random solution
def init():
    return BinarySolution([], 30).random()

# default validator
def validator(solution):
    return True

def main():

    updators = [SimpleBinaryMutation, SimpleMutation]
    policy = RandomPolicy(updators)

    algo = ILS(init, evaluatorExample, updators, policy, validator, True)

    bestSol = algo.run(100000)

    print("Found ", bestSol)


if __name__ == "__main__":
    main()