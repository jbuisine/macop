"""Classical policies classes implementations
"""
# main imports
import random

# module imports
from macop.policies.base import Policy


class RandomPolicy(Policy):
    """Policy class implementation which is used for select operator randomly from the `operators` list

    Attributes:
        operators: {[:class:`~macop.operators.base.Operator`]} -- list of selected operators for the algorithm

    Example:

    >>> import random
    >>> random.seed(42)
    >>> from macop.operators.discrete.crossovers import SimpleCrossover
    >>> from macop.operators.discrete.mutators import SimpleMutation
    >>> from macop.policies.classicals import RandomPolicy
    >>>
    >>> # create policy instance and select next operator to apply using policy
    >>> policy = RandomPolicy([SimpleCrossover(), SimpleMutation()])
    >>> operator = policy.select()
    >>> type(operator).__name__
    'SimpleCrossover'
    """
    def select(self):
        """Select randomly the next operator to use

        Returns:
            {:class:`~macop.operators.base.Operator`}: the selected operator

        """
        # choose operator randomly
        index = random.randint(0, len(self.operators) - 1)
        return self.operators[index]
