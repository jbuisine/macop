"""Abstract Crossover class
"""
# module imports
from ..Operator import KindOperator, Operator


# main mutation class
class Crossover(Operator):
    """Abstract crossover extend from Operator

    Attributes:
        kind: {KindOperator} -- specify the kind of operator
    """
    def __init__(self):
        self.kind = KindOperator.CROSSOVER

    def apply(self, solution):
        raise NotImplementedError
