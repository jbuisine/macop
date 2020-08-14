# module imports
from ..Operator import KindOperator, Operator


# main mutation class
class Crossover(Operator):
    def __init__(self):
        self.kind = KindOperator.CROSSOVER
