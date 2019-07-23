# main imports
import random
import sys

# module imports
from .Mutation import Mutation

from ...solutions.BinarySolution import BinarySolution
from ...solutions.Solution import Solution

class SimpleBinaryMutation(Mutation):

    def apply(self, solution):
        size = solution.size

        cell = random.randint(0, size - 1)

        # copy data of solution
        currentData = solution.data.copy()

        # swicth values
        if currentData[cell]:
            currentData[cell] = 0
        else:
            currentData[cell] = 1

        # create solution of same kind with new data
        return globals()[type(solution).__name__](currentData, size)