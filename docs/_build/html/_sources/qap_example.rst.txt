===============================
Quadratric Assignment Problem
===============================

This example will deal with the use of the **Macop** package in relation to a quadratic assignment problem (QAP). We will use a known example of this problem to associate a set of facilities (:math:`F`) to a set of locations (:math:`L`).

.. image:: _static//examples/qap/factories_qap.png
   :width: 50 %
   :align: center
   :alt: Example of QAP facilities to locations problem


.. note:: 
   The full code for what will be proposed in this example is available: qapExample.py_.

.. _qapExample.py: https://github.com/jbuisine/macop/blob/master/examples/qapExample.py


QAP problem definition
======================

The quadratic assignment problem (QAP) was introduced by Koopmans and Beckman in 1957 in the context of locating "indivisible economic activities". The objective of the problem is to assign a set of facilities to a set of locations in such a way as to minimize the total assignment cost. The assignment cost for a pair of facilities is a function of the flow between the facilities and the distance between the locations of the facilities.

Location assignment example
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Consider a **facility location problem** with **four** facilities (and **four** locations). One possible assignment is shown in the figure below: facility 4 is assigned to location 1, facility 1 
is assigned to location 2, facility 3 is assigned to location 3, and facility 2 is assigned to location 3. This assignment can be written as the permutation :math:`p=\{4,1,3,2\}`, 
which means that facility 4 is assigned to location 1, facility 1 is assigned to location 2, facility 3 is assigned to location 3, and facility 2 is assigned to location 3. 
In the figure, the line between a pair of facilities indicates that there is required flow between the facilities, and the thickness of the line increases with the value of the flow. 

.. image:: _static/examples/qap/factories_qap.png
   :width: 50 %
   :align: center
   :alt: Example of QAP facilities to locations problem


To calculate the assignment cost of the permutation, the required flows between facilities and the distances between locations are needed.


.. tabularcolumns:: |p{1cm}|p{1cm}|p{1cm}|p{1cm}|

.. csv-table:: flow of the current facilities
   :header: facility `i`, facility `j`, flow( `i`\, `j` )
   :widths: 2, 2, 3

   1, 4, 4
   3, 4, 10  
   3, 1, 8
   2, 1, 6  


.. csv-table:: distances of between locations
   :header: location `i`, location `j`, distances( `i`\, `j` )
   :widths: 2, 2, 3

   1, 2, 42
   1, 3, 30  
   2, 3, 41
   3, 4, 23  


Then, the assignment cost of the permutation can be computed as:

:math:`f(1,4)⋅d(1,2)+f(3,4)⋅d(1,3)+f(1,3)⋅d(2,3)+f(3,2)⋅d(3,4)` 
with result :math:`4⋅42+10⋅30+8⋅41+6⋅23=934`.

Note that this permutation is not the optimal solution.

Mathematical definition
~~~~~~~~~~~~~~~~~~~~~~~

**Sets**

- :math:`N=\{1,2,⋯,n\}`
- :math:`S_n=\phi:N→N` is the set of all permutations

**Parameters**

- :math:`F=(f_{ij})` is an :math:`n×n` matrix where :math:`f_{ij}` is the required flow between facilities :math:`i` and :math:`j`
- :math:`D=(d_{ij})` is an :math:`n×n` matrix where :math:`d_{ij}` is the distance between locations :math:`i` and :math:`j`.

**Optimization Problem**

- :math:`min_{ϕ∈S_n}\sum_{i=1}^{n}{\sum_{j=1}^{n}{f_{ij}⋅d_{\phi(i)\phi(j)}}}`

The assignment of facilities to locations is represented by a permutation :math:`\phi`, where :math:`\phi(i)` is the location to which facility :math:`i` is assigned. Each individual product :math:`f_{ij}⋅d_{\phi(i)\phi(j)}` is the cost of assigning facility :math:`i` to location :math:`\phi(i)` and facility :math:`j` to location :math:`\phi(j)`.

QAP Problem instance generation
===============================

To define our quadratic assignment problem instance, we will use the available mQAP_ multi-objective quadratic problem generator. 

Genration of the instance
~~~~~~~~~~~~~~~~~~~~~~~~~

We will limit ourselves here to a single objective for the purposes of this example. The file **makeQAPuni.cc**, will be used to generate the instance.

.. code:: bash

    g++ makeQAPuni.cc -o mQAPGenerator
    ./mQAPGenerator -n 100 -k 1 -f 30 -d 80 -s 42 > qap_instance.txt

with the following parameters:

- **-n** positive integer: number of facilities/locations;
- **-k** positive integer: number of objectives;
- **-f** positive integer: maximum flow between facilities;
- **-d** positive integer: maximum distance between locations;
- **-s** positive long: random seed.

The generated qap_instance.txt_ file contains the two matrices :math:`F` and :math:`D` and define our instance problem.

.. _mQAP: https://www.cs.bham.ac.uk/~jdk/mQAP/

.. _qap_instance.txt: https://github.com/jbuisine/macop/blob/master/examples/instances/qap/qap_instance.txt


Load data instance
~~~~~~~~~~~~~~~~~~


We are now going to load this instance via a Python code which will be useful to us later on:

.. code:: Python

    qap_instance_file = 'qap_instance.txt'

    n = 100 # the instance size

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

.. note::
    As we know the size of our instance and the structure of the document, it is quite quick to look for the lines related to the :math:`F` and :math:`D` matrices.

Macop QAP implementation
========================

Let's see how it is possible with the use of the **Macop** package to implement and deal with this QAP instance problem.

Solution structure definition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Firstly, we are going to use a type of solution that will allow us to define the structure of our solutions.

The available macop.solutions.discrete.CombinatoryIntegerSolution_ type of solution within the Macop package represents exactly what one would wish for. 
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

So we are going to create a class that will inherit from the abstract class macop.evaluators.base.Evaluator_:


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
        for index_i, val_i in enumerate(solution.getdata = )):
            for index_j, val_j in enumerate(solution.getdata = )):
                fitness += self._data['F'][index_i, index_j] * self._data['D'][val_i, val_j]

        return fitness

The cost function for the quadratic problem is now well defined.

.. tip::
    The class proposed here, is available in the Macop package macop.evaluators.discrete.mono.QAPEvaluator_.

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
        if len(list(solution.getdata = ))) > len(set(list(solution.getdata = )))):
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


.. _macop.solutions.discrete.CombinatoryIntegerSolution: macop/macop.solutions.discrete.html#macop.solutions.discrete.CombinatoryIntegerSolution
.. _macop.evaluators.base.Evaluator: macop/macop.evaluators.base.html#macop.evaluators.base.Evaluator
.. _macop.evaluators.discrete.mono.QAPEvaluator: macop/macop.evaluators.discrete.mono.html#macop.evaluators.discrete.mono.QAPEvaluator