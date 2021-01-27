Macop QAP implementation
========================

Let's see how it is possible with the use of the **Macop** package to implement and deal with this QAP instance problem.

Solution structure definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Firstly, we are going to use a type of solution that will allow us to define the structure of our solutions.

The available ``macop.solutions.discrete.CombinatoryIntegerSolution`` type of solution within the Macop package represents exactly what one would wish for. 
I.e. a solution that stores a sequence of integers relative to the size of the problem, the order of which is not sorted.

Let's see an example of its use:

.. code:: python

    from macop.solutions.discrete import CombinatoryIntegerSolution
    
    solution = CombinatoryIntegerSolution.random(10)
    print(solution)


The resulting solution obtained:

.. code:: bash

    Combinatory integer solution [2 9 8 1 7 6 0 4 3 5]


QAP Evaluator
~~~~~~~~~~~~~

Now that we have the structure of our solutions, and the means to generate them, we will seek to evaluate them.

To do this, we need to create a new evaluator specific to our problem and the relative evaluation function:

- :math:`min_{ϕ∈S_n}\sum_{i=1}^{n}{\sum_{j=1}^{n}{f_{ij}⋅d_{\phi(i)\phi(j)}}}`

So we are going to create a class that will inherit from the abstract class ``macop.evalutarors.base.Evaluator``:


.. code:: python

    from macop.evaluators.base import Evaluator

    class QAPEvaluator(Evaluator):
    """QAP evaluator class which enables to compute QAP solution using specific `_data`

    - stores into its `_data` dictionary attritute required measures when computing a QAP solution
    - `_data['F']` matrix of size n x n with flows data between facilities (stored as numpy array)
    - `_data['D']` matrix of size n x n with distances data between locations (stored as numpy array)
    - `compute` method enables to compute and associate a score to a given QAP solution
    """

    def compute(self, solution):
        """Apply the computation of fitness from solution

        Args:
            solution: {Solution} -- QAP solution instance
    
        Returns:
            {float} -- fitness score of solution
        """
        fitness = 0
        for index_i, val_i in enumerate(solution.getData()):
            for index_j, val_j in enumerate(solution.getData()):
                fitness += self._data['F'][index_i, index_j] * self._data['D'][val_i, val_j]

        return fitness

The cost function for the quadratic problem is now well defined.

.. tip::
    The class proposed here, is available in the Macop package ``macop.evaluators.discrete.mono.QAPEvaluator``.

Running algorithm
~~~~~~~~~~~~~~~~~

Now that the necessary tools are available, we will be able to deal with our problem and look for solutions in the search space of our QAP instance.

Here we will use local search algorithms already implemented in **Macop**.

If you are uncomfortable with some of the elements in the code that will follow, you can refer to the more complete **Macop** documentation_ that focuses more on the concepts and tools of the package.

.. code:: python

    # main imports
    import numpy as np

    # module imports
    from macop.solutions.discrete import CombinatoryIntegerSolution
    from macop.evaluators.discrete.mono import QAPEvaluator

    from macop.operators.discrete.mutators import SimpleMutation

    from macop.policies.classicals import RandomPolicy

    from macop.algorithms.mono import IteratedLocalSearch as ILS
    from macop.algorithms.mono import HillClimberFirstImprovment

    # usefull instance data
    n = 100
    qap_instance_file = 'qap_instance.txt'

    # default validator (check the consistency of our data, i.e. only unique element)
    def validator(solution):
        if len(list(solution.getData())) > len(set(list(solution.getData()))):
            print("not valid")
            return False
        return True

    # define init random solution
    def init():
        return CombinatoryIntegerSolution.random(n, validator)

    # load qap instance
    with open(qap_instance_file, 'r') as f:
        file_data = f.readlines()
        print(f'Instance information {file_data[0]}')

        D_lines = file_data[1:n + 1]
        D_data = ''.join(D_lines).replace('\n', '')

        F_lines = file_data[n:2 * n + 1]
        F_data = ''.join(F_lines).replace('\n', '')

    D_matrix = np.fromstring(D_data, dtype=float, sep=' ').reshape(n, n)
    print(f'D matrix shape: {D_matrix.shape}')
    F_matrix = np.fromstring(F_data, dtype=float, sep=' ').reshape(n, n)
    print(f'F matrix shape: {F_matrix.shape}')

    # only one operator here
    operators = [SimpleMutation()]

    # random policy even if list of solution has only one element
    policy = RandomPolicy(operators)

    # use of loaded data from QAP instance
    evaluator = QAPEvaluator(data={'F': F_matrix, 'D': D_matrix})

    # passing global evaluation param from ILS
    hcfi = HillClimberFirstImprovment(init, evaluator, operators, policy, validator, maximise=False, verbose=True)
    algo = ILS(init, evaluator, operators, policy, validator, localSearch=hcfi, maximise=False, verbose=True)

    # run the algorithm
    bestSol = algo.run(10000, ls_evaluations=100)

    print('Solution for QAP instance score is {}'.format(evaluator.compute(bestSol)))


QAP problem solving is now possible with **Macop**. As a reminder, the complete code is available in the qapExample.py_ file.

.. _qapExample.py: https://github.com/jbuisine/macop/blob/master/examples/qapExample.py
.. _documentation: https://jbuisine.github.io/macop/_build/html/documentations