4. Validate a solution
======================

When an optimization problem requires respecting certain constraints, Macop allows you to quickly verify that a solution is valid. 
It is based on a defined function taking a solution as input and returning the validity criterion (true or false).

4.1. Validator definition
~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: python

    """
    Problem instance definition
    """

    elements_score = [ 4, 2, 10, 1, 2 ] # value of each object
    elements_weight = [ 12, 1, 4, 1, 2 ] # weight of each object

    """
    validator function definition
    """
    def validator(solution):

        weight_sum = 0

        for i, w in enumerate(elements_weight):
            weight_sum += w * solution._data[i]
        
        return weight_sum <= 15


4.2. Use of validator
~~~~~~~~~~~~~~~~~~~~~