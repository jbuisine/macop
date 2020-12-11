"""Abstract Mutation class
"""
# module imports
from ..Operator import KindOperator, Operator


# main mutation class
class Mutation(Operator):
    """Abstract Mutation extend from Operator

    Attributes:
        kind: {KindOperator} -- specify the kind of operator
    """
    def __init__(self):
        self._kind = KindOperator.MUTATOR

    def apply(self, solution):
        raise NotImplementedError
