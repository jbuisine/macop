"""Classical policies classes implementations
"""
# main imports
import random

# module imports
from .base import Policy


class RandomPolicy(Policy):
    """Policy class implementation which is used for select operator randomly

    Attributes:
        operators: {[Operator]} -- list of selected operators for the algorithm
    """
    def select(self):
        """Select randomly the next operator to use

        Returns:
            {Operator}: the selected operator
        """
        # choose operator randomly
        index = random.randint(0, len(self._operators) - 1)
        return self._operators[index]
