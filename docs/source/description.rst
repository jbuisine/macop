Description
=====================================

.. image:: _static/logo_macop.png
   :width: 350 px
   :align: center


Context
------------

`macop` is an optimization Python package which not implement the whole available algorithms in the literature but let you the possibility to quickly develop and test your own algorithm and strategies. The main objective of this package is to be the most flexible as possible and hence, to offer a maximum of implementation possibilities.

Installation
------------

Just install package using `pip` Python package manager: 

.. code:: bash
   
   pip install macop


How to use ?
------------

Load all `macop` implemented features:

.. code:: python
    
   from macop.algorithms.IteratedLocalSearch import IteratedLocalSearch as ILS
   from macop.solutions.BinarySolution import BinarySolution
   from macop.evaluators.EvaluatorExample import evaluatorExample

   from macop.operators.mutators.SimpleMutation import SimpleMutation
   from macop.operators.mutators.SimpleBinaryMutation import SimpleBinaryMutation
   from macop.operators.crossovers.SimpleCrossover import SimpleCrossover
   from macop.operators.crossovers.RandomSplitCrossover import RandomSplitCrossover

   from macop.operators.policies.RandomPolicy import RandomPolicy

   from macop.checkpoints.BasicCheckpoint import BasicCheckpoint

   # logging configuration
   logging.basicConfig(format='%(asctime)s %(message)s', filename='example.log', level=logging.DEBUG)

   # default validator
   def validator(solution):
      return True

   # define init random solution
   def init():
      return BinarySolution([], 30).random(validator)

   filepath = "checkpoints.csv"

   def main():

      operators = [SimpleBinaryMutation(), SimpleMutation(), SimpleCrossover(), RandomSplitCrossover()]
      policy = RandomPolicy(operators)

      algo = ILS(init, evaluatorExample, operators, policy, validator, True)
      algo.addCheckpoint(_class=BasicCheckpoint, _every=5, _filepath=filepath)

      bestSol = algo.run(425)

      print("Found ", bestSol)


   if __name__ == "__main__":
      main()
