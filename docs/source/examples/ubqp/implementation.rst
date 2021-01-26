Macop UBQP implementation
=========================

Let's see how it is possible with the use of the **Macop** package to implement and deal with this UBQP instance problem.

Solution structure definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Firstly, we are going to use a type of solution that will allow us to define the structure of our solutions.

The available ``macop.solutions.discrete.BinarySolution`` type of solution within the Macop package represents exactly what one would wish for. 

Let's see an example of its use:

.. code:: python

    from macop.solutions.discrete import BinarySolution
    
    solution = BinarySolution.random(10)
    print(solution)


The resulting solution obtained:

.. code:: bash

    Binary solution [1 0 1 1 1 0 0 1 1 0]


UBQP Evaluator
~~~~~~~~~~~~~~

Now that we have the structure of our solutions, and the means to generate them, we will seek to evaluate them.

To do this, we need to create a new evaluator specific to our problem and the relative evaluation function we need to maximise:

- :math:`f(x)=x′Qx=\sum_{i=1}^{n}{\sum_{j=1}^{n}{q_{ij}⋅x_i⋅x_j}}`

So we are going to create a class that will inherit from the abstract class ``macop.evalutarors.base.Evaluator``:

.. code:: python

    from macop.evaluators.base import Evaluator

    class UBQPEvaluator(Evaluator):
    """UBQP evaluator class which enables to compute UBQP solution using specific `_data`

    - stores into its `_data` dictionary attritute required measures when computing a UBQP solution
    - `_data['Q']` matrix of size n x n with real values data (stored as numpy array)
    - `compute` method enables to compute and associate a score to a given UBQP solution
    """

    def compute(self, solution):
        """Apply the computation of fitness from solution

        Args:
            solution: {Solution} -- UBQP solution instance
    
        Returns:
            {float} -- fitness score of solution
        """
        fitness = 0
        for index_i, val_i in enumerate(solution._data):
            for index_j, val_j in enumerate(solution._data):
                fitness += self._data['Q'][index_i, index_j] * val_i * val_j

        return fitness

The cost function for the Unconstrained binary quadratic problem is now well defined.

.. warning::
    The class proposed here, is available in the Macop package ``macop.evaluators.discrete.mono.UBQPEvaluator``.

Running algorithm
~~~~~~~~~~~~~~~~~

Now that the necessary tools are available, we will be able to deal with our problem and look for solutions in the search space of our UBQP instance.

Here we will use local search algorithms already implemented in **Macop**.

If you are uncomfortable with some of the elements in the code that will follow, you can refer to the more complete **Macop** documentation_ that focuses more on the concepts and tools of the package.

.. code:: python

    # main imports
    import numpy as np

    # module imports
    from macop.solutions.discrete import BinarySolution
    from macop.evaluators.discrete.mono import UBQPEvaluator

    from macop.operators.discrete.mutators import SimpleMutation, SimpleBinaryMutation

    from macop.policies.classicals import RandomPolicy

    from macop.algorithms.mono import IteratedLocalSearch as ILS
    from macop.algorithms.mono import HillClimberFirstImprovment

    # usefull instance data
    n = 100
    qap_instance_file = 'qap_instance.txt'

    # default validator
    def validator(solution):
        return True

    # define init random solution
    def init():
        return BinarySolution.random(n, validator)

    # load UBQP instance
    with open(ubqp_instance_file, 'r') as f:

        lines = f.readlines()

        # get all string floating point values of matrix
        Q_data = ''.join([ line.replace('\n', '') for line in lines[8:] ])

        # load the concatenate obtained string
        Q_matrix = np.fromstring(Q_data, dtype=float, sep=' ').reshape(n, n)

    print(f'Q_matrix shape: {Q_matrix.shape}')

    # only one operator here
    operators = [SimpleMutation(), SimpleBinaryMutation()]

    # random policy
    policy = RandomPolicy(operators)

    # use of loaded data from UBQP instance
    evaluator = UBQPEvaluator(data={'Q': Q_matrix})

    # passing global evaluation param from ILS
    hcfi = HillClimberFirstImprovment(init, evaluator, operators, policy, validator, maximise=True, verbose=True)
    algo = ILS(init, evaluator, operators, policy, validator, localSearch=hcfi, maximise=True, verbose=True)

    # run the algorithm
    bestSol = algo.run(10000, ls_evaluations=100)

    print('Solution for UBQP instance score is {}'.format(evaluator.compute(bestSol)))


UBQP problem solving is now possible with **Macop**. As a reminder, the complete code is available in the ubqpExample.py_ file.

.. _ubqpExample.py: https://github.com/jbuisine/macop/blob/master/examples/ubqpExample.py
.. _documentation: https://jbuisine.github.io/macop/_build/html/documentations