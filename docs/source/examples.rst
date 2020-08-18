Some examples
=====================================

1. Mono-objective
-----------------------

In this tutorial, it will introduce the way of running your algorithm quickly.
First of all we need to define the kind of solution best represent the problem. In this tutorial, we use the well known knapsack problem using 30 objects.

1.1 Problem definition
~~~~~~~~~~~~~~~~~~~~~~

Hence, we define our problem :
- value of each component of knapsack
- weight associated to each of these components (objects)

.. code:: python
    
    """
    imports part
    """
    import random

    """
    Problem definition
    """
    random.seed(42)

    elements_score = [ random.randint(1, 20) for _ in range(30) ]
    elements_weight = [ random.randint(5, 25) for _ in range(30) ]

We can now define the solution representation. In knapsack problem we want to fill our knapsack in an optimization way selecting or not each component (object).
The best way to represent this problem is to use the `BinarySolution` from `macop` which stores solution as a binary array.

Using the solution representation, we need to define multiple things to fit our algorithm :
- 1. function which validates or not a solution (based on constraints)
- 2. function which evaluates the solution (in order to obtain fitness)
- 3. initialization solution function

.. code:: python
    
    """
    imports part
    """
    import random
    from macop.solutions.BinarySolution import BinarySolution

    """
    Problem definition
    """
    random.seed(42)

    elements_score = [ random.randint(1, 20) for _ in range(30) ]
    elements_weight = [ random.randint(2, 5) for _ in range(30) ]

    # 1. validator function (we accept only bag with maximum weight 80kg)
    def validator(_solution):

        weight_sum = 0
        for index, elem in enumerate(_solution.data):
            weight_sum += elements_weight[index] * elem

        if weight_sum <= 80:
            return True
        else:
            False

    # 2. function which computes fitness of solution
    def evaluator(_solution):

        fitness = 0
        for index, elem in enumerate(_solution.data):
            fitness += (elements_score[index] * elem)

        return fitness

    # 3. function which here initializes solution ramdomly and check validity of solution
    def init():
        return BinarySolution([], 30).random(validator)

1.2 Operators and Policy
~~~~~~~~~~~~~~~~~~~~~~~~

In our algorithm we need to use some operators in order to improve current best solution found at current `n` evaluations.

In `macop` you have some available operators. In this example, we use 3 of them.

.. code:: python
    
    """
    imports part
    """
    ...

    from macop.operators.mutators.SimpleMutation import SimpleMutation
    from macop.operators.mutators.SimpleBinaryMutation import SimpleBinaryMutation
    from macop.operators.crossovers.SimpleCrossover import SimpleCrossover

    """
    Problem definition
    """
    ...

    """
    Algorithm parameters
    """
    # list of operators instance to use
    operators = [SimpleBinaryMutation(), SimpleMutation(), SimpleCrossover(), RandomSplitCrossover()]

As we defined multiple operators, we have to tell how we want to select them into the algorithm. This is why **Policy** classes have been implemented.
`Policy` class implementation enables to select the next operator to use and once new solution is generated, computes its score (in `apply` method). This class requires all the operators use to be instanciate.

Why computing score into **Policy** `apply` method ? Because it's a way to get some important statistics from solution improvment using specific operator.
**UCBPolicy** as example, based on Upper Confidence Bound (UCB_), computes reward each time a new solution is generated from an operator in order to better select next operator later. We use in this example the `UCBPolicy` implementation.

.. _UCB: https://banditalgs.com/2016/09/18/the-upper-confidence-bound-algorithm/

.. code:: python
    
    """
    imports part
    """
    ...

    from macop.operators.mutators.SimpleMutation import SimpleMutation
    from macop.operators.mutators.SimpleBinaryMutation import SimpleBinaryMutation
    from macop.operators.crossovers.SimpleCrossover import SimpleCrossover

    from macop.operators.policies.UCBPolicy import UCBPolicy

    """
    Problem definition
    """
    ...

    """
    Algorithm parameters
    """
    # list of operators instance to use
    operators = [SimpleBinaryMutation(), SimpleMutation(), SimpleCrossover(), RandomSplitCrossover()]

    # `policy` instance is created using specific value for Upper Confidence Bound
    policy = UCBPolicy(operators, C=100.)

1.3 Before running algorithm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before running algorithm we can define a logger to keep track of the all algorithm run.

.. code:: python
    
    """
    imports part
    """
    ...

    import logging

    """
    Problem definition
    """
    ...

    """
    Algorithm parameters
    """
    ...

    if not os.path.exists('data'):
    os.makedirs('data')

    # logging configuration
    logging.basicConfig(format='%(asctime)s %(message)s', filename='data/example.log', level=logging.DEBUG)

We can now instanciate our algorithm. We use the Iterated Local Search in this example. It is mainly used to avoid local optima using multiple local search.

.. code:: python
    
    """
    imports part
    """
    ...

    import logging

    from macop.algorithms.IteratedLocalSearch import IteratedLocalSearch as ILS

    """
    Problem definition
    """
    ...

    """
    Algorithm parameters
    """
    ...

    if not os.path.exists('data'):
    os.makedirs('data')

    # logging configuration
    logging.basicConfig(format='%(asctime)s %(message)s', filename='data/example.log', level=logging.DEBUG)

    algo = ILS(init, evaluator, operators, policy, validator, _maximise=True)

The algorithm is now well defined and is ready to run ! But one thing can be done, and it's very interesting to avoir restart from scratch the algorithm run.
The use of checkpoint is available in `macop`. A `BasicCheckpoint` class let the algorithm save at `every` evaluations the best solution found.

We need to specify the use of checkpoint if we prefer to restart from.

.. code:: python
    
    """
    imports part
    """
    ...
    
    import logging

    from macop.algorithms.IteratedLocalSearch import IteratedLocalSearch as ILS
    from macop.checkpoints.BasicCheckpoint import BasicCheckpoint

    """
    Problem definition
    """
    ...

    """
    Algorithm parameters
    """
    ...

    if not os.path.exists('data'):
    os.makedirs('data')

    # logging configuration
    logging.basicConfig(format='%(asctime)s %(message)s', filename='data/example.log', level=logging.DEBUG)

    algo = ILS(init, evaluator, operators, policy, validator, _maximise=True)

    # we specify the checkpoint class directly, the frequency and the path we want to save algorithm evolution
    algo.addCheckpoint(_class=BasicCheckpoint, _every=5, _filepath='data/checkpoint.csv')


In this way, now we can run and obtained the best solution found in `n` evaluations

.. code:: python

    bestSol = algo.run(10000)
    print('Solution score is {}'.format(evaluator(bestSol)))

2. Multi-objective example
--------------------------

Available soon...