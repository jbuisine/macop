Some examples
=====================================

1. Mono-objective
-----------------------

In this tutorial, we introduce the way of using `macop` and running your algorithm quickly.
First of all we need to define the kind of solution which best represent the problem. As example, we use the well known knapsack problem using 30 objects (solution size of 30).

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

    elements_score = [ random.randint(1, 20) for _ in range(30) ] # value of each object
    elements_weight = [ random.randint(5, 25) for _ in range(30) ] # weight of each object

We can now define the solution representation. In knapsack problem we want to fill our knapsack in an optimization way selecting or not each component (object).
The best way to represent this problem is to use the `BinarySolution` from `macop` which stores solution as a binary array.

Using the solution representation, we need to define multiple elements to fit our algorithm :

- function which validates or not a solution (based on constraints)

- function which evaluates the solution (in order to obtain fitness)

- initialization solution function

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

    elements_score = [ random.randint(1, 20) for _ in range(30) ] # value of each object
    elements_weight = [ random.randint(5, 25) for _ in range(30) ] # weight of each object

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

    from macop.algorithms.mono.IteratedLocalSearch import IteratedLocalSearch as ILS

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
The use of checkpoint is available in `macop`. A `BasicCheckpoint` class let the algorithm save at `every` evaluations the best solution found. This class is based on callback process. 
A Callback is runned every number of evaluations but can also implement the `load` method in order to to specific instrusctions when initializing algorithm.

It's important to note, we can add any number of callbacks we want. For tabu search as example, we need to store many solutions.

In our case, we need to specify the use of checkpoint if we prefer to restart from.

.. code:: python
    
    """
    imports part
    """
    ...
    
    import logging

    from macop.algorithms.mono.IteratedLocalSearch import IteratedLocalSearch as ILS
    from macop.callbacks.BasicCheckpoint import BasicCheckpoint

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

    # create instance of BasicCheckpoint callback
    callback = BasicCheckpoint(_every=5, _filepath='data/checkpoint.csv')

    # Add this callback instance into list of callback
    # It tells the algorithm to apply this callback every 5 evaluations
    # And also the algorithm to load checkpoint if exists before running by using `load` method of callback
    algo.addCallback(callback)


In this way, now we can run and obtained the best solution found in `n` evaluations

.. code:: python

    bestSol = algo.run(10000)
    print('Solution score is {}'.format(evaluator(bestSol)))

2. Multi-objective
-------------------

1.1 Problem definition
~~~~~~~~~~~~~~~~~~~~~~

In this example we also use the knapsack problem, with here, 2 kinds of value for each object in the knapsack :

- value 1 of each component of knapsack
- value 2 of each component of knapsack
- weight associated to each of these components (objects)

In multi-objective algorithm, we do not only found one solution but a set of non-dominated solutions called Pareto front as we have multiple objectives.

.. code:: python
    
    """
    imports part
    """
    import random

    """
    Problem definition
    """
    random.seed(42)

    elements_score1 = [ random.randint(1, 20) for _ in range(200) ] # value 1 of each object
    elements_score2 = [ random.randint(1, 20) for _ in range(200) ] # value 2 of each object
    elements_weight = [ random.randint(5, 25) for _ in range(200) ] # weight of each object


We can now define the solution representation. In knapsack problem we want to fill our knapsack in an optimization way selecting or not each component (object).
The best way to represent this problem is to use the `BinarySolution` from `macop` which stores solution as a binary array.

Using the solution representation, we need to define multiple elements to fit our algorithm :

- function which validates or not a solution (based on constraints)
- the first objective function which evaluates the solution (fitness score for objective 1)
- the second objective function which evaluates the solution (fitness score for objective 2)
- initialization solution function

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

    elements_score1 = [ random.randint(1, 20) for _ in range(200) ] # value 1 of each object
    elements_score2 = [ random.randint(1, 20) for _ in range(200) ] # value 2 of each object
    elements_weight = [ random.randint(5, 25) for _ in range(200) ] # weight of each object

    # 1. validator function (we accept only bag with maximum weight 80kg)
    def validator(_solution):

        weight_sum = 0
        for index, elem in enumerate(_solution.data):
            weight_sum += elements_weight[index] * elem

        if weight_sum <= 80:
            return True
        else:
            False

    # 2. functions which computes fitness of solution for the two objectives
    def evaluator1(_solution):

        fitness = 0
        for index, elem in enumerate(_solution.data):
            fitness += (elements_score1[index] * elem)

        return fitness

    def evaluator2(_solution):

        fitness = 0
        for index, elem in enumerate(_solution.data):
            fitness += (elements_score2[index] * elem)

        return fitness

    # 3. function which here initializes solution ramdomly and check validity of solution
    def init():
        return BinarySolution([], 200).random(validator)

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

1.3 How works multi-objective in macop ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As we have now multiple objectives, we define a new algorithm named MOEAD for `MultiObjective Evolutionary Algorithm with Decomposition` inside `macop.algorithms.multi.MOEAD`. 
The principle of this algorithm is to decompose the multi-objective problem into several single-objective problems (see MOEAD_ documentation framework).
To implement this algorithm, we now define the attribute `evaluator` as a list of evaluators. The number of objectives is defined by the length of this list and generated weights for each sub problem too.

The `mu` attribute represent the number of sub problems and hence our current population of solutions.

.. _MOEAD: https://sites.google.com/view/moead/home

In order to represent the `mu` mono-objective sub problems (obtained from weighted decomposition), we define the `macop.algorithms.multi.MOSubProblem` class. 
This class enables to compute and find best solution from weighted decomposition. The `weights` attribute of this class stores the weight for each objective of this sub problem instance.

The `evaluator` of MOSubProblem is defined as below:

.. code:: python

    def moEvaluator(_solution, _evaluator, _weights):

        scores = [eval(_solution) for eval in _evaluator]

        # associate objectives scores to solution
        _solution.scores = scores

        # return the weighted sum
        return sum([scores[i] for i, w in enumerate(_weights)])

    ...

    # compute weighted sum from solution using list of evaluators and weights for current sub problem
    sub_evaluator = lambda _solution: moEvaluator(_solution, _evaluator, weights[i])


This function computes the weighted sum of objectives (to transform sub problem into mono-objective) and also stores the objectives scores into solution using the dynamic added `scores` attributes.
This is an example, we based our function using classical weighted sum, we can also implement Tchebychev_ method.

.. _Tchebychev: https://repository.lib.ncsu.edu/handle/1840.16/272

We can now instance our MOEAD algorithm:

.. code:: python
    
    """
    imports part
    """
    ...
    
    import logging

    from macop.algorithms.multi.MOEAD import MOEAD

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

    algo = MOEAD(init, [evaluator1, evaluator2], operators, policy, validator, _maximise=True)

1.4 Checkpoint multi-objective solutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To keep track of our `mu` population and `pfPop` pareto front set, 2 new callbacks have been defined:

.. code:: python
    
    """
    imports part
    """
    ...
    
    import logging

    from macop.algorithms.multi.MOEAD import MOEAD
    from macop.callbacks.MultiCheckpoint import MultiCheckpoint
    from macop.callbacks.ParetoFront import ParetoFront

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

    # Add this callback instance into list of callback
    # It tells the algorithm to apply this callback every 5 evaluations
    # And also the algorithm to load checkpoint if exists before running by using `load` method of callback
    algo.addCallback(MultiCheckpoint(_every=5, _filepath='data/checkpointMOEAD.csv'))

    # add Pareto Checkpoint callback instance too
    algo.addCallback(ParetoCheckpoint(_every=5, _filepath='data/paretoMOEAD.csv'))

These callbacks only stores the last states of `mu` population and `pfPop`.

We can now run the MOEAD algorithm instance:

.. code:: python

    paretoFront = algo.run(10000) 

    print("Pareto front is composed of", len(paretoFront), "solutions")