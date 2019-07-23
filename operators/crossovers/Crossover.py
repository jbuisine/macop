# module imports
from ..Operator import Operator

# main mutation class
class Crossover():

    def __init__(self):
        self.kind = Operator.CROSSOVER

    def apply(self, solution, secondSolution=None):
        raise NotImplementedError