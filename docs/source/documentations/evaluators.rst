5. Use of evaluators
====================

Now that it is possible to generate a solution randomly or not. It is important to know the value associated with this solution. We will then speak of evaluation of the solution. With the score associated with it, the `fitness`.

5.1. Generic evaluator
~~~~~~~~~~~~~~~~~~~~~~

As for the management of solutions, a generic evaluator class ``macop.evaluators.base.Evaluator`` is developed within **Macop**:

Abstract Evaluator class is used for computing fitness score associated to a solution. To evaluate all the solutions, this class:

- stores into its ``_data`` dictionary attritute required measures when computing a solution
- has a ``compute`` abstract method enable to compute and associate a score to a given solution
- stores into its ``_algo`` attritute the current algorithm to use (we will talk about algorithm later)

.. code-block: python

    class Evaluator():
    """
    Abstract Evaluator class which enables to compute solution using specific `_data` 
    """
    def __init__(self, data):
        self._data = data

    @abstractmethod
    def compute(self, solution):
        """
        Apply the computation of fitness from solution
        """
        pass

    def setAlgo(self, algo):
        """
        Keep into evaluator reference of the whole algorithm
        """
        self._algo = algo

We must therefore now create our own evaluator based on the proposed structure.

5.2. Custom evaluator
~~~~~~~~~~~~~~~~~~~~~

To create our own evaluator, we need both:

- data useful for evaluating a solution
- calculate the score (fitness) associated with the state of the solution from these data. Hence, implement specific ``compute`` method.

We will define the ``KnapsackEvaluator`` class, which will therefore allow us to evaluate solutions to our current problem.

.. code-block:: python

    """
    modules imports
    """
    from macop.evaluators.base import Evaluator

    class KnapsackEvaluator(Evaluator):
        
        def compute(solution):

            # `_data` contains worths array values of objects
            fitness = 0
            for index, elem in enumerate(solution._data):
                fitness += self._data['worths'][index] * elem

            return fitness


It is now possible to initialize our new evaluator with specific data of our problem instance:

.. code-block:: python

    """
    Problem instance definition
    """
    elements_score = [ 4, 2, 10, 1, 2 ] # worth of each object
    elements_weight = [ 12, 1, 4, 1, 2 ] # weight of each object

    """
    Evaluator problem instance
    """
    evaluator = KnapsackEvaluator(data={'worths': elements_score})

    # using defined BinarySolution
    solution = BinarySolution.random(5)

    # obtaining current solution score
    solution_fitness = solution.evaluate(evaluator)

    # score is also stored into solution
    solution_fitness = solution.fitness()

.. note::
    The current developed ``KnapsackEvaluator`` is available into ``macop.evaluators.mono.KnapsackEvaluator`` in **Macop**.

In the next part we will see how to modify our current solution with the use of modification operator.