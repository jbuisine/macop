# module imports
from ..Operator import KindOperator, Operator


# main mutation class
class Mutation(Operator):
    def __init__(self):
        self.kind = KindOperator.MUTATOR

    def apply(self, solution):
        raise NotImplementedError
