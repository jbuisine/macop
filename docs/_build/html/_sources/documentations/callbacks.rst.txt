Keep track
==============

Keeping track of the running algorithm can be useful on two levels. First of all to understand how it unfolded at the end of the classic run. But also in the case of the unwanted shutdown of the algorithm. 
This section will allow you to introduce the recovery of the algorithm thanks to a continuous backup functionality.

Logging into algorithm
~~~~~~~~~~~~~~~~~~~~~~

Some logs can be retrieve after running an algorithm. **Macop** uses the ``logging`` Python package in order to log algorithm advancement.

Here is an example of use when running an algorithm:

.. code-block:: python

    """
    basic imports
    """
    import logging

    # logging configuration
    logging.basicConfig(format='%(asctime)s %(message)s', filename='data/example.log', level=logging.DEBUG)

    ...
    
    # maximizing algorithm (relative to knapsack problem)
    algo = HillClimberBestImprovment(initialiser, evaluator, operators, policy, validator, maximise=True, verbose=False)

    # run the algorithm using local search and get solution found 
    solution = algo.run(evaluations=100)
    print(solution.fitness)

Hence, log data are saved into ``data/example.log`` in our example.

Callbacks introduction
~~~~~~~~~~~~~~~~~~~~~~~

Having output logs can help to understand an error that has occurred, however all the progress of the research carried out may be lost. 
For this, the functionality relating to callbacks has been developed.

Within **Macop**, a callback is a specific instance of ``macop.callbacks.Callback`` that allows you to perform an action of tracing / saving information **every** ``n`` **evaluations** but also reloading information if necessary when restarting an algorithm.


.. code-block:: python

    class Callback():

        def __init__(self, every, filepath):
            ...

        @abstractmethod
        def run(self):
            """
            Check if necessary to do backup based on `every` variable
            """
            pass

        @abstractmethod
        def load(self):
            """
            Load last backup line of solution and set algorithm state at this backup
            """
            pass

        def setAlgo(self, algo):
            """
            Specify the main algorithm instance reference
            """
            ...


- The ``run`` method will be called during run process of the algo and do backup at each specific number of evaluations. 
- The ``load`` method will be used to reload the state of the algorithm from the last information saved. All saved data is saved in a file whose name will be specified by the user.

Towards the use of Callbacks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We are going to create our own Callback instance called ``BasicCheckpoint`` which will save the best solution found and number of evaluations done in order to reload it for the next run of our algorithm.

.. code-block:: python

    """
    module imports
    """
    from macop.callbacks.base import Callback


    class BasicCheckpoint(Callback):
        
        def run(self):
            """
            Check if necessary to do backup based on `every` variable
            """
            # get current best solution
            solution = self.algo._bestSolution

            currentEvaluation = self.algo.getGlobalEvaluation()

            # backup if necessary every number of evaluations
            if currentEvaluation % self._every == 0:

                # create specific line with solution data
                solution.data = ""
                solutionSize = len(solution.getdata = ))

                for index, val in enumerate(solution.getdata = )):
                    solution.data += str(val)

                    if index < solutionSize - 1:
                        solution.data += ' '

                # number of evaluations done, solution data and fitness score
                line = str(currentEvaluation) + ';' + solution.data + ';' + str(
                    solution.fitness) + ';\n'

                # check if file exists
                if not os.path.exists(self._filepath):
                    with open(self._filepath, 'w') as f:
                        f.write(line)
                else:
                    with open(self._filepath, 'a') as f:
                        f.write(line)

        def load(self):
            """
            Load last backup line and set algorithm state (best solution and evaluations)
            """
            if os.path.exists(self._filepath):

                with open(self._filepath) as f:

                    # get last line and read data
                    lastline = f.readlines()[-1]
                    data = lastline.split(';')

                    # get evaluation  information
                    globalEvaluation = int(data[0])

                    # restore number of evaluations
                    if self.algo.getParent() is not None:
                        self.algo.getParent()._numberOfEvaluations = globalEvaluation
                    else:
                        self.algo._numberOfEvaluations = globalEvaluation

                    # get best solution data information
                    solution.data = list(map(int, data[1].split(' ')))

                    # avoid uninitialised solution
                    if self.algo._bestSolution is None:
                        self.algo._bestSolution = self.algo.initialiser()

                    # set to algorithm the lastest obtained best solution
                    self.algo._bestsolution.getdata = ) = np.array(solution.data)
                    self.algo._bestSolution._score = float(data[2])


In this way, it is possible to specify the use of a callback to our algorithm instance:


.. code-block:: python

    ...
    
    # maximizing algorithm (relative to knapsack problem)
    algo = HillClimberBestImprovment(initialiser, evaluator, operators, policy, validator, maximise=True, verbose=False)

    callback = BasicCheckpoint(every=5, filepath='data/hillClimberBackup.csv')

    # add callback into callback list
    algo.addCallback(callback)

    # run the algorithm using local search and get solution found 
    solution = algo.run(evaluations=100)
    print(solution.fitness)


.. note::
    It is possible to add as many callbacks as desired in the algorithm in question.


Previously, some methods of the abstract ``Algorithm`` class have not been presented. These methods are linked to the use of callbacks, 
in particular the ``addCallback`` method which allows the addition of a callback to an algorithm instance as seen above.

- The ``resume`` method will reload all callbacks list using ``load`` method.
- The ``progress`` method will ``run`` each callbacks during the algorithm search.

If we want to exploit this functionality, then we will need to exploit them within our algorithm. Let's make the necessary modifications for our algorithm ``IteratedLocalSearch``:


.. code-block:: python

    """
    module imports
    """
    from macop.algorithms.base import Algorithm

    class IteratedLocalSearch(Algorithm):
        
        ...

        def run(self, evaluations, ls_evaluations=100):
            """
            Run the iterated local search algorithm using local search
            """

            # by default use of mother method to initialise variables
            super().run(evaluations)

            # initialise current solution
            self.initRun()

            # restart using callbacks backup list
            self.resume()

            # local search algorithm implementation
            while not self.stop():

                # create and search solution from local search
                newSolution = self._localSearch.run(ls_evaluations)

                # if better solution than currently, replace it
                if self.isBetter(newSolution):
                    self._bestSolution = newSolution

                # check if necessary to call each callbacks
                self.progress()

                self.information()

            return self._bestSolution


All the features of **Macop** were presented. The next section will aim to quickly present the few implementations proposed within **Macop** to highlight the modulality of the package.