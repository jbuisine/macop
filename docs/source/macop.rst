Documentation
=============

macop
-------------------

macop.algorithms
-------------------

.. autosummary::
   :toctree: macop
   
   macop.algorithms.Algorithm
   macop.algorithms.IteratedLocalSearch
   macop.algorithms.LocalSearch

macop.checkpoints
-------------------

.. autosummary::
   :toctree: macop
   
   macop.checkpoints.BasicCheckpoint
   macop.checkpoints.Checkpoint

macop.evaluators
-------------------

.. autosummary::
   :toctree: macop
   
   macop.evaluators.EvaluatorExample

macop.operators
-------------------

.. autosummary::
   :toctree: macop
   
   macop.operators.crossovers.Crossover
   macop.operators.crossovers.RandomSplitCrossover
   macop.operators.crossovers.SimpleCrossover

   macop.operators.mutators.Mutation
   macop.operators.mutators.SimpleBinaryMutation
   macop.operators.mutators.SimpleMutation

   macop.operators.policies.Policy
   macop.operators.policies.RandomPolicy
   macop.operators.policies.UCBPolicy
   
   macop.operators.Operator

macop.solution
-------------------

.. autosummary::
   :toctree: macop

   macop.solutions.BinarySolution
   macop.solutions.CombinatoryIntegerSolution
   macop.solutions.IntegerSolution
   macop.solutions.Solution