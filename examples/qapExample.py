# main imports
import logging
import os
import random
import numpy as np

# module imports
from macop.solutions.discrete import CombinatoryIntegerSolution
from macop.evaluators.discrete.mono import QAPEvaluator

from macop.operators.discrete.mutators import SimpleMutation

from macop.policies.classicals import RandomPolicy
from macop.policies.reinforcement import UCBPolicy

from macop.algorithms.mono import IteratedLocalSearch as ILS
from macop.algorithms.mono import HillClimberFirstImprovment
from macop.callbacks.classicals import BasicCheckpoint

if not os.path.exists('data'):
    os.makedirs('data')

# logging configuration
logging.basicConfig(format='%(asctime)s %(message)s', filename='data/example_qap.log', level=logging.DEBUG)

random.seed(42)

# usefull instance data
n = 100
qap_instance_file = 'instances/qap/qap_instance.txt'
filepath = "data/checkpoints_qap.csv"


# default validator
def validator(solution):
    if len(list(solution.data)) > len(set(list(solution.data))):
        print("not valid")
        return False
    return True

# define init random solution
def init():
    return CombinatoryIntegerSolution.random(n, validator)


def main():

    with open(qap_instance_file, 'r') as f:
        file_data = f.readlines()
        print(f'Instance information {file_data[0]}')

        D_lines = file_data[1:n + 1]
        D_data = ''.join(D_lines).replace('\n', '')

        F_lines = file_data[n:2 * n + 1]
        F_data = ''.join(F_lines).replace('\n', '')

    D_matrix = np.fromstring(D_data, dtype=float, sep=' ').reshape(n, n)
    print(f'D matrix shape: {D_matrix.shape}')
    F_matrix = np.fromstring(F_data, dtype=float, sep=' ').reshape(n, n)
    print(f'F matrix shape: {F_matrix.shape}')

    operators = [SimpleMutation()]
    policy = RandomPolicy(operators)
    callback = BasicCheckpoint(every=5, filepath=filepath)
    evaluator = QAPEvaluator(data={'F': F_matrix, 'D': D_matrix})

    # passing global evaluation param from ILS
    hcfi = HillClimberFirstImprovment(init, evaluator, operators, policy, validator, maximise=False, verbose=True)
    algo = ILS(init, evaluator, operators, policy, validator, localSearch=hcfi, maximise=False, verbose=True)
    
    # add callback into callback list
    algo.addCallback(callback)

    bestSol = algo.run(10000, ls_evaluations=100)

    print('Solution for QAP instance score is {}'.format(evaluator.compute(bestSol)))

if __name__ == "__main__":
    main()