# main imports
import logging
import os
import random
import numpy as np

# module imports
from macop.solutions.discrete import BinarySolution
from macop.evaluators.discrete.mono import UBQPEvaluator

from macop.operators.discrete.mutators import SimpleMutation
from macop.operators.discrete.mutators import SimpleBinaryMutation

from macop.policies.classicals import RandomPolicy

from macop.algorithms.mono import IteratedLocalSearch as ILS
from macop.algorithms.mono import HillClimberFirstImprovment
from macop.callbacks.classicals import BasicCheckpoint

if not os.path.exists('data'):
    os.makedirs('data')

# logging configuration
logging.basicConfig(format='%(asctime)s %(message)s', filename='data/example.log', level=logging.DEBUG)

random.seed(42)

# usefull instance data
n = 100
ubqp_instance_file = 'instances/ubqp/ubqp_instance.txt'
filepath = "data/checkpoints_ubqp.csv"


# default validator
def validator(solution):
    return True

# define init random solution
def init():
    return BinarySolution.random(n, validator)


filepath = "data/checkpoints.csv"

def main():

    # load UBQP instance
    with open(ubqp_instance_file, 'r') as f:

        lines = f.readlines()

        # get all string floating point values of matrix
        Q_data = ''.join([ line.replace('\n', '') for line in lines[8:] ])

        # load the concatenate obtained string
        Q_matrix = np.fromstring(Q_data, dtype=float, sep=' ').reshape(n, n)

    print(f'Q_matrix shape: {Q_matrix.shape}')

    operators = [SimpleBinaryMutation(), SimpleMutation()]
    policy = RandomPolicy(operators)
    callback = BasicCheckpoint(every=5, filepath=filepath)
    evaluator = UBQPEvaluator(data={'Q': Q_matrix})

    # passing global evaluation param from ILS
    hcfi = HillClimberFirstImprovment(init, evaluator, operators, policy, validator, maximise=True, verbose=True)
    algo = ILS(init, evaluator, operators, policy, validator, localSearch=hcfi, maximise=True, verbose=True)
    
    # add callback into callback list
    algo.addCallback(callback)

    bestSol = algo.run(10000, ls_evaluations=100)

    print('Solution for UBQP instance score is {}'.format(evaluator.compute(bestSol)))

if __name__ == "__main__":
    main()