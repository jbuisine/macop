# main imports
import random
import sys

# module imports
from .Crossover import Crossover

from ...solutions.BinarySolution import BinarySolution
from ...solutions.Solution import Solution


class RandomSplitCrossover(Crossover):
    def apply(self, solution):
        size = solution.size

        # copy data of solution
        firstData = solution.data.copy()
        # get best solution from current algorithm
        secondData = self.algo.bestSolution.data.copy()

        splitIndex = random.randint(0, len(secondData))

        if random.uniform(0, 1) > 0.5:
            firstData[splitIndex:(size - 1)] = firstData[splitIndex:(size - 1)]
            currentData = firstData
        else:
            secondData[splitIndex:(size - 1)] = firstData[splitIndex:(size -
                                                                      1)]
            currentData = secondData

        # create solution of same kind with new data
        return globals()[type(solution).__name__](currentData, size)
