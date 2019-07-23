# module imports
from ..Operator import Operator

# main mutation class
class Mutation():

    def __init__(self):
        self.kind = Operator.MUTATOR

    def apply(self, solution):
        raise NotImplementedError